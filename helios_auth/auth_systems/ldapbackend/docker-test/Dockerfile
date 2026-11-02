FROM --platform=$BUILDPLATFORM python:3.6.15-buster AS base

# for python-ldap==3.4.3 in requirements
RUN apt-get -y update -y \
    && apt-get -y install python3-dev libldap2-dev libsasl2-dev \
    # Remove arquivos temporários
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* /tmp/*

EXPOSE 8000
WORKDIR /usr/src/app 
COPY ../../../../requirements.txt /usr/src/app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
