#!/bin/bash
# DESTRUCTIVE, dev-only: drops and recreates the local `helios` database.
# NEVER run this on a server with real data; a fresh deploy only needs
# `python manage.py migrate`.
# Note: dropdb/createdb connect via the local socket with your shell user,
# while the Django steps honor POSTGRES_HOST/DB_USER/... env vars
# (settings.py defaults the host to the docker-compose name "db").
set -e  # Exit immediately if a command exits with a non-zero status.
dropdb helios
createdb helios
python manage.py makemigrations
python manage.py migrate
#echo "from helios_auth.models import User; User.objects.create(user_type='google',user_id='shirlei@gmail.com', info={'name':'Shirlei Chaves'})" | python manage.py shell
