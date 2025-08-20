pipeline {
    agent any
    stages {
        stage('Checkout Backend') {
            steps {
                dir('backend') {
                    git branch: 'dev', url: 'https://github.com/vinay-hegde-17/TestFastAPI.git'
                }
            }
        }

        stage('Backend venv & deps') {
            steps {
                dir('backend') {
                    bat 'python -m venv venv'
                    bat 'call venv\\Scripts\\activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Start Backend') {
            steps {
                dir('backend') {
                    // call the batch file (make sure run_server.bat activates venv)
                    bat 'start "" /B run_server.bat'
                }
                // wait ~5s for server
                bat 'ping 127.0.0.1 -n 6 >nul'
            }
        }

        stage('Checkout Tests') {
            steps {
                dir('tests') {
                    git branch: 'dev', url: 'https://github.com/vinay-hegde-17/VinayTestAutomation.git'
                }
            }
        }

        stage('Test venv & deps') {
            steps {
                dir('tests') {
                    bat 'python -m venv venv'
                    bat 'call venv\\Scripts\\activate && pip install --upgrade pip'
                    // install pytest + reporter
                    bat 'call venv\\Scripts\\activate && pip install requests pytest pytest-html'
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('tests') {
                    bat 'call venv\\Scripts\\activate && pytest --maxfail=1 --disable-warnings -q --html=report.html --self-contained-html'
                }
            }
        }

        stage('Archive Report') {
            steps {
                dir('tests') {
                    archiveArtifacts artifacts: 'report.html', fingerprint: true
                }
            }
        }
    }

    post {
        always {
            // Kill FastAPI running on port 8000
            bat 'powershell -NoLogo -NonInteractive -Command "Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }"'
        }
    }
}
