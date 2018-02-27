node() {
    def image = null
    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        image = docker.build("qasimodo-bot:${env.BUILD_ID}")
    }

    stage('Deploy'){
        try{
            sh 'docker stop qasimodo-bot && docker rm qasimodo-bot'
        }catch(Exception e){
            echo e.getMessage()
        }

        withCredentials([string(credentialsId: 'qasimodo-slack-token', variable: 'token')]) {
            withCredentials([string(credentialsId: 'witai-qasimodo-token', variable: 'wit_token')]) {
                def runArgs = '\
-e "BOT_TOKEN=$token" \
-e "WITAI_QASIMODO_TOKEN=$wit_token" \
--name qasimodo-bot'

                def container = image.run(runArgs)
            }
        }
    }
}