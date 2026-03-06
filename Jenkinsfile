pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.11'
        ALLURE_RESULTS = 'reports/allure-results'
        ALLURE_REPORT = 'reports/allure-report'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        ansiColor('xterm')
    }

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['lower', 'preprod', 'prod'],
            description: 'Target environment'
        )
        choice(
            name: 'TEST_SCOPE',
            choices: ['smoke', 'api', 'ui', 'all'],
            description: 'Test scope to run'
        )
        booleanParam(
            name: 'OPEN_REPORT',
            defaultValue: false,
            description: 'Open Allure report after tests (for local Jenkins)'
        )
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker build -t lead-manager-qa:${BUILD_NUMBER} .
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def testArg = params.TEST_SCOPE == 'all' ? '' : "--${params.TEST_SCOPE}"
                    sh """
                        docker run --rm \
                            -v \$(pwd)/reports:/app/reports \
                            -e ENV=${params.ENVIRONMENT} \
                            lead-manager-qa:${BUILD_NUMBER} \
                            ./run.sh ${testArg} --env=${params.ENVIRONMENT}
                    """
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    // Find the latest run directory
                    def latestRun = sh(
                        script: "ls -d reports/run_* 2>/dev/null | sort | tail -1",
                        returnStdout: true
                    ).trim()
                    
                    if (latestRun) {
                        sh """
                            allure generate ${latestRun}/allure-results \
                                --clean -o ${latestRun}/allure-report
                        """
                        
                        // Archive for Jenkins Allure plugin
                        sh "cp -r ${latestRun}/allure-results/* ${ALLURE_RESULTS}/ || true"
                    }
                }
            }
        }
    }

    post {
        always {
            // Publish Allure report to Jenkins
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: '${ALLURE_RESULTS}']]
            ])

            // Archive artifacts
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            
            // Publish HTML report
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: '**/report.html',
                reportName: 'Test Reports'
            ])
        }

        success {
            echo '✅ All tests passed!'
        }

        failure {
            echo '❌ Tests failed. Check Allure report for details.'
        }
    }
}
