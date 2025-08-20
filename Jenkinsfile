pipeline {
    agent any
    options { disableConcurrentBuilds() }

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
                    bat 'call venv\\Scripts\\activate && python -m pip install --upgrade pip'
                    bat 'call venv\\Scripts\\activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Start Backend') {
            steps {
                dir('backend') {
                    // Run FastAPI using app.main:app (like your run_server.bat)
                    bat 'start "" /B cmd /c "call venv\\Scripts\\activate && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"'
                }
                // wait ~5 seconds for server startup
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
                    bat 'call venv\\Scripts\\activate && python -m pip install --upgrade pip'
                    bat 'if exist requirements.txt (call venv\\Scripts\\activate && pip install -r requirements.txt) else (echo No requirements.txt in tests repo)'
                    bat 'call venv\\Scripts\\activate && pip install requests pytest pytest-html'
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('tests') {
                    // run tests (adjust test folder if different)
                    bat 'call venv\\Scripts\\activate && pytest tests --maxfail=1 --disable-warnings -q --html=report.html --self-contained-html'
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
            // Kill backend running on port 8000 (cleanup)
            bat 'powershell -NoLogo -NonInteractive -Command "Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }"'
        }
        success {
            echo '✅ Backend and Tests ran successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs!'
        }
    }
}
