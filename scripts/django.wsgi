import sys, os
current_path = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(current_path, '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'niwi.settings'



import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
