# -*- coding: utf-8 -*-
# Copyright (c) 2011 Andrei Antoukh <niwi@niwi.be>
# License: BSD-3 
# Version: 2

from gevent.queue import Queue
from gevent import sleep, spawn

from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from logging import StreamHandler, Handler

import re, glob, requests

class Singleton(type):
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance



""" Local use handlers. """

class GreenHandlerMixin(object):
    _log_queue = Queue()
    def __init__(self, *args, **kwargs):
        super(GreenHandlerMixin, self).__init__(*args, **kwargs)
        self.grl = spawn(self.__save_loop)

    def __save_loop(self):
        while True:
            record = self._log_queue.get()
            super(GreenHandlerMixin, self).emit(record)
    
    def emit(self, record):
        self._log_queue.put_nowait(record)


class GreenInfiniteTimedRotatingFileHandler(GreenHandlerMixin, TimedRotatingFileHandler):
    """ Gevent-based infinite async time rotating log file handler.

    Usage:
        Add this to your log configuration, and assign it to any 
        logger you are using:

       'handlername':{
           'level':'DEBUG',
           'when': 'h',
           'interval': 2,
           'class':'niwi_logging.handlers.GreenInfiniteTimedRotatingFileHandler',
           'filename': '/tmp/debug.log',
           'formatter': 'verbose',
       }
    """
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        super(GreenInfiniteTimedRotatingFileHandler, self).__init__(filename, when, interval, backupCount, encoding, delay, utc)
        self.backupCount = self.current_max_files() 
    
    def current_max_files(self):
        files = sorted(glob.glob("%s*" % (self.baseFilename)), reverse=True)
        print files
        if not files:
            return 10
        else:
            return len(files) + 10
        
    def doRollover(self):
        super(GreenInfiniteTimedRotatingFileHandler, self).doRollover()
        self.backupCount += 1


class GreenInfiniteRotatingFileHandler(GreenHandlerMixin, RotatingFileHandler):
    """ Gevent-based infinite async rotating log file handler.

    Usage:
        Add this to your log configuration, and assign it to any 
        logger you are using:

       'handlername':{
           'level':'DEBUG',
           'maxBytes':2000,
           'class':'niwi_logging.handlers.GreenInfiniteRotatingFileHandler',
           'filename': '/tmp/debug.log',
           'formatter': 'verbose',
       }
    """

    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0):
        super(GreenInfiniteRotatingFileHandler, self).__init__(filename, 'a', maxBytes, backupCount, encoding, delay)
        self.rx = re.compile("^[\w\d\-\/\.\_]+\.(\d+)$", flags=re.U)
        self.backupCount = self.current_max_files() or 1

    def current_max_files(self):
        files = sorted(glob.glob("%s*" % (self.baseFilename)), reverse=True)
        if not files:
            return None
        
        if self.rx.match(files[0]):
            return int(self.rx.search(files[0]).group(1))
        else:
            return None

    def doRollover(self):
        super(GreenInfiniteRotatingFileHandler, self).doRollover()
        self.backupCount += 1


class GreenRotatingFileHandler(GreenHandlerMixin, RotatingFileHandler):
    """ Gevent-based async rotating log file handler.

    Usage:
        Add this to your log configuration, and assign it to any 
        logger you are using:

       'handlername':{
           'level':'DEBUG',
           'maxBytes':2000,
           'backupCount':3,
           'class':'niwi_logging.handlers.GreenRotatingFileHandler',
           'filename': '/tmp/debug.log',
           'formatter': 'verbose',
       }
    """
    pass


class GreenStreamHandler(StreamHandler):
    """ Gevent-based async StreamHandler implementation.

    Usage:
        Add this to your log configuration, and assign it to any 
        logger you are using:

       'console':{
           'level':'DEBUG',
           'class':'niwi_logging.handlers.GreenStreamHandler',
           'formatter': 'verbose',
       }
    """
    _log_queue = Queue()
    def __init__(self, *args, **kwargs):
        #super(GreenStreamHandler, self).__init__(*args, **kwargs)
        StreamHandler.__init__(self, *args, **kwargs)
        self.grl = spawn(self.__save_loop)

    def __save_loop(self):
        while True:
            record = self._log_queue.get()
            #super(GreenStreamHandler, self).emit(record)
            StreamHandler.emit(self, record)
    
    def emit(self, record):
        self._log_queue.put_nowait(record)


""" Remote use handlers. """

class RemoteNiwiLoggingHandler(Handler):
    """ Gevent-based async stream handler to remote server over 
    http/https protocol.

    Usage:
        Add this to your log configuration, and assign it to any 
        logger you are using:

       'handlername':{
           'level':'DEBUG',
           'class':'niwi_logging.handlers.RemoteNiwiLoggingHandler',
           'username': 'foouser',
           'passowrd': 'foopass',
           'reference': 'niwibe',
           'name':'handlername',
           'url': 'https://remotehost.domain/logging/',
           'formatter': 'verbose',
       }
    """

    _log_queue = Queue()
    def __init__(self, username, password, reference, url, name):
        super(RemoteNiwiLoggingHandler, self).__init__()
        self.grl = spawn(self.__save_loop)
        self._username = username
        self._password = password
        self._reference = reference
        self._name = name
        self._url = url
        

    def __save_loop(self):
        while True:
            self.__send_logrecord(self._log_queue.get())

    def __send_logrecord(self, record):
        raw_record = self.format(record)
        request_data = {'reference': self._reference, 'record': raw_record, 'name':self._name,\
            'username': self._username, 'password':self._password}
        response = requests.post(self._url, data=request_data)
    
    def emit(self, record):
        self._log_queue.put_nowait(record)
