# -*- coding: utf-8 -*-

import os

if "NIWI_ENVIRON" in os.environ:
    if os.environ["NIWI_ENVIRON"] in ('production', 'development', 'local'):
        print "importing %s" % os.environ["NIWI_ENVIRON"]
        eval("from .%s import *" % (os.environ["NIWI_ENVIRON"]))

else:
    try:
        print "Trying import local.py settings..."
        from .local import *
    except ImportError:
        print "Trying import development.py settings..."
        from .development import *

