pipeline {
    agent any
    options { 
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
                    git branch: 'dev', 
                        url: "${BACKEND_REPO}",
                        credentialsId: "${GITHUB_CREDENTIALS}"
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
                    bat 'start "" /B cmd /c "call venv\\Scripts\\activate && python -m uvicorn main:app --host 127.0.0.1 --port 8000"'
                }
                bat 'ping 127.0.0.1 -n 20 >nul'
            }
        }

        stage('Verify Backend') {
            steps {
                retry(3) {
                    bat 'powershell -Command "try { Invoke-WebRequest http://127.0.0.1:8000/docs -UseBasicParsing -TimeoutSec 15; Write-Host \\"Backend is running\\"; exit 0 } catch { Write-Host \\"Backend not ready, retrying...\\"; exit 1 }"'
                }
            }
        }

        stage('Checkout Tests') {
            steps {
                dir('tests') {
                    git branch: 'dev',
                        url: "${TEST_REPO}",
                        credentialsId: "${GITHUB_CREDENTIALS}"
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
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    dir('backend') {
                        withCredentials([string(credentialsId: "${GITHUB_CREDENTIALS}", variable: 'GITHUB_TOKEN')]) {
                            bat '''
                                git config user.name "Jenkins CI"
                                git config user.email "jenkins@yourdomain.com"
                                
                                REM Fetch all branches
                                git fetch origin
                                
                                REM Force checkout main and reset to match dev
                                git checkout -B main origin/dev
                                
                                REM Push to main (this will make main identical to dev)
                                git push https://%GITHUB_TOKEN%@github.com/vinay-hegde-17/TestFastAPI.git main --force
                            '''
                        }
                    }
                }
            }
            post {
                success {
                    echo "✅ Successfully pushed to main branch! Ready for Vercel deployment."
                }
                failure {
                    echo "❌ Failed to push to main branch. Check Git configuration and permissions."
                }
            }
        }

        stage('Trigger Vercel Deployment') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    echo "🚀 Main branch updated - Vercel will auto-deploy if connected to main branch"
                    // Optional: Add webhook call to trigger Vercel deployment manually
                    // bat 'curl -X POST "your-vercel-webhook-url"'
                }
            }
        }
    }

    post {
        always {
            // Cleanup: Stop backend server
            bat '''
                powershell -NoLogo -NonInteractive -Command ^
                "Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }; exit 0"
            '''
            
            // Cleanup: Remove virtual environments to save space
            bat '''
                if exist backend\\venv rmdir /s /q backend\\venv
                if exist tests\\venv rmdir /s /q tests\\venv
            '''
        }
        
        success {
            echo "🎉 Pipeline completed successfully! Code has been pushed to main and is ready for deployment."
        }
        
        failure {
            echo "💥 Pipeline failed. Check the logs above for details."
        }
        
        unstable {
            echo "⚠️ Pipeline completed with warnings. Check test results."
        }
    }
}