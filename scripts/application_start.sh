#!/usr/bin/env bash

source $(dirname $0)/common.sh

$MKDIR $RUN_PATH
$MKDIR $LOG_PATH

$CHOWN $WEB_USER:$WEB_USER $RUN_PATH
$CHOWN $WEB_USER:$WEB_USER $LOG_PATH

cd $APPLICATION_PATH$BACKEND_PATH_SUFFIX
sudo -u $WEB_USER $PYTHON_ENV_PATH/bin/gunicorn --daemon --name $APPLICATION_NAME --bind unix:$RUN_PATH/backend.sock --pid $RUN_PATH/backend.pid --error-logfile $LOG_PATH/backend.log wsgi:app

cd $APPLICATION_PATH$FRONTEND_PATH_SUFFIX/production
SOCK=$RUN_PATH/frontend.sock sudo -u $WEB_USER $PM2 start --name $APPLICATION_NAME --interpreter node_modules/@babel/node/bin/babel-node.js index.js -o $LOG_PATH/frontend.log -e $LOG_PATH/frontend.log

exit 0
