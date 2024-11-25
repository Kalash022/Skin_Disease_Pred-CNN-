pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'kalash022/skin_disease_pred_cnn'
        GIT_CREDENTIALS_ID = 'github-credentials-id'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials-id'
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

        stage('Push Docker Image to DockerHub') {
            steps {
                echo 'Pushing Docker image to DockerHub...'
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh """
                            echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                            docker push ${DOCKER_IMAGE}:latest
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully. Docker image pushed to DockerHub.'
        }
        failure {
            echo 'Pipeline failed. Check the logs for errors.'
        }
    }
}
