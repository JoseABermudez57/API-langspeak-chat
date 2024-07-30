pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'lang-speak-chats-service-prod-deploy'
        NAME_PROJECT = 'API-langspeak-chat'
        PORT = '8083:8083'
        DOCKER_IMAGE_TAG = "${DOCKER_IMAGE}:latest"
        REMOTE_USER = "ubuntu"
        REMOTE_HOST = "44.199.36.163"
//         EMAIL_ADDRESS = "213376@ids.upchiapas.edu.mx"
        SSH_CREDENTIALS_ID = "ssh-credentials-lang-speak-chats-prod-ec2"
        REPO_URL = "https://github.com/JoseABermudez57/${NAME_PROJECT}.git"
        REPO_DIR = "/home/ubuntu/${NAME_PROJECT}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Pre-build') {
            steps {
                script {
                    sshagent(credentials: ["${env.SSH_CREDENTIALS_ID}"]) {
                        def repoExists = sh(script: "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'test -d ${env.REPO_DIR}'", returnStatus: true) == 0
                        if (repoExists) {
                            sh "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'cd ${env.REPO_DIR} && git pull origin main'"
                        } else {
                            sh "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'git clone ${env.REPO_URL} ${env.REPO_DIR}'"
                        }
                        withCredentials([file(credentialsId: 'env_chats', variable: 'ENV_CHATS')]) {
                            script {
                                sh "chmod -R 755 ${WORKSPACE}"
                                sh "cp ${ENV_CHATS} ${WORKSPACE}"
//                                 sh 'chmod 644 ${WORKSPACE}/.env'
//                                 sh "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'cp ${WORKSPACE}/${ENV_SENTIMENT_ANALYZER} ${REPO_DIR}'"
                                sh "scp -o StrictHostKeyChecking=no ${WORKSPACE}/.env ${env.REMOTE_USER}@${env.REMOTE_HOST}:${REPO_DIR}/"
                            }
                        }
                        def imageExists = sh(script: "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'docker images -q ${env.DOCKER_IMAGE_TAG}'", returnStatus: true) == 0
                        if (imageExists) {
                            def containerRunning = sh(script: "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'docker ps -q -f name=${env.DOCKER_IMAGE}'", returnStatus: true) == 0
                            def containerExists = sh(script: "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'docker ps -a -q -f name=${env.DOCKER_IMAGE}'", returnStatus: true) == 0
                            if (containerRunning) {
                                sh "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'docker stop ${env.DOCKER_IMAGE} || true && docker rm ${env.DOCKER_IMAGE} || true && docker rmi ${env.DOCKER_IMAGE_TAG} || true'"
                            } else if (containerExists) {
                                sh "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'docker rm ${env.DOCKER_IMAGE} || true && docker rmi ${env.DOCKER_IMAGE_TAG} || true'"
                            } else {
                                sh "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'docker rmi ${env.DOCKER_IMAGE_TAG} || true'"
                            }
                        }
                    }
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    sshagent(credentials: ["${env.SSH_CREDENTIALS_ID}"]) {
                        sh "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'cd ${env.REPO_DIR} && docker build -f Dockerfile -t ${env.DOCKER_IMAGE_TAG} .'"
                    }
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    echo 'Testing...'
                }
            }
        }
        stage('Pre-deploy') {
            steps {
                script {
                    sshagent(credentials: ["${env.SSH_CREDENTIALS_ID}"]) {
                        sh "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'docker stop ${env.DOCKER_IMAGE} || true && docker rm ${env.DOCKER_IMAGE} || true'"
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    sshagent(credentials: ["${env.SSH_CREDENTIALS_ID}"]) {
                        sh "ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} 'docker run --name ${env.DOCKER_IMAGE} -d -p ${env.PORT} ${env.DOCKER_IMAGE_TAG}'"
                    }
                }
            }
        }
    }
//     post {
//         success {
//             mail to: "${env.EMAIL_ADDRESS}",
//                  subject: "Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
//                  body: "Good news! The build ${env.BUILD_NUMBER} was successful."
//         }
//         failure {
//             mail to: "${env.EMAIL_ADDRESS}",
//                  subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
//                  body: "The build ${env.BUILD_NUMBER} failed. Please check the logs for details."
//         }
//     }
}
