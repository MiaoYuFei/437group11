#!/usr/bin/env bash

source $(dirname $0)/common.sh

sudo -u $WEB_USER $PM2_STOP $APPLICATION_NAME

BACKEND_PID_FILE="$RUN_PATH/backend.pid"
if test -f "$BACKEND_PID_FILE"; then
    BACKEND_PID="$(<$BACKEND_PID_FILE)"
    $KILL $BACKEND_PID
    $RM $BACKEND_PID_FILE
fi

$RM $PID_PATH

exit 0
