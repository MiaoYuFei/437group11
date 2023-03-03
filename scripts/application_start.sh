#!/usr/bin/env bash

source $(dirname $0)/common.sh

$MKDIR $PID_PATH
$MKDIR $LOG_PATH

cd $APPLICATION_PATH$BACKEND_PATH_SUFFIX
sudo -u $WEB_USER $PYTHON_ENV_PATH/bin/python3 $APPLICATION_PATH$BACKEND_PATH_SUFFIX/main.py >>$LOG_PATH/backend.log 2>&1 &
echo $! > $PID_PATH/backend.pid

cd $APPLICATION_PATH$FRONTEND_PATH_SUFFIX/production
sudo -u $WEB_USER $PM2_START --name $APPLICATION_NAME --interpreter node_modules/@babel/node/bin/babel-node.js index.js -o $LOG_PATH/frontend.log -e $LOG_PATH/frontend.log

exit 0
