# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import cache_page
from django.views.generic import View
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib import messages

from niwi.models import *
from niwi.views.generic import GenericView

import logging, itertools

logger = logging.getLogger("niwi")

