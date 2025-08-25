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
                    bat '''
                    call venv\\Scripts\\activate
                    start /MIN cmd /c "python -m uvicorn main:app --host 127.0.0.1 --port 8000"
                    '''
                }
                bat 'ping 127.0.0.1 -n 20 >nul'
            }
        }

        stage('Verify Backend') {
            steps {
                bat 'powershell -Command "try { Invoke-WebRequest http://127.0.0.1:8000/docs -UseBasicParsing -TimeoutSec 10; exit 0 } catch { exit 1 }"'
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
                    bat '''
                        if exist requirements.txt (
                            call venv\\Scripts\\activate && pip install -r requirements.txt
                        ) else (
                            echo No requirements.txt in test repo
                        )
                    '''
                    bat 'call venv\\Scripts\\activate && pip install requests pytest pytest-html'
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('tests') {
                    bat 'call venv\\Scripts\\activate && pytest tests/test_cases --html=reports/test_report.html --self-contained-html'
                }
            }
        }

        stage('Archive Report') {
            steps {
                dir('tests') {
                    archiveArtifacts artifacts: 'reports/test_report.html', fingerprint: true
                    publishHTML(target: [
                        reportName: 'Test Report',
                        reportDir: 'reports',
                        reportFiles: 'test_report.html',
                        alwaysLinkToLastBuild: true,
                        keepAll: true
                    ])
                }
            }
        }

        // ✅ Only runs if ALL previous stages succeed
        stage('Merge dev to main') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                dir('backend') {
                    withCredentials([usernamePassword(credentialsId: 'github-creds', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                        bat '''
                        git config user.name "jenkins"
                        git config user.email "jenkins@local"

                        REM ensure we are on dev
                        git checkout dev
                        git pull origin dev

                        REM fetch main branch
                        git fetch origin main

                        REM switch to main
                        git checkout main
                        git pull origin main

                        REM merge dev into main
                        git merge dev --no-ff -m "Auto-merge: dev -> main after successful Jenkins build"

                        REM push main
                        git push origin main
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            bat '''
            powershell -NoLogo -NonInteractive -Command ^
            "Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }; exit 0"
            '''
        }
    }
}
