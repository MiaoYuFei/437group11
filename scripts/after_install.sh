#!/usr/bin/env bash

source $(dirname $0)/common.sh

chown -R www-data:www-data $APPLICATION_PATH
cd $APPLICATION_PATH/backend
sudo -u www-data python3 -m venv $PYTHON_ENV_PATH
sudo -u www-data $PYTHON_ENV_PATH/bin/python3 -m pip install -r $APPLICATION_PATH/backend/requirements.txt
cd $APPLICATION_PATH/frontend/stocknews
sudo -u www-data npm install
