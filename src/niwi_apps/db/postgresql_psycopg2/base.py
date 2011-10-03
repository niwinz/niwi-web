# -*- coding: utf-8 -*-

"""
TODO:
    * set all pool params fron settings
    * add documentation to use with server
        side cursors.
"""


from psycopg2.extras import register_hstore
from psycopg2.pool import ThreadedConnectionPool, PersistentConnectionPool

from django import VERSION
from django.db.backends.util import truncate_name
from django.db.backends.postgresql_psycopg2.base import *
from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as BaseDatabaseWrapper
from django.core import signals

import uuid
import datetime
import threading

pool = None

def make_connection_params(self, settings_dict):
    if settings_dict['NAME'] == '':
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured("You need to specify NAME in your"
                                   " Django settings file.")
    conn_params = {
        'database': settings_dict['NAME'],
    }
    conn_params.update(settings_dict['OPTIONS'])
    if 'autocommit' in conn_params:
        del conn_params['autocommit']

    if settings_dict['USER']:
        conn_params['user'] = settings_dict['USER']
    if settings_dict['PASSWORD']:
        conn_params['password'] = settings_dict['PASSWORD']
    if settings_dict['HOST']:
        conn_params['host'] = settings_dict['HOST']
    if settings_dict['PORT']:
        conn_params['port'] = settings_dict['PORT']

    return conn_params

class DatabaseWrapper(BaseDatabaseWrapper):
    """
    Psycopg2 database backend that allows the use of server side cursors.
    
    Usage:
    
    qs = Model.objects.all()
    with server_side_cursors(qs, itersize=x):
        for item in qs.iterator():
            item.value
    
    """
    def __init__(self, *args, **kwargs):
        self.server_side_cursors = False
        self.server_side_cursor_itersize = None

        super(DatabaseWrapper, self).__init__(*args, **kwargs)

    def close(self):
        global pool
        
        if self.connection is None:
            return
        
        if not self.connection.closed:
            pool.putconn(self.connection)

        self.connection = None
        #print "close()"

    def _cursor(self):
        """
        Returns a unique server side cursor if they are enabled, 
        otherwise falls through to the default client side cursors.
        """
        new_connection = False
        set_tz = False
        settings_dict = self.settings_dict

        global pool, connections
        
        if not pool:
            from .pool import QueuePool
            conn_params = make_connection_params(self, self.settings_dict)
            pool = QueuePool(3, 7, conn_params, self.isolation_level,
                self.settings_dict)

        if not self.connection:
            #key = threading.current_thread().ident
            newcon, self.connection = pool.getconn()
            if newcon:
                new_connection = True

        cursor = None
        if self.server_side_cursors:
            # give the cursor a unique name which will invoke server side cursors
            cursor = self.connection.cursor(name='cur%s' % str(uuid.uuid4()).replace('-', ''))
            cursor.tzinfo_factory = None
            
            if self.server_side_cursor_itersize is not None:
                cursor.itersize = self.server_side_cursor_itersize
        else:
            cursor = self.connection.cursor()
            cursor.tzinfo_factory = None
            
        if new_connection:
            self._get_pg_version()
            connection_created.send(sender=self.__class__,
                            connection=self)

        return CursorWrapper(cursor)
