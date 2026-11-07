pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Build') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m compileall -q calculator.py test_calculator.py'
            }
        }
        stage('Unit tests') {
            steps {
                sh 'python3 -m unittest discover -v'
            }
        }
    }

    post {
        always {
            script {
                withEnv(["BUILD_STATUS=${currentBuild.currentResult}",
                         'WEBEX_ROOM_TITLE=CI/CD Build Notifications']) {
                    withCredentials([string(credentialsId: 'webex-bot-token',
                                            variable: 'WEBEX_BOT_TOKEN')]) {
                        sh 'python3 scripts/notify_webex.py'
                    }
                }
            }
        }
    }
}
