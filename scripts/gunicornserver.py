import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = "niwi.settings"

from django.conf import settings
from django.utils import translation
translation.activate(settings.LANGUAGE_CODE)

from django.core.handlers.wsgi import WSGIHandler
_application = WSGIHandler()

def application(environ, start_response):
    # put this psycopg2 green patch
    return _application(environ, start_response)
