#!/usr/bin/env bash

WEB_USER="www-data"

APPLICATION_PATH="/var/www/stocknews"

FRONTEND_PATH_SUFFIX="/frontend"
FRONTEND_PRODUCTION_PATH_SUFFIX="$FRONTEND_PATH_SUFFIX/production"
BACKEND_PATH_SUFFIX="/backend"

PID_PATH="/var/run/stocknews"
LOG_PATH="/var/log/stocknews"

PYTHON_ENV_PATH="/var/www/.python_env/stocknews"

KILL="kill -9"
RM="rm -rf"
MKDIR="mkdir -p"
