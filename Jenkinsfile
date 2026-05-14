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

        stage('Trivy Filesystem Scan') {
            steps {
                sh "trivy fs --format table -o trivy-fs-report.txt ."
                archiveArtifacts artifacts: 'trivy-fs-report.txt', allowEmptyArchive: true
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh "trivy image --format table -o trivy-image-report.txt ${DOCKER_IMAGE}:${DOCKER_TAG}"
                archiveArtifacts artifacts: 'trivy-image-report.txt', allowEmptyArchive: true
            }
        }

        stage('Gate Image Scan') {
            steps {
                input message: 'Review the Trivy image scan results. Proceed with deployment?', ok: 'Approve'
            }
        }

        stage('Unit Test') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh """
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements-test.txt
                        python -m pytest test_app.py -v
                    """
                }
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

        stage('Manual Check') {
            steps {
                sh "sleep 5"
                sh "curl -f http://localhost:5000/ || exit 1"
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