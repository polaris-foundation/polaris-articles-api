#!/usr/bin/env bash
SERVER_PORT=${1-5000}
export SERVER_PORT=${SERVER_PORT}
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_USER=gdm-articles-api
export DATABASE_PASSWORD=gdm-articles-api
export DATABASE_NAME=gdm-articles-api
export FLASK_APP=gdm_articles_api/autoapp.py
export ENVIRONMENT=DEVELOPMENT
export ALLOW_DROP_DATA=true
export GDM_ARTICLES_WWW=http://localhost:${SERVER_PORT}
export LOG_LEVEL=${LOG_LEVEL:-DEBUG}
export LOG_FORMAT=${LOG_FORMAT:-COLOUR}

if [ -z "$*" ]
then
  flask db upgrade
  python -m gdm_articles_api
else
  flask $*
fi
