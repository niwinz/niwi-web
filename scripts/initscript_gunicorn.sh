#!/bin/bash

set -e

# general config
PROCNAME="niwi-web-server"
ROOT="/home/niwi/devel/niwi-web"
PYTHONBIN="/usr/bin/python2"

GUNICORN_BIN="/usr/bin/gunicorn_django"
GUNICORN_WORKER_TYPE="gevent"
GUNICORN_MAX_REQUESRS="1000"
GUNICORN_NUM_WORKERS="5"
GUNICORN_LISTEN="0.0.0.0:9000"
GUNICORN_SETTINGS="$ROOT/niwi/settings.py"

GUNICORN_LOG="$ROOT/gunicornserver.log"
GUNICORN_PID="$ROOT/gunicornserver.pid"

DAEMONPARAMS="-k $GUNICORN_WORKER_TYPE -w $GUNICORN_NUM_WORKERS -b $GUNICORN_LISTEN\
    --daemon --preload -n $PROCNAME --log-file=$GUNICORN_LOG --pid=$GUNICORN_PID $GUNICORN_SETTINGS "

cd $ROOT

case "$1" in
    start)
        echo "Starting GunicornServer..."
        if [ -s $GUNICORN_PID ]; then
            echo "GunicornServer is already running."
        else
            cd
            $PYTHONBIN $GUNICORN_BIN $DAEMONPARAMS
            if [ $? -ne 0 ]; then
                echo "GunicornServer is now runngin."
            fi
        fi
        ;;
    stop)
        echo "Stopping GunicornServer"
        kill -QUIT `cat $GUNICORN_PID` &>/dev/null
        if [ $? -ne 0 ]; then
            echo "Fail on stop GunicornServer"
        else
            echo "GunicornServer is now stoped"
            rm $GUNICORN_PID
        fi
        ;;
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    *)
        echo "usage: $0 {start|stop|restart}"
esac
