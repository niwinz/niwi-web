# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.conf import settings
from django.contrib import messages

from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction, IntegrityError
from django.utils import simplejson

import datetime
import base64
import hashlib
import hmac

import logging
logger = logging.getLogger("niwi")

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4 
    inp += "="*padding_factor 
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request):
    secret = settings.FCBK_APP_SECRET
    encoded_sig, payload = signed_request.split('.', 2)
    sig = base64_url_decode(encoded_sig)
    data = simplejson.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        return data



class FacebookMiddleware(object):
    def process_request(self, request):
        if "signed_request" in request.POST:
            if request.method == 'POST':
                request.method = 'GET'

            signed_request = parse_signed_request(request.POST['signed_request'])
            logger.debug('FacebookMiddleware: received signed_request')
            logger.debug('FacebookMiddleware: %s' % (str(signed_request)))

        return None

