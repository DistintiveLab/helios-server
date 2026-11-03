Notes on errors faced during installation/configuration

First, read the instructions at INSTALL.md and README.md !

* Build dependencies for python-ldap (the LDAP auth module) and other
  packages that compile from source:

```bash
sudo apt install build-essential python3-dev libsasl2-dev libldap2-dev gettext
```

With uv, all Python dependencies are then installed with:

```bash
uv sync
```

* Database connection errors ("could not translate host name db", "Peer
  authentication failed"): the defaults in `settings.py` point at the
  docker-compose host `db`. On a direct server install set the environment
  variables `POSTGRES_HOST`, `DB_USER`, `DB_PWD`, `DB_NAME` (see `.env.sample`),
  or set `DATABASE_URL` to override the whole block (forces SSL).

* Vote hash was not saving / voter e-mails were not sent: the Celery worker
  was not running. Celery (5.x) uses Redis as its broker
  (default `redis://127.0.0.1:6379`, override with `CELERY_BROKER_URL`).
  Run in a separate terminal:

```bash
uv run celery --app helios worker -l info
```

* `module object has no attribute STATUS_UPDATES`: your auth module needs to
  declare `STATUS_UPDATES` (see `helios_auth/auth_systems/*.py` for examples).

* Discourse Connect login failing: check that `DISCOURSE_URL` and
  `DISCOURSE_SECRET` in `settings.py` match the Discourse Connect provider
  settings on the forum side (same shared secret), and that the forum is
  reachable from the Helios server.
