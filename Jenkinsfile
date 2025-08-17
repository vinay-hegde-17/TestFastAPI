pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: 'https://github.com/vinay-hegde-17/TestFastAPI.git'
            }
        }
        stage('Setup venv') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }
        stage('Run Backend') {
            steps {
                // Run FastAPI in background
                bat 'start /B run_server.bat'
            }
        }
    }
    post {
        success {
            echo 'Backend started successfully'
        }
    }
}
