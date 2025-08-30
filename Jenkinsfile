pipeline {
    agent any
    options { disableConcurrentBuilds() }

    stages {
        stage('Checkout Backend') {
            steps {
                dir('backend') {
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/dev']],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [[$class: 'CloneOption', noTags: false, shallow: false, depth: 0]],
                        userRemoteConfigs: [[
                            url: 'https://github.com/vinay-hegde-17/TestFastAPI.git',
                            credentialsId: 'github-creds'
                        ]]
                    ])
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
                    start /MIN cmd /c "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
                    '''
                }
            }
        }

        stage('Verify Backend') {
            steps {
                bat '''
                powershell -Command "
                $max=15;
                for ($i=0; $i -lt $max; $i++) {
                try {
                    Invoke-WebRequest http://127.0.0.1:8000/docs -UseBasicParsing -TimeoutSec 2;
                    Write-Host 'Backend is UP';
                    exit 0
                } catch {
                    Start-Sleep -Seconds 2
                }
                }
                Write-Error 'Backend failed to start';
                exit 1
                "
                '''
            }
        }

        stage('Checkout Tests') {
            steps {
                dir('tests') {
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/dev']],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [[$class: 'CloneOption', noTags: false, shallow: false, depth: 0]],
                        userRemoteConfigs: [[
                            url: 'https://github.com/vinay-hegde-17/VinayTestAutomation.git',
                            credentialsId: 'github-creds'
                        ]]
                    ])
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
                    bat 'call venv\\Scripts\\activate && pytest --html=reports/test_report.html --self-contained-html'
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
    }

    post {
        success {
            dir('backend') {
                withCredentials([usernamePassword(credentialsId: 'github-creds', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    bat '''
                        git config user.email "jenkins@local"
                        git config user.name "Jenkins"

                        REM Fetch all branches with full history
                        git fetch --all

                        REM Ensure we are on main branch
                        git checkout main
                        git pull origin main

                        REM Merge dev into main
                        git merge origin/dev

                        REM Debug info
                        git log --oneline -10
                        git status

                        REM Push merged code back to main
                        git push https://%GIT_USER%:%GIT_PASS%@github.com/vinay-hegde-17/TestFastAPI.git main
                    '''
                }
            }
        }

        always {
            bat '''
            powershell -NoLogo -NonInteractive -Command ^
            "Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }; exit 0"
            '''
        }
    }
}
