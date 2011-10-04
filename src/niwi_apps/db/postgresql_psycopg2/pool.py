# -*- coding: utf-8 -*-

from Queue import Queue
import threading
import psycopg2

class PoolError(Exception):
    pass


class QueuePool(object):
    """ 
    Psycopg2-Django ORM Queue connection pool implementation.
    """

    def __init__(self, dbparams, ilevel, settings):
        """
        Queue pool constructor.

        :param dict dbparams: pyscopg2.connect() connection dictionary.
        :param enum ileve: pyscopg2 isolation level
        :param object settings: django settings part.
        """
        options = settings.get('OPTIONS', {})
        self.maxconn = "POOLSIZE" in options \
            and int(options['POOLSIZE']) or 10

        self.dbparams = dbparams
        self._pool = Queue()
        self._isolation_level = ilevel
        self._settings = settings
        self._lock = threading.Lock()

    def _connect(self):
        """
        Method for make a new database connection
        and set correct timezone and client encoding..
        """
        conn = psycopg2.connect(**self.dbparams)
        conn.set_client_encoding('UTF8')
        conn.set_isolation_level(self._isolation_level)

        cursor = conn.cursor()
        cursor.execute("SET TIME ZONE %s", [self._settings['TIME_ZONE']])
        cursor.close()
        return conn

    def _try_connected(self, connection):
        """
        Try if connection object is connected
        to a database.

        :param psycopg.connection connection: db connection.
        :returns: True or False
        :rtype: bool
        """
        try:
            connection.cursor().execute("SELECT 1;")
            return True
        except psycopg2.OperationalError:
            return False


    def _getconn(self):
        """
        Internal method: get connection from
        pool or create one new connection.
        """
        if self._pool.qsize() == 0:
            return True, self._connect()
        else:
            conn = self._pool.get(block=True)
            if self._try_connected(conn):
                return False, conn
            else:
                return True, self._connect()

    def _putconn(self, conn):
        """
        Internal method: put connection into a pool
        if this not full else, close connection.
        """
        with threading.Lock():
            if self._pool.qsize() >= self.maxconn:
                conn.close()
            else:
                self._pool.put(conn, block=False)

    def getconn(self):
        """
        Public method for get connection 
        from a pool.
        """
        return self._getconn()

    def putconn(self, conn):
        """
        Public method for put connection
        into a pool.
        """
        self._putconn(conn)


class PersistentPool(QueuePool):
    """
    Thread persistent connection pool.

    QueuePool is similar to, but maintains 
    a queue for each thread, thus ensuring 
    that a thread always receives the same 
    connections.

    In most of my tests with django, only one 
    connection is maintained by thread.
    """
    
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
