FROM jenkins/jenkins:lts
ARG DOCKER_GID=118
USER root

# Elimina el grupo docker existente (si existe) y crea uno nuevo con el GID correcto
RUN groupdel docker || true && \
    groupadd -g ${DOCKER_GID} docker && \
    usermod -aG docker jenkins
    
# Instala dependencias básicas, Docker CLI, Helm, Trivy, Node.js y Yarn en una sola capa
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    jq \
    git \
    bash \
    unzip \
    zip \
    wget \
    lsb-release \
    software-properties-common && \
    curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
    https://download.docker.com/linux/debian/gpg && \
    echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
    https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker.io && \
    groupadd -g $DOCKER_GID docker || true && \
    usermod -aG docker jenkins && \
    curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | tee /usr/share/keyrings/helm.gpg > /dev/null && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list && \
    apt-get update && \
    apt-get install -y helm && \
    wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - && \
    echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list && \
    apt-get update && \
    apt-get install -y trivy && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && \
    apt-get install -y yarn && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jenkins
RUN jenkins-plugin-cli \
    --plugins \
    workflow-support \
    pam-auth \
    sshd \
    ws-cleanup \
    ssh-agent \
    docker-workflow \
    pipeline-utility-steps