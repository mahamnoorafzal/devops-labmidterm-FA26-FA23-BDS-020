
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'mahamnoor/devops-labmidterm-fa23-bds-020'
        CONTAINER_NAME = 'midterm-fa23-bds-020'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_SHA = sh(
                        script: 'git rev-parse HEAD',
                        returnStdout: true
                    ).trim()
                }
                echo "Building commit: ${GIT_SHA}"
            }
        }

        stage('Build and Test') {
            steps {
                sh '''
                    docker build \
                      --build-arg GIT_COMMIT=$GIT_SHA \
                      -t $IMAGE_NAME:latest .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login \
                          -u "$DOCKER_USER" --password-stdin
                        docker push $IMAGE_NAME:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy on EC2') {
            steps {
                sh '''
                    docker rm -f $CONTAINER_NAME || true
                    docker run -d \
                      --name $CONTAINER_NAME \
                      --restart unless-stopped \
                      -p 8000:8000 \
                      $IMAGE_NAME:latest

                    for i in $(seq 1 10); do
                      if curl -fsS http://localhost:8000/metrics; then
                        exit 0
                      fi
                      sleep 3
                    done

                    echo "API health verification failed"
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            script {
                try {
                    emailext(
                        to: 'qasimalik@gmail.com',
                        subject: "DevOps Midterm FA23-BDS-020 - SUCCESS",
                        body: "Deployment successful. Commit: ${env.GIT_SHA}\nAPI: http://100.53.182.212:8000/metrics"
                    )
                } catch (err) {
                    echo "Email notification could not be sent: ${err}"
                }
            }
        }

        failure {
            script {
                try {
                    emailext(
                        to: 'qasimalik@gmail.com',
                        subject: "DevOps Midterm FA23-BDS-020 - FAILED",
                        body: "Jenkins build failed. Please check the Jenkins console output."
                    )
                } catch (err) {
                    echo "Failure email could not be sent: ${err}"
                }
            }
        }
    }
}
