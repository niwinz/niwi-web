# -*- coding: utf-8 -*-

from django.db.backends.signals import connection_created
from django.dispatch import receiver

#@receiver(connection_created)
#def connection_created_handler(sender, connection, **kwargs):
#    #print "Connection created: ", id(connection.connection)
#    pass
