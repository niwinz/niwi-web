# -*- coding: utf-8 -*-
"""
TODO:
    * make connection counter with auto garbage
        collection procedure.
"""

from Queue import Queue
import threading
import psycopg2

class PoolError(Exception):
    pass


class QueuePool(object):
    def __init__(self, maxconn, dbparams, ilevel, settings):
        self.maxconn = maxconn
        self.closed = False
        self.dbparams = dbparams
        self._pool = Queue()
        self._isolation_level = ilevel
        self._conns = []
        self._settings = settings
        self._lock = threading.Lock()

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
        return self._getconn()

    def putconn(self, conn):
        self._putconn(conn)


class PersistentPool(QueuePool):
    def __init__(self, *args, **kwargs):
        super(PersistentPool, self).__init__(*args, **kwargs)
        self._pool = {}

    def _getconn(self):
        key = threading.current_thread().ident
        newc, conn = None, None

        if key not in self._pool:
            self._pool[key] = Queue()
            newc, conn = True, self._connect()
        else:
            if self._pool[key].qsize() == 0:
                newc, conn = True, self._connect()
            else:
                newc, conn = False, self._pool[key].get(block=True)

        return newc, conn

    def _putconn(self, conn):
        key = threading.current_thread().ident
        if key in self._pool:
            self._pool[key].put(conn, block=False)
        else:
            conn.close()
