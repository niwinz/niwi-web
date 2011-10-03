# -*- coding: utf-8 -*-
"""
TODO:
 * consider use this snippet http://djangosnippets.org/snippets/1707/ 
    for check if connection state is connected.
 * make thread persistent pool.
"""

from Queue import Queue
import threading
import psycopg2

class PoolError(Exception):
    pass


class QueuePool(object):
    def __init__(self, minconn, maxconn, dbparams, ilevel, settings):
        self.minconn = minconn
        self.maxconn = maxconn
        self.closed = False
        self.dbparams = dbparams
        self._pool = Queue()
        self._isolation_level = ilevel
        self._conns = []
        self._settings = settings
        self._lock = threading.Lock()

        for x in xrange(self.minconn):
            self._pool.put(self._connect())

    def _connect(self):
        conn = psycopg2.connect(**self.dbparams)
        conn.set_client_encoding('UTF8')
        conn.set_isolation_level(self._isolation_level)

        cursor = conn.cursor()
        cursor.execute("SET TIME ZONE %s", [self._settings['TIME_ZONE']])
        cursor.close()

        self._conns.append(id(conn))
        return conn

    def _try_connected(self, connection):
        try:
            connection.cursor().execute("SELECT 1;")
            return True
        except psycopg2.OperationalError:
            return False

    def _getconn(self):
        if self._pool.qsize() == 0:
            return True, self._connect()
        else:
            conn = self._pool.get(block=True)
            if self._try_connected(conn):
                return False, conn
            else:
                return True, self._connect()

    def _putconn(self, conn):
        if id(conn) in self._conns:
            self._pool.put(conn, block=True)
        else:
            conn.close()

    def getconn(self):
        self._lock.acquire()
        try:
            return self._getconn()
        finally:
            self._lock.release()

    def putconn(self, conn):
        self._lock.acquire()
        try:
            self._putconn(conn)
        finally:
            self._lock.release()
