FROM python:3.13-bookworm

ARG UID=1000
ARG GID=1000

RUN \
    apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get install -y -q \
    build-essential \
    libsasl2-dev \
    libldap2-dev \
    gettext \
    # Instala a dependência para o wait-for
    netcat-openbsd &&\
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# uv para gerenciar as dependências (pyproject.toml / uv.lock)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN groupadd -r -g "${GID}" helios && useradd -r -g "${GID}" -u "${UID}" helios

# instalação dos pacotes necessários em /opt/venv, fora do volume com o
# código fonte (montado em /var/www/helios-server pelo docker-compose)
COPY pyproject.toml uv.lock /tmp/helios-deps/
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN cd /tmp/helios-deps && \
    uv sync --frozen --no-install-project --no-dev && \
    rm -rf /tmp/helios-deps


WORKDIR /var/www/helios-server
RUN chown helios:helios /var/www/helios-server
COPY --chown=helios  ./docker/app/docker-entrypoint.sh ./docker/app/start-celeryworker ./docker/app/start-celerybeat ./docker/app/start /
RUN  chmod +x /docker-entrypoint.sh /start-celerybeat /start-celeryworker /start

USER helios

ENTRYPOINT ["/docker-entrypoint.sh"]
