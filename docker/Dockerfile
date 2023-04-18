FROM python:3.6.15-buster as djangobase

ARG UID=1000
ARG GID=1000

RUN \
    apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get install -y -q \
    python3-dev \
    libsasl2-dev \
    libldap2-dev \
    gettext \
    # Instala a dependência para o wait-for
    netcat &&\
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

RUN groupadd -r -g "${GID}" helios && useradd -r -g "${GID}" -u "${UID}" helios

# instalação dos pacotes necessários
COPY requirements.txt /tmp/pip-tmp/
ENV PATH="/opt/venv/bin:$PATH"
RUN python3 -m venv  /opt/venv
RUN pip install --no-compile --no-cache-dir -r /tmp/pip-tmp/requirements.txt


WORKDIR /var/www/helios-server
RUN chown helios:helios /var/www/helios-server
COPY --chown=helios  ./docker/docker-entrypoint.sh ./docker/start-celeryworker ./docker/start-celerybeat ./docker/start /
RUN  chmod +x /docker-entrypoint.sh /start-celerybeat /start-celeryworker /start

USER helios

ENTRYPOINT ["/docker-entrypoint.sh"]
