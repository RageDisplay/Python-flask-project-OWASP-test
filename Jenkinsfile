pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "ragedisplay/app-for-owasp-test:flaskwork"
        KUBE_NAMESPACE = "flask-app"
        REGISTRY_CREDENTIALS = "docker-hub-credentials"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/RageDisplay/Python-flask-project-OWASP-test.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        stage('Scan for Vulnerabilities') {
            steps {
                script {
                    sh "trivy image --exit-code 1 --severity CRITICAL ${DOCKER_IMAGE}"
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', REGISTRY_CREDENTIALS) {
                        docker.image("${DOCKER_IMAGE}").push()
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Обновляем конфигурацию deployment в Kubernetes
                    sh """
                        kubectl set image deployment/flask-app-deployment flask-app=${DOCKER_IMAGE} -n ${KUBE_NAMESPACE} --record=true
                        kubectl rollout status deployment/flask-app-deployment -n ${KUBE_NAMESPACE}
                    """
                }
            }
        }
    }
    post {
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline succeeded!'
        }
    }
}
