#!/bin/bash

set -e

# general config
ROOT="/home/niwi/devel/niwi-web"
PYTHONBIN="/usr/bin/python2"
GEVENTSERVER="$ROOT/scripts/geventserver.py"

PIDFILE="$ROOT/geventserver.pid"
LOGFILE="$ROOT/geventserver.log"
DAEMONPARAMS="--root="$ROOT" --pidfile="$PIDFILE" --logfile="$LOGFILE" --settings=niwi.settings  -p 9000 --daemon"

case "$1" in
    start)
        echo "Starting GeventServer..."
        if [ -s $PIDFILE ]; then
            echo "GeventServer is already running."
        else
            cd
            $PYTHONBIN $GEVENTSERVER $DAEMONPARAMS
            if [ $? -ne 0 ]; then
                echo "GeventServer is now runngin."
            fi
        fi
        ;;
    stop)
        echo "Stopping GeventServer"
        kill -QUIT `cat $PIDFILE` &>/dev/null
        if [ $? -ne 0 ]; then
            echo "Fail on stop GeventServer"
        else
            echo "GeventServer is now stoped"
            rm $PIDFILE
        fi
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    *)
        echo "usage: $0 {start|stop|restart}"
esac
