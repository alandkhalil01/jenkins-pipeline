pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo "Starting Build stage..."
                sh "echo 'Compiling application...'"
                sh "touch app.jar"
                sh "ls -la"
                echo "Build stage complete."
            }
        }
        stage('Test') {
            steps {
                echo "Starting Test stage..."
                sh "pwd"
                sh "echo 'Running unit tests...'"
                sh "touch test-results.xml"
                sh "ls -la"
                echo "Test stage complete - all tests passed."
            }
        }
        stage('Deploy') {
            steps {
                echo "Starting Deploy stage..."
                sh "mkdir -p deploy"
                sh "mv app.jar deploy/"
                sh "mv test-results.xml deploy/"
                sh "ls -la deploy/"
                echo "Deploy stage complete - application deployed successfully."
            }
        }
    }
    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}