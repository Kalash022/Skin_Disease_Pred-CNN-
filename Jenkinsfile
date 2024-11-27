pipeline {
    agent any

    stages {
        stage('Send Test Email') {
            steps {
                emailext(
                    subject: "Test Email from Jenkins",
                    body: "This is a test email to verify the email configuration.",
                    to: 'kalash.asati21@st.niituniversity.in',
                    replyTo: 'aniketasa30@gmail.com',
                    mimeType: 'text/html'
                )
            }
        }
    }
}
