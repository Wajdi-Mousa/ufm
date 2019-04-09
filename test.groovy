#!/usr/bin/env groovy

pipeline {
    options { skipDefaultCheckout() }
    parameters {
        choice(
                choices: "installed-" + env.BRANCH_NAME + "\nufm-svr43\nsmg-ib-svr033",
                description: "Select setup:",
name: 'setup')
    }
    agent {
        node {
            label params.setup
            customWorkspace 'workspace/' + JOB_NAME
        }
}
stages {
        stage("test") {
            steps {
                sh """
                echo "wajdi Mousa"
                """
}
        }

}
