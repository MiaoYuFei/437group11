#!/usr/bin/env bash

source $(dirname $0)/common.sh

FRONTEND_PID_FILE=$PID_PATH/frontend.pid
if test -f "$FRONTEND_PID_FILE"; then
    FRONTEND_PID=$(<$FRONTEND_PID_FILE)
    $KILL $FRONTEND_PID
    $RM $FRONTEND_PID_FILE
fi

BACKEND_PID_FILE=$PID_PATH/backend.pid
if test -f "$BACKEND_PID_FILE"; then
    BACKEND_PID=$(<$BACKEND_PID_FILE)
    $KILL $BACKEND_PID
    $RM $BACKEND_PID_FILE
fi

exit 0
