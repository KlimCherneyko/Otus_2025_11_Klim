FROM jenkins/jenkins:lts-jdk17

USER root

ARG ALLURE_VERSION=2.32.2

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        chromium \
        chromium-driver \
        curl \
        ca-certificates \
        unzip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /tmp/allure.tgz \
      "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz" \
    && tar -xzf /tmp/allure.tgz -C /opt \
    && ln -s "/opt/allure-${ALLURE_VERSION}" /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/local/bin/allure \
    && rm /tmp/allure.tgz

ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

USER jenkins

COPY --chown=jenkins:jenkins plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

COPY --chown=jenkins:jenkins init.groovy.d/ /usr/share/jenkins/ref/init.groovy.d/
