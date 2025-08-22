pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "ragedisplay/app-for-owasp-test:flaskwork"
        KUBE_NAMESPACE = "flask-app"
        REGISTRY_CREDENTIALS = credentials('docker-hub-credentials')
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
        stage('Trivy Security Scan') {
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
                    // Обновляем образ в Kubernetes
                    sh """
                        kubectl set image deployment/flask-app flask-app=${DOCKER_IMAGE} -n ${KUBE_NAMESPACE} --record
                        kubectl rollout status deployment/flask-app -n ${KUBE_NAMESPACE}
                    """
                }
            }
        }
    }
    post {
        failure {
            emailext body: "Сборка ${env.BUILD_URL} завершилась с ошибкой", subject: "FAILED: ${env.JOB_NAME}", to: "dev@example.com"
        }
    }
}
