pipeline {
    agent any

    environment {
        DOCKER_PASS = credentials('docker-hub-password')
        DOCKER_IMAGE = 'amarocket/maas_prometheus_adapter'
        DOCKER_SERVICE = "maas_prometheus_metrics_adapter_service"
        DOCKER_USER = credentials('docker-hub-username')
        LOG_FILE = "/var/log/docker_auto_update.log"
        METRICS_URL = credentials('maas_metrics_url')
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

        stage('Restart Monitoring Stack Services1') {
            steps {
                dir('/opt/monitoring') {
                    script {
                        sh '''
                        echo docker stack monitoring service restart
                        docker stack rm monitoring
                        echo Docker stack service was removed.
                        '''
                    }
                }
            }
        }

        stage('Remove Docker Swarm Service') {
            steps {
                script {
                    sh '''
                        echo "Updating Docker Swarm service..." | tee -a $LOG_FILE
                        echo "Removing the existing Docker Swarm service..." | tee -a $LOG_FILE
                        docker service rm $DOCKER_SERVICE || true
                        sleep 5
                        echo "Waiting for the port to be free..."
                        while netstat -tuln | grep -q ":8001 "; do
                            echo "Port 8001 still in use, waiting..."
                            sleep 2
                        done
                        echo "Port 8001 is now free, continuing..." | tee -a $LOG_FILE
                        '''
                }
            }
        }

        stage('Start Docker Swarm Service') {
            steps {
                script {
                    sh '''
                        echo "Re-creating Docker Swarm service..." | tee -a $LOG_FILE
                        docker service create \
                            --name $DOCKER_SERVICE \
                            --constraint 'node.labels.role == manager' \
                            --network host \
                            -e METRICS_URL=$METRICS_URL \
                            --restart-condition on-failure \
                            --replicas 1 \
                            $DOCKER_IMAGE:latest
                        echo "Docker Swarm service recreated successfully." | tee -a $LOG_FILE
                        '''
                }
            }
        }

        stage('Restart Monitoring Stack Services2') {
            steps {
                dir('/opt/monitoring') {
                    script {
                        sh '''
                        echo docker stack monitoring service restart
                        docker stack deploy -c docker-stack.yml monitoring
                        echo Docker stack service was deployed.
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