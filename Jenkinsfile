pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: 'https://github.com/vinay-hegde-17/TestFastAPI.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Backend Tests') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings --html=reports/backend_report.html'
            }
        }
        stage('Archive Report') {
            steps {
                archiveArtifacts artifacts: 'reports/*.html', fingerprint: true
            }
        }
    }
}
