pipeline {
    agent any

    stages {
        stage('Debug Email') {
            steps {
                script {
                    try {
                        emailext(
                            subject: "Test Email from Jenkins Pipeline",
                            body: "This is a debug test email from the pipeline.",
                            to: 'kalash.asati21@st.niituniversity.in',
                            replyTo: 'aniketasa30@gmail.com',
                            mimeType: 'text/plain'
                        )
                        echo "Email sent successfully."
                    } catch (Exception e) {
                        echo "Failed to send email: ${e.message}"
                    }
                }
            }
        }
    }
}
