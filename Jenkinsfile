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
                emailext(
                    subject: "Jenkins Build Failure: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: """
                        <h3>Jenkins Build Failure</h3>
                        <p>The build for job <b>'${env.JOB_NAME}'</b> (Build #${env.BUILD_NUMBER}) has failed.</p>
                        <p>Check the logs for more details: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                        <p>Regards,<br>Jenkins</p>
                    """,
                    to: 'kalash.asati21@st.niituniversity.in',
                    replyTo: 'aniketasa30@gmail.com',
                    mimeType: 'text/html'
                )
            }
        }
        success {
            echo 'Pipeline executed successfully.'
        }
    }
}
