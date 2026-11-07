"""Send a Jenkins result using credentials supplied through the environment."""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def main():
    token = os.environ.get("WEBEX_BOT_TOKEN")
    room_id = os.environ.get("WEBEX_ROOM_ID")
    if not token:
        print("Webex notification requires WEBEX_BOT_TOKEN.", file=sys.stderr)
        return 1

    if not room_id:
        title = os.environ.get("WEBEX_ROOM_TITLE", "CI/CD Build Notifications")
        lookup = Request(
            "https://webexapis.com/v1/rooms?max=1000",
            headers={"Authorization": f"Bearer {token}"},
        )
        try:
            with urlopen(lookup, timeout=30) as response:
                rooms = json.load(response).get("items", [])
                if response.headers.get("Link"):
                    print("Set WEBEX_ROOM_ID explicitly: room list has more pages.", file=sys.stderr)
                    return 1
        except HTTPError as error:
            print(f"Webex room lookup failed: HTTP {error.code}", file=sys.stderr)
            return 1
        except (URLError, TimeoutError, ValueError):
            print("Webex room lookup failed: connection error or invalid response.", file=sys.stderr)
            return 1
        matches = [room for room in rooms if room.get("title") == title]
        if len(matches) != 1:
            print(f"Expected one Webex space named {title!r}; found {len(matches)}.", file=sys.stderr)
            print("Check the space name and bot membership, or set WEBEX_ROOM_ID.", file=sys.stderr)
            return 1
        room_id = matches[0]["id"]
        print(f"Found Webex space: {title}")

    status = os.environ.get("BUILD_STATUS", "UNKNOWN")
    job = os.environ.get("JOB_NAME", "cicd-demo")
    number = os.environ.get("BUILD_NUMBER", "unknown")
    commit = os.environ.get("GIT_COMMIT", "unknown")
    build_url = os.environ.get("BUILD_URL", "")
    text = (
        f"Jenkins build: {status}\n"
        f"Job: {job}\nBuild: #{number}\n"
        f"Commit: {commit}\nConsole: {build_url}console"
    )
    request = Request(
        "https://webexapis.com/v1/messages",
        data=json.dumps({"roomId": room_id, "text": text}).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            if response.status != 200:
                print(f"Unexpected Webex response: HTTP {response.status}", file=sys.stderr)
                return 1
    except HTTPError as error:
        # Avoid printing request headers or response bodies containing private data.
        print(f"Webex notification failed: HTTP {error.code}", file=sys.stderr)
        return 1
    except (URLError, TimeoutError):
        print("Webex notification failed: connection error or timeout.", file=sys.stderr)
        return 1
    print(f"Webex notification sent: {status}, build #{number}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
