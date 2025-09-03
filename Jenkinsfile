pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "ragedisplay/app-for-owasp-test"
        KUBE_NAMESPACE = "default"
        REGISTRY_CREDENTIALS = "docker-hub-credentials"
        K8S_MANIFEST = "kubernetes/app.yaml"
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
                    def customTag = "flaskwork-${env.BUILD_NUMBER}"
                    env.IMAGE_TAG = customTag
                    docker.build("${DOCKER_IMAGE}:${customTag}")
                }
            }
        }
        stage('Scan for Vulnerabilities') {
            steps {
                script {
                    sh "trivy image --exit-code 1 --severity CRITICAL ${DOCKER_IMAGE}:${env.IMAGE_TAG}"
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', REGISTRY_CREDENTIALS) {
                        docker.image("${DOCKER_IMAGE}:${env.IMAGE_TAG}").push()
                    }
                }
            }
        }
        stage('Prepare Manifest') {
            steps {
                script {
                    sh """
                        sed -i 's/FLASKWORK_TAG/${env.IMAGE_TAG}/g' ${K8S_MANIFEST}
                    """
                    archiveArtifacts artifacts: "${K8S_MANIFEST}", fingerprint: true
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh "kubectl apply -f ${K8S_MANIFEST} -n ${KUBE_NAMESPACE}"

                    sh "kubectl rollout status deployment/myapp-test -n ${KUBE_NAMESPACE}"

                    sh "kubectl get pods -n ${KUBE_NAMESPACE} -l app=myapp-test"
                }
            }
        }
    }
    post {
        always {
            sh "git checkout -- ${K8S_MANIFEST}"
        }
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline succeeded!'
        }
    }
}
