#!/usr/bin/env bash

APPLICATION_NAME="stocknews"
APPLICATION_PATH="/var/www/$APPLICATION_NAME"

WEB_USER="www-data"

FRONTEND_PATH_SUFFIX="/frontend"
FRONTEND_PRODUCTION_PATH_SUFFIX="$FRONTEND_PATH_SUFFIX/production"
BACKEND_PATH_SUFFIX="/backend"

RUN_PATH="/var/run/$APPLICATION_NAME"
LOG_PATH="/var/log/$APPLICATION_NAME"

PYTHON_ENV_PATH="/var/www/.python_env/$APPLICATION_NAME"

KILL="kill -9"
RM="rm -rf"
MKDIR="mkdir -p"
CHOWN="chown -R"
PM2="pm2"
