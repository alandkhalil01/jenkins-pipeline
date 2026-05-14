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
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    docker run --rm \
                        -v \$(pwd)/test_app.py:/app/test_app.py \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        python -m pytest test_app.py -v
                """
            }
        }

        stage('Deploy') {
            steps {
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
            }
        }

        stage('Health Check') {
            steps {
                sh "sleep 5"
                sh "curl -f http://localhost:5000/health || exit 1"
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline FAILED!"
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