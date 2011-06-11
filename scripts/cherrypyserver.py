#!/usr/bin/python
# Copyright (c) 2011 Andrei Antoukh <niwi@niwi.be>
# License: BSD-3
# Description:  CherryPy wsgi server.
# Version: 1
#
# Changelog:
#   * 03-05-2011 First version of cherrypy wsgi server.

import sys, os, traceback
from optparse import OptionParser

root_path = os.path.dirname(os.path.realpath(__file__))
current_path = os.path.abspath('.')

def extract_application(filename):
    import imp 
    basename = os.path.basename(filename)
    if '.' in basename:
        name, suffix = basename.rsplit('.', 1)
    else:
        name, suffix = basename, ''

    module = imp.load_module(name, open(filename), filename, (suffix, 'r', imp.PY_SOURCE))
    return module.application




from cherrypy.wsgiserver import CherryPyWSGIServer

def django_worker_function(options, args):
    from django.core.handlers.wsgi import WSGIHandler
    from django.conf import settings
    from django.utils import translation
    translation.activate(settings.LANGUAGE_CODE)

    if len(args) > 0:
        appfile = args[0]
        try:
            application = extract_application(appfile)
        except AttributeError:
            sys.exit("Could not find application in %s" % filename)
    
    else:
        application = WSGIHandler()
        
    server = CherryPyWSGIServer((options.host, int(options.port)), application, request_queue_size=500)
    print >>sys.stderr, "Serving on %s:%s\n" % (options.host, options.port)
    server.start()


def wsgi_worker_function(options, args):
    if len(args) > 0:
        appfile = args[0]
        try:
            application = extract_application(appfile)
        except AttributeError:
            sys.exit("Could not find application in %s" % filename)

        server = CherryPyWSGIServer((options.host, int(options.port)), application, request_queue_size=500)
        print >>sys.stderr, "Serving on %s:%s\n" % (options.host, options.port)
        server.start()

    else:
        sys.exit("Is necesary application file.")


def write_pidfile(options, pid):
    if options.pidfile:
        pidpath = os.path.join(current_path, options.pidfile)
        if os.path.exists(pidpath):
            os.remove(pidpath)
        with open(pidpath, "w") as pidfile:
            pidfile.write("%s\n" % (pid))


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-P', '--pidfile', dest='pidfile', help='set pidfile path')
    parser.add_option('-p', '--port', dest='port', default='9000', help='set local port for listen')
    parser.add_option('-i', '--host', dest='host', default='0.0.0.0', help='set hostname')
    parser.add_option('-r', '--root', dest='root', default='local', help='set root directory')
    parser.add_option('-s', '--settings', dest='settings', default='settings', help='set settings module string')
    parser.add_option('-d', '--daemon', dest='daemon', default=False, action="store_true", help="run in daemon mode")
    parser.add_option('-t', '--type', dest='type', default='django', help="set type application: django, wsgi")

    options, args = parser.parse_args()
    if options.root == 'local':
        sys.path.append(current_path)
    else:
        current_path = os.path.join(current_path, options.root)
        sys.path.append(current_path)
    
    if options.type == 'django':
        os.environ['DJANGO_SETTINGS_MODULE'] = options.settings

    if options.daemon:
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
            sys.exit(1)

        os.setsid()
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                write_pidfile(options, pid)
                sys.exit(0)

        except OSError as e:
            print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
            sys.exit(1)
        
    else:
        write_pidfile(options, os.getpid())
 
    if options.type == 'django':
        django_worker_function(options, args)
    else:
        wsgi_worker_function(options, args)
