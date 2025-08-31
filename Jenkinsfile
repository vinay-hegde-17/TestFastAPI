pipeline {
    agent any
    options { 
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        GITHUB_CREDENTIALS = 'github-creds'
        BACKEND_REPO = 'https://github.com/vinay-hegde-17/TestFastAPI.git'
        TEST_REPO = 'https://github.com/vinay-hegde-17/VinayTestAutomation.git'
    }

    stages {
        stage('Checkout Backend') {
            steps {
                dir('backend') {
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/dev']],
                        userRemoteConfigs: [[
                            url: "${BACKEND_REPO}",
                            credentialsId: 'github-creds',
                        ]]
                    ])
                }
            }
        }

        stage('Backend venv & deps') {
            steps {
                dir('backend') {
                    bat '''
                        if exist venv rmdir /s /q venv
                        python -m venv venv
                        call venv\\Scripts\\activate && python -m pip install --upgrade pip
                        call venv\\Scripts\\activate && pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Start Backend') {
            steps {
                dir('backend') {
                    bat '''
                        call venv\\Scripts\\activate && ^
                        python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload --timeout-keep-alive 120
                    '''
                }
            }
        }

        stage('Verify Backend') {
            steps {
                retry(5) {
                    bat '''
                        powershell -Command ^
                        "try {
                            Invoke-WebRequest http://127.0.0.1:8000/docs -UseBasicParsing -TimeoutSec 10;
                            Write-Host 'Backend is running'; exit 0
                        } catch {
                            Write-Host 'Backend not ready, retrying...'; exit 1
                        }"
                    '''
                }
            }
        }

        stage('Checkout Tests') {
            steps {
                dir('tests') {
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/dev']],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [],
                        userRemoteConfigs: [[
                            url: "${TEST_REPO}",
                            credentialsId: 'github-creds',
                        ]]
                    ])
                }
            }
        }

        stage('Test venv & deps') {
            steps {
                dir('tests') {
                    bat '''
                        if exist venv rmdir /s /q venv
                        python -m venv venv
                        call venv\\Scripts\\activate && python -m pip install --upgrade pip
                        if exist requirements.txt (
                            call venv\\Scripts\\activate && pip install -r requirements.txt
                        ) else (
                            echo No requirements.txt in test repo
                        )
                        call venv\\Scripts\\activate && pip install requests pytest pytest-html
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                dir('tests') {
                    bat '''
                        call venv\\Scripts\\activate && pytest --html=reports/test_report.html --self-contained-html --tb=short
                    '''
                }
            }
            post {
                always {
                    dir('tests') {
                        // Ensure reports directory exists
                        bat 'if not exist reports mkdir reports'
                    }
                }
            }
        }

        stage('Archive Test Results') {
            steps {
                dir('tests') {
                    archiveArtifacts artifacts: 'reports/test_report.html', 
                                   fingerprint: true,
                                   allowEmptyArchive: true

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

        stage('Debug Git Status') {
            steps {
                dir('backend') {
                    bat '''
                        git status
                        git branch -a
                        git log --oneline -3
                    '''
                }
            }
        }

        stage('Push to Main Branch') {
            when {
                allOf {
                    success()
                    expression { env.BRANCH_NAME == 'dev' || env.GIT_BRANCH == 'dev' }
                }
            }
            steps {
                    dir('backend') { withCredentials([usernamePassword(
                            credentialsId: "${GITHUB_CREDENTIALS}",
                            usernameVariable: 'GIT_USER',
                            passwordVariable: 'GIT_PASS'
                        )]) {
                            bat """
                                git config user.name "Jenkins CI"
                                git config user.email "jenkins@yourdomain.com"

                                git fetch origin
                                git checkout dev
                                git pull origin dev

                                git checkout -B main
                                git merge dev --no-edit

                                git push https://${GIT_USER}:${GIT_PASS}@github.com/vinay-hegde-17/TestFastAPI.git main --force
                            """
                        }
                }
            }
        }

        stage('Trigger Vercel Deployment') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo "🚀 Main branch updated - Vercel will auto-deploy"
            }
        }
    }

    post {
        always {
            bat '''
                powershell -NoLogo -NonInteractive -Command ^
                "Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }; exit 0"
            '''
            bat '''
                if exist backend\\venv rmdir /s /q backend\\venv
                if exist tests\\venv rmdir /s /q tests\\venv
            '''
        }
        success {
            echo "🎉 Pipeline completed successfully! Code has been merged into main."
        }
    }
}