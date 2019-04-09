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
                cp /project/sw/ufm/install/UFM6.2.0/x86_64/rhel7/ufm-6.2.0-3.el7.x86_64.tgz /tmp
                """
            }
        }
        stage("extract ufm"){
            steps{
                sh """
                cd /tmp
                tar -xvzf ufm-6.2.0-3.el7.x86_64.tgz
                cd  ufm-6.2.0-3.el7.x86_64
                """
            }
        }
    }

}
