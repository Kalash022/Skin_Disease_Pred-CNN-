pipeline {
    agent any

    environment {
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
                    userRemoteConfigs: [[url: "${GIT_REPO_URL}"]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                // This step forces a failure for testing email functionality
                sh 'exit 1'
            }
        }
    }

    post {
        failure {
            script {
                echo 'Pipeline failed. Sending email notification...'
                emailext body: 'ASDFGHJKL;', replyTo: 'aniketasa30@gmail.com', subject: 'TEST', to: 'kalash.asati21@st.niituniversity.in'
            }
        }
        success {
            echo 'Pipeline executed successfully.'
        }
    }
}
