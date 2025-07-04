pipeline {
    agent any

    environment {
        // Use the credentials ID you set in Jenkins
        GIT_CREDENTIALS = credentials('github-creds')
        DOCKER_IMAGE_NAME = 'muliro1/messaging_app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }

    tools {
        // Explicitly specify Python tool to avoid Java/Maven conflicts
        python 'Python-3.10'
    }

    stages {
        stage('Configure Git') {
            steps {
                // Configure Git to handle network issues
                sh 'git config --global http.postBuffer 524288000'
                sh 'git config --global http.maxRequestBuffer 100M'
                sh 'git config --global core.compression 9'
                sh 'git config --global http.lowSpeedLimit 0'
                sh 'git config --global http.lowSpeedTime 999999'
            }
        }
        stage('Checkout') {
            steps {
                git credentialsId: "${GIT_CREDENTIALS}", url: 'https://github.com/Muliro1/alx-backend-python.git', branch: 'main'
            }
        }
        stage('Show Git Branch') {
            steps {
                sh 'git branch'
            }
        }
        stage('Install dependencies') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'python -m pip install -r messaging_app/requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'cd messaging_app && python -m pytest --junitxml=report.xml'
            }
            post {
                always {
                    junit 'messaging_app/report.xml'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image from the messaging_app directory
                    dockerImage = docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_TAG}", "./messaging_app")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Push to Docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-creds') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean up Docker images to save space
            sh 'docker system prune -f'
        }
        success {
            echo "Docker image ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} built and pushed successfully!"
        }
        failure {
            echo "Pipeline failed! Check the logs for details."
        }
    }
    
    triggers {
        // No triggers for manual only
    }
}