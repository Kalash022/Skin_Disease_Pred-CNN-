pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository (handled automatically in a multibranch pipeline)
                git url: 'https://github.com/Kalash022/Skin_Disease_Pred-CNN-.git', branch: 'main'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    def app = docker.build("skin-disease-backend:latest")
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    // Clean up old container if it exists
                    sh "docker stop skin-disease-container || true"
                    sh "docker rm skin-disease-container || true"
                    
                    // Run the new Docker container
                    app.run("-d --name skin-disease-container -p 5000:5000")
                }
            }
        }
    }
}
