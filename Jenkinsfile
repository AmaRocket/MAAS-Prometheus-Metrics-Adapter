pipeline {
    agent any

    environment {
        DOCKER_PASS = credentials('docker-hub-password')
        DOCKER_IMAGE = 'amarocket/maas_prometheus_adapter'
        DOCKER_SERVICE = "maas_prometheus_metrics_adapter_service"
        DOCKER_USER = credentials('docker-hub-username')
        LOG_FILE = "/var/log/docker_auto_update.log"
    }

    stages {
        stage('Clone Repository') {
            steps {
                dir('/var/lib/jenkins/workspace/MAAS_Prometheus_Adapter/') {
                    script {
                        if (fileExists('.git')) {
                            sh 'git stash || true'
                            sh 'git pull origin main'
                        } else {
                            git branch: 'main', url: 'https://github.com/AmaRocket/MAAS-Prometheus-Metrics-Adapter.git'
                        }
                    }
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                dir('/var/lib/jenkins/workspace/MAAS_Prometheus_Adapter/') {
                    script {
                        sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker build --no-cache -t $DOCKER_IMAGE:latest .
                        docker push $DOCKER_IMAGE:latest
                        echo $DOCKER_IMAGE was deployed.
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Deployment failed.'
        }
    }
}