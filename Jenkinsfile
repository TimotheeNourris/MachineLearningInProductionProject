pipeline {
    agent any 
    stages {
	stage('Checkout') {
	    steps {
		bat "git checkout Aury"
                bat "git fetch origin"
		bat "git merge origin/Aury"
	    }
	}
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
                bat 'docker login -u auryble -p dckr_pat_zJAgdboJZq0En6669fSf72QOZW0'
                bat 'docker tag jenkinsdocker auryble/pj_mlops_repo'
                bat 'docker push auryble/pj_mlops_repo'
            }
        }       
    }    
    triggers {
        githubPush()
    }
}
