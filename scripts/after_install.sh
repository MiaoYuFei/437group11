#!/usr/bin/env bash

source $(dirname $0)/common.sh

chown -R $WEB_USER:$WEB_USER $APPLICATION_PATH
cd $APPLICATION_PATH$BACKEND_PATH_SUFFIX
sudo -u $WEB_USER python3 -m venv $PYTHON_ENV_PATH
sudo -u $WEB_USER $PYTHON_ENV_PATH/bin/python3 -m pip install -r $APPLICATION_PATH$BACKEND_PATH_SUFFIX/requirements.txt
cd $APPLICATION_PATH$FRONTEND_PATH_SUFFIX
sudo -u $WEB_USER npm install
sudo -u $WEB_USER npm run build

exit 0
