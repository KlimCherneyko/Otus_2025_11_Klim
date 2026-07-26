pipeline {
    agent any

    parameters {
        string(
            name: 'SELENOID_URL',
            defaultValue: 'http://selenoid:4444/wd/hub',
            description: 'Адрес executor (Selenoid)'
        )
        string(
            name: 'OPENCART_URL',
            defaultValue: 'http://127.0.0.1:8080',
            description: 'Адрес приложения OpenCart (используй LAN IP хоста, не localhost, если браузер в Selenoid)'
        )
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox'],
            description: 'Браузер'
        )
        string(
            name: 'BROWSER_VERSION',
            defaultValue: '120.0',
            description: 'Версия браузера'
        )
        string(
            name: 'THREADS',
            defaultValue: '2',
            description: 'Количество потоков pytest-xdist (-n)'
        )
    }

    environment {
        OPENCART_ADMIN_USER = 'user'
        OPENCART_ADMIN_PASSWORD = 'bitnami'
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                dir('dz') {
                    sh '''
                        set -e
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                dir('dz') {
                    sh """
                        set -e
                        . .venv/bin/activate
                        python -m pytest -c pytest.ini tests/selenium_tests \
                          --executor selenoid \
                          --selenoid-url '${params.SELENOID_URL}' \
                          --opencart-url '${params.OPENCART_URL}' \
                          --selenium-browser '${params.BROWSER}' \
                          --browser_version '${params.BROWSER_VERSION}' \
                          -n '${params.THREADS}'
                    """
                }
            }
        }
    }

    post {
        always {
            dir('dz') {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }
}
