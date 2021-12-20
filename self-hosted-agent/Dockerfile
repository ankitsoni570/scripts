FROM ubuntu:18.04

# First installing Python 3.9
COPY scripts /scripts
COPY requirements.txt ./
ENV AGENT_TOOLSDIRECTORY=/_work/_tool

RUN apt-get update -y  && apt-get install -y  make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libsqlite3-dev \
    unixodbc-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libreadline-dev \
    libffi-dev \
    wget

RUN chmod 777 /scripts/*.sh /requirements.txt && \
    /scripts/python_from_source.sh "3.9.0"

# Extracting Agent on the machine
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    jq \
    git \
    iputils-ping \
    libcurl4 \
    libicu60 \
    libunwind8 \
    netcat \
    libssl1.0 \
    tar \
  && rm -rf /var/lib/apt/lists/*


RUN curl -LsS https://aka.ms/InstallAzureCLIDeb | bash \
  && rm -rf /var/lib/apt/lists/*

ARG TARGETARCH=amd64
ARG AGENT_VERSION=2.185.1

WORKDIR /azp
RUN if [ "$TARGETARCH" = "amd64" ]; then \
      AZP_AGENTPACKAGE_URL=https://vstsagentpackage.azureedge.net/agent/${AGENT_VERSION}/vsts-agent-linux-x64-${AGENT_VERSION}.tar.gz; \
    else \
      AZP_AGENTPACKAGE_URL=https://vstsagentpackage.azureedge.net/agent/${AGENT_VERSION}/vsts-agent-linux-${TARGETARCH}-${AGENT_VERSION}.tar.gz; \
    fi; \
    curl -LsS "$AZP_AGENTPACKAGE_URL" | tar -xz
                                                   
COPY ./start.sh .
RUN chmod +x start.sh

ENTRYPOINT [ "./start.sh" ]