#!/usr/bin/env groovy

pipeline {
    options { skipDefaultCheckout() }
    parameters {
        choice(
                choices: "installed-" + env.BRANCH_NAME + "\nufm-svr43\nsmg-ib-svr033\nsmg-ib-svr042",
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
        stage("copy ufm") {
            steps {
                checkout scm
                sh """
                echo "test"
                """
            }
        }
        stage("extract ufm"){
            steps{
                sh """
                echo "test"
                """
            }
        }
    }

}
