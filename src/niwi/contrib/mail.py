# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from gevent.event import Event
from gevent import sleep, spawn

from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend

class EmailBackend(DjangoEmailBackend):
    """ Gevent ready async smtp email backend. """

    _pending_sent = []
    _ready_sent = Event()

    def __init__(self, *args, **kwargs):
        spawn(self.__mail_proc)
        super(EmailBackend, self).__init__(*args, **kwargs)

    def __mail_proc(self):
        self._ready_sent.wait()
        super(EmailBackend, self).send_messages(self._pending_sent)
    
    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        self._pending_sent = email_messages
        self._ready_sent.set()
        return len(email_messages)
