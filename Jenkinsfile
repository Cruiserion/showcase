// Basic Jenkins pipeline for Python codebase scanning

// Pre-requisites:
// - git credentials configured in Jenkins
// - python installed on Jenkins node
// - sonarqube instance running and the connection details configured in Jenkins
// - mail server running and the connection details configured in Jenkins

pipeline {
    stages {

        environment {
            EMAIL_REPORT_TO = 'someone@somewhere.com; someones-tech-lead@somewhere.com'
        }

        stage('Pull repo to agent') {
            steps {
                git branch: "main", credentialsId: "showcase-deploy-token", url: "https://github.com/Cruiserion/showcase.git"
            }
        }

        stage('SonarQube scan') {
            environment {
                SCANNER_HOME = tool 'sonar_scanner'
                PROJECT_NAME = "showcase"
            }
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''$SCANNER_HOME/bin/sonar-scanner \
                    -Dsonar.projectKey=$PROJECT_NAME \
                    -Dsonar.sources=.'''
                }
            }
        }
        
        stage('Install/upgrade basic Python scanning tools') {
            steps {
                sh 'python -m pip install --upgrade bandit mypy'
            }
        }

        stage('MyPy scan') {
            steps {
                container('python') {
                    sh "python -m mypy --ignore-missing-imports --exclude 'venv' ."
                }
            }
        }
        
        stage('Bandit scan') {
            steps {
                container('python') {
                    sh 'python -m bandit -r . -lll -ii  --exclude ./venv'
                }
            }
        }
    }

    post {
        always {
            // Mail a success/failure report.
            emailext body: 'Check console output at $BUILD_URL to view the results.\n\n -------------------------------------------------- \n${BUILD_LOG, maxLines=100, escapeHtml=false}', 
                     to: "${EMAIL_REPORT_TO}", 
                     subject: "Build ${currentBuild.currentResult} in Jenkins: ${JOB_NAME} - #${BUILD_NUMBER}"
        }
    }
}



