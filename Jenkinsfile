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
                bat 'call venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Run Backend') {
            steps {
                // Start FastAPI using your .bat file
                bat 'start "" /B run_server.bat'

                // Give the server time to start (5 sec)
                bat 'ping 127.0.0.1 -n 6 >nul'
            }
        }
    }

    post {
        success {
            echo 'Backend started successfully'
        }
    }
}
