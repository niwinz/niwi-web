# -*- coding: utf-8 -*-

from psycopg2.extras import register_hstore

from django import VERSION
from django.db.backends.util import truncate_name
from django.db.backends.postgresql_psycopg2.base import *
from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as BaseDatabaseWrapper

import uuid

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
    
    def _cursor(self):
        """
        Returns a unique server side cursor if they are enabled, 
        otherwise falls through to the default client side cursors.
        """
        if self.server_side_cursors:
            # intialise the connection if we haven't already
            # this will waste a client side cursor, but only on the first call
            if self.connection is None:
                super(DatabaseWrapper, self)._cursor()
            
            # give the cursor a unique name which will invoke server side cursors
            cursor = self.connection.cursor(name='cur%s' % str(uuid.uuid4()).replace('-', ''))
            cursor.tzinfo_factory = None
            
            if self.server_side_cursor_itersize is not None:
                cursor.itersize = self.server_side_cursor_itersize
            
            return CursorWrapper(cursor)
        
        return super(DatabaseWrapper, self)._cursor()
