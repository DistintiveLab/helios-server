# Helios Server Installation

## Prerequisites

* Install PostgreSQL 12+

* Install Redis
  This is needed as the Celery broker. Celery does background processing such as
  the processing of uploaded list-of-voter CSV files and sending voter emails.
  Default broker URL is `redis://127.0.0.1:6379` (override with `CELERY_BROKER_URL`).

* Download helios-server

* `cd` into the helios-server directory

## Python Setup

* Install Python 3.13 including dev packages

```
sudo apt install python3 python3-dev
```

* Install uv (modern Python package manager)

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

* You'll also need Postgres dev libraries. For example on Ubuntu:

```
sudo apt install libpq-dev
```

* Install dependencies (uv creates a virtual environment automatically)

```
uv sync
```

Note: `python-ldap` builds from source; you need `libsasl2-dev` and
`libldap2-dev` (plus `build-essential`) installed first.

## Database Setup

Configure the connection via environment variables (see `.env.sample`):
`POSTGRES_HOST`, `POSTGRES_PORT`, `DB_NAME`, `DB_USER`, `DB_PWD`. Alternatively,
set `DATABASE_URL` to override the whole block (this also forces SSL).

Then apply migrations (a fresh deploy only needs this — `reset.sh` is a
destructive, dev-only helper that drops and recreates the database):

```
uv run python manage.py migrate
uv run python manage.py collectstatic
```

## Compiling the pt-BR translations

```
uv run python manage.py compilemessages -l pt_BR
```

## Running the Server

* Start server

```
uv run python manage.py runserver
```

* Start Celery worker (separate terminal; Redis must be reachable)

```
uv run celery --app helios worker -l info
```

## Google Auth Configuration

To get Google Auth working:

* Go to https://console.developers.google.com

* Create an application

* Set up OAuth2 credentials as a web application, with your origin, e.g. `https://myhelios.example.com`, and your auth callback, which based on our example is `https://myhelios.example.com/auth/after/`

* In the developer console, enable the Google People API

* Set the `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` configuration variables accordingly

## Discourse Connect Auth Configuration

Helios can use a Discourse forum as a login provider via Discourse Connect
(SSO). The implementation lives in `helios_auth/auth_systems/discourse.py`.

* In Discourse admin settings, enable the **Discourse Connect provider** and set
  the **discourse connect provider secrets** to `your-helios-host:shared-secret`
  (a bare secret with no host is also accepted)

* Configure via environment variables (read in `settings.py` with
  `get_from_env`; see `.env.sample`):

```
DISCOURSE_URL=https://your-forum.example.org
DISCOURSE_SECRET=shared-secret
```

* Make sure `discourse` is listed in `AUTH_ENABLED_AUTH_SYSTEMS` (it is part of
  the default list). Users are identified by their Discourse `username`; the
  e-mail used is the one registered in the forum.

## LDAP Auth Configuration

This fork ships a LDAP auth module (`django-auth-ldap`). Key settings:
`AUTH_LDAP_SERVER_URI`, `AUTH_LDAP_BIND_DN`, `AUTH_LDAP_BIND_PASSWORD` and
`AUTH_LDAP_USER_SEARCH`. Enable the module with
`AUTH_ENABLED_AUTH_SYSTEMS=ldap`.
