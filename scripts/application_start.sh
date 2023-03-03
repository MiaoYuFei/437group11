#!/usr/bin/env bash

source $(dirname $0)/common.sh

cd $APPLICATION_PATH/backend
sudo -u www-data $PYTHON_ENV_PATH/bin/python3 $APPLICATION_PATH/backend/main.py &
echo $! > $PID_PATH/stocknews-backend.pid

cd $APPLICATION_PATH/frontend/stocknews
sudo -u www-data npm run build &
echo $! > $PID_PATH/stocknews-frontend.pid
