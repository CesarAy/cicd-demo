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
}
