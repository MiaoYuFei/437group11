#!/usr/bin/env bash

source $(dirname $0)/common.sh

$MKDIR $PID_PATH
$MKDIR $LOG_PATH

cd $APPLICATION_PATH$BACKEND_PATH_SUFFIX
sudo -u $WEB_USER $PYTHON_ENV_PATH/bin/python3 $APPLICATION_PATH$BACKEND_PATH_SUFFIX/main.py >>$LOG_PATH/backend.log 2>&1 &
echo $! > $PID_PATH/backend.pid

cd $APPLICATION_PATH$FRONTEND_PATH_SUFFIX
sudo -u $WEB_USER npm run build >>$LOG_PATH/frontend.log 2>&1 &
echo $! > $PID_PATH/frontend.pid

exit 0
