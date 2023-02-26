pipeline {
    agent any 
    stages {
        stage('Build part') {
            steps {
                bat 'echo build start'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Test part') {
            steps {       
                bat 'echo test start'
                bat 'python -m unittest'
            }
        }
        stage('Deploy part') {
            steps {
                bat 'docker build -t jenkinsdocker .'
                bat 'docker run -d -p 5000:5000 jenkinsdocker'
                bat 'docker login -u timotheenourriscli -p dckr_pat_liPCBB7KmZ3x_UHNbz9oyMTNpiE'
                bat 'docker tag jenkinsdocker timotheenourriscli/jenkins_docker'
                bat 'docker push timotheenourriscli/jenkins_docker'
            }
        }       
    }    
    triggers {
        githubPush()
    }
}
