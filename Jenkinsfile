pipeline {
    agent any  // This allows the pipeline to run on any available agent

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/Kalash022/Skin_Disease_Pred-CNN-.git', branch: 'main'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t skin-disease-backend:latest .'
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker stop skin-disease-container || true'
                    sh 'docker rm skin-disease-container || true'
                    
                    sh 'docker run -d --name skin-disease-container -p 5000:5000 skin-disease-backend:latest'
                }
            }
        }
    }
}
