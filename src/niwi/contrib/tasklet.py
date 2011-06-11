# -*- coding: utf-8 -*-
# Copyright (c) 2011 Andrei Antoukh <niwi@niwi.be>
# License: BSD-3
# Description:  Gevent 0.13+ / Treaded background task processor.
# Version: 0.1

import socket as standardsocket
from gevent import socket as geventsocket

import gevent
import logging
import time


logger = logging.getLogger("tasklet")

def countergen():
    """ Secuence id generator. """
    num = -1
    while True:
        num += 1
        yield str(num)

cgen = countergen()

def make_task(function):
    """ Decorator: makes function as async task. """

    def _wrapper(*gs, **kwgs):
        start_after = kwgs.pop('start_after', 0)
        def _subfunc():
            id, res = next(cgen), None
            logger.info(u"%s start task <%s>" % (id, function.__name__))

            if start_after:
                time.sleep(start_after)
                res = function(*gs, **kwgs)
            else:
                res = function(*gs, **kwgs)
            
            logger.info(u"%s end task <%s> with response: <%s>" % (id, function.__name__, res))

        if standardsocket.socket is geventsocket.socket:
            return gevent.spawn(_subfunc)
        else:
            import threading
            return threading.Thread(target=_subfunc).start()

    return _wrapper


"""
Example:

from time import sleep

import hashlib
import random

@make_task
def footask():
    sleep(random.randint(2, 10))
    return True
"""
