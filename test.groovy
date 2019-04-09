#!/usr/bin/env groovy

pipeline {
    options { skipDefaultCheckout() }
    parameters {
        choice(
                choices: "installed-" + env.BRANCH_NAME + "\nufm-svr43\nsmg-ib-svr033\nsmg-ib-svr042",
                description: "Select setup:", 
                name: 'setup')
        choice(
                choices: "RHEL\nSLES",
                description: "Select OS:", 
                name: 'OS')
    }
    agent {
        node {
            label params.setup
            customWorkspace 'workspace/' + JOB_NAME
        }
    }
    stages {
        stage("config") {
            steps {
                script {
                    deleteDir()
                    checkout scm
                    cmd = 'process-template.py'
                    sh """
                    ${cmd} --nic "${params.OS}"
                    """
                }
            }
        }
    }
}
