# -*- coding: utf-8 -*-

import uuid

#from django.db.backends.postgresql_psycopg2.base import *
#from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as BaseDatabaseWrapper

class server_side_cursors(object):
    """
    With block helper that enables and disables server side cursors.
    """
    def __init__(self, qs_or_using_or_connection, itersize=None):
        from django.db import connections
        from django.db.models.query import QuerySet
        
        self.itersize = itersize
        if isinstance(qs_or_using_or_connection, QuerySet):
            self.connection = connections[qs_or_using_or_connection.db]
        elif isinstance(qs_or_using_or_connection, basestring):
            self.connection = connections[qs_or_using_or_connection]
        else:
            self.connection = qs_or_using_or_connection
    
    def __enter__(self):
        self.connection.server_side_cursors = True
        self.connection.server_side_cursor_itersize = self.itersize
    
    def __exit__(self, type, value, traceback):
        self.connection.server_side_cursors = False
        self.connection.server_side_cursor_itersize = None
