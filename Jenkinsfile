pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'kalash022/skin_disease_pred_cnn'
        GIT_CREDENTIALS_ID = 'github-credentials-id'
        GIT_REPO_URL = 'https://github.com/Kalash022/Skin_Disease_Pred-CNN-.git'
        BRANCH_NAME = 'main'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning the repository...'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${BRANCH_NAME}"]],
                    userRemoteConfigs: [[url: "${GIT_REPO_URL}", credentialsId: "${GIT_CREDENTIALS_ID}"]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully. Docker image built locally.'
        }
        failure {
            echo 'Pipeline failed. Sending email notification...'
            script {
                emailext(
                    subject: "Jenkins Build Failure: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        Hi,

                        The Jenkins build for the job '${env.JOB_NAME}' (#${env.BUILD_NUMBER}) has failed.
                        
                        Check the logs for more details: ${env.BUILD_URL}

                        Regards,
                        Jenkins
                    """,
                    to: 'kalash.asati21@st.niituniversity.in'
                )
            }
        }
    }
}
