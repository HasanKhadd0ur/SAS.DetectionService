pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/HasanKhadd0ur/SAS.DetectionService.git', branch: 'main'
            }
        }

        stage('Setup Python') {
            steps {
                sh 'python -m venv $VENV_DIR'
                sh '. $VENV_DIR/bin/activate && pip install --upgrade pip && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. $VENV_DIR/bin/activate && pytest tests/'
            }
        }
    }

    post {
        always {
            junit 'tests/**/pytest-report.xml'
        }
    }
}
