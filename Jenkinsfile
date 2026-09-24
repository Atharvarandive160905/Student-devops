pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh '''
                python3 -m venv .ci-venv
                . .ci-venv/bin/activate
                pip install -r requirements.txt
                pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t student-devops:${BUILD_NUMBER} .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop student-app || true
                docker rm student-app || true
                docker run -d --name student-app -p 5000:5000 student-devops:${BUILD_NUMBER}
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                sleep 2
                python3 -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/health').read().decode())"
                '''
            }
        }
    }
}
