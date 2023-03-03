#!/usr/bin/env bash

source $(dirname $0)/common.sh

FRONTEND_PID_FILE=$PID_PATH/stocknews-frontend.pid
if test -f "$FRONTEND_PID_FILE"; then
    FRONTEND_PID=$(<$FRONTEND_PID_FILE)
    kill -9 $FRONTEND_PID
    rm -f $FRONTEND_PID_FILE
fi

BACKEND_PID_FILE=$PID_PATH/stocknews-backend.pid
if test -f "$BACKEND_PID_FILE"; then
    BACKEND_PID=$(<$BACKEND_PID_FILE)
    kill -9 $BACKEND_PID
    rm -f $BACKEND_PID_FILE
fi
