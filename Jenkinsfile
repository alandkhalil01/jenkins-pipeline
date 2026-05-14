pipeline {
    agent any

    environment {
        APP_NAME = 'jenkins-pipeline-app'
        DOCKER_IMAGE = 'jenkins-pipeline-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "=== Checking out source code ==="
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "=== Building Docker Image ==="
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
                echo "Docker image built successfully: ${DOCKER_IMAGE}:${DOCKER_TAG}"
            }
        }

        stage('Run Tests') {
            steps {
                echo "=== Running Tests ==="
                sh """
                    docker run --rm \
                        -v \$(pwd)/test_app.py:/app/test_app.py \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        python -m pytest test_app.py -v
                """
                echo "All tests passed!"
            }
        }

        stage('Deploy') {
            steps {
                echo "=== Deploying Application ==="
                sh """
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                """
                sh """
                    docker run -d \
                        --name ${APP_NAME} \
                        -p 5000:5000 \
                        --restart unless-stopped \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                """
                echo "Application deployed successfully!"
            }
        }

        stage('Health Check') {
            steps {
                echo "=== Running Health Check ==="
                sh "sleep 5"
                sh "curl -f http://localhost:5000/health || exit 1"
                echo "Health check passed - application is running!"
            }
        }
    }

    post {
        success {
            echo """
            =========================================
            Pipeline completed successfully!
            App: ${APP_NAME}
            Image: ${DOCKER_IMAGE}:${DOCKER_TAG}
            Status: DEPLOYED & HEALTHY
            =========================================
            """
        }
        failure {
            echo """
            =========================================
            Pipeline FAILED!
            Please check the logs above for errors.
            =========================================
            """
            sh "docker stop ${APP_NAME} || true"
            sh "docker rm ${APP_NAME} || true"
        }
        always {
            sh """
                docker images ${DOCKER_IMAGE} --format '{{.Tag}}' | \
                sort -rn | tail -n +4 | \
                xargs -I {} docker rmi ${DOCKER_IMAGE}:{} || true
            """
        }
    }
}