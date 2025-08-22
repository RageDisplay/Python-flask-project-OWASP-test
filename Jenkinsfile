pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "ragedisplay/app-for-owasp-test:${env.BUILD_NUMBER}"
        KUBE_NAMESPACE = "production"
        DOCKER_REGISTRY = "docker.io"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/RageDisplay/Python-flask-project-OWASP-test.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        stage('Security Scan') {
            steps {
                script {
                    // Сканирование на уязвимости
                    def scanResult = sh(script: "trivy image --severity HIGH,CRITICAL --exit-code 0 --format json ${DOCKER_IMAGE}", returnStdout: true).trim()
                    def scanData = readJSON text: scanResult
                    
                    // Анализ результатов
                    def criticalVulns = scanData.Results?.findAll { result ->
                        result.Vulnerabilities?.any { vuln -> vuln.Severity == "CRITICAL" }
                    }?.size() ?: 0
                    
                    def highVulns = scanData.Results?.findAll { result ->
                        result.Vulnerabilities?.any { vuln -> vuln.Severity == "HIGH" }
                    }?.size() ?: 0
                    
                    if (criticalVulns > 0) {
                        error "Обнаружены критические уязвимости! Сборка прервана."
                    }
                    
                    if (highVulns > 0) {
                        // Можно настроить опционально - прерывать или только предупреждать
                        echo "ВНИМАНИЕ: Обнаружены уязвимости уровня HIGH"
                        // error "Обнаружены уязвимости уровня HIGH! Сборка прервана."
                    }
                }
            }
        }
        stage('Push to Registry') {
            when {
                expression { 
                    // Пуш только если сканирование прошло успешно
                    return currentBuild.result == null || currentBuild.result == 'SUCCESS' 
                }
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}"
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            when {
                expression { 
                    return currentBuild.result == null || currentBuild.result == 'SUCCESS' 
                }
            }
            steps {
                script {
                    // Обновляем конфигурацию deployment
                    sh """
                        kubectl set image deployment/owasp-app-deployment \
                        owasp-app=${DOCKER_IMAGE} -n ${KUBE_NAMESPACE} || \
                        kubectl apply -f kubernetes/deployment.yaml
                    """
                    
                    // Проверяем статус развертывания
                    sh "kubectl rollout status deployment/owasp-app-deployment -n ${KUBE_NAMESPACE} --timeout=300s"
                }
            }
        }
        stage('Advanced Security Scan') {
    steps {
        script {
            // Сканирование зависимостей приложения
            sh "trivy fs . --severity HIGH,CRITICAL --exit-code 0 --format json > dependency-scan.json"
            
            // Сканирование конфигурации Dockerfile
            sh "trivy config . --severity HIGH,CRITICAL --exit-code 0 --format json > config-scan.json"
            
            // Анализ результатов
            def depScan = readJSON file: 'dependency-scan.json'
            def configScan = readJSON file: 'config-scan.json'
            
            // Проверка на критические уязвимости
            def criticalIssues = depScan.Results.findAll { result ->
                result.Vulnerabilities.any { vuln -> vuln.Severity == "CRITICAL" }
            }.size() + configScan.Results.findAll { result ->
                result.Vulnerabilities.any { vuln -> vuln.Severity == "CRITICAL" }
            }.size()
            
            if (criticalIssues > 0) {
                error "Обнаружены критические уязвимости в зависимостях или конфигурации!"
            }
        }
    }
}
    }
    post {
        failure {
            slackSend channel: '#ci-cd-alerts',
                      message: "Сборка ${currentBuild.fullDisplayName} завершилась с ошибкой."
        }
        success {
            slackSend channel: '#ci-cd-alerts',
                      message: "Сборка ${currentBuild.fullDisplayName} успешно завершена и развернута в production."
        }
    }
}
