# -*- coding: utf-8 -*-

from django.views.decorators.cache import cache_page
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.csrf.middleware import csrf_exempt
from django.template import RequestContext, loader
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, ImageFormatter
from pygments.styles import get_style_by_name

from .models import Paste
from .forms import PasteForm

import logging
logger = logging.getLogger("niwi")


@cache_page(30)
def paste(request):
    if request.method == 'POST':
        form = PasteForm(request.POST, request=request)
        if form.is_valid():
            paste_obj = Paste.objects.create(
                text = form.cleaned_data.get('paste'),
                lexer = form.cleaned_data.get('lexer'),
                title = form.cleaned_data.get('title'),
                group = form.cleaned_data.get('group'),
            )
            return HttpResponseRedirect(reverse('web:paste-view', args=[paste_obj.id]))
      
    else:
        form = PasteForm(request=request.META)

    pastes = Paste.objects.all().order_by('-created')[:30]

    ctx = {'form':form, 'pastes':pastes}
    return render_to_response("paste/post.html", ctx, mimetype="text/html",
        context_instance=RequestContext(request))

@cache_page(60**2)
def paste_view(request, pasteid):
    paste_obj = get_object_or_404(Paste, pk=int(pasteid))
    style = get_style_by_name('trac')
    lexer = get_lexer_by_name(paste_obj.lexer, stripall=True)
    formatter = HtmlFormatter(
        linenos=True, 
        nobackground=True,
        encoding="utf-8",
        style=style
    )
    result = highlight(paste_obj.text, lexer, formatter)
    ctx = {
        'result': result,
        'obj':paste_obj,
        'style': formatter.get_style_defs('.highlight')
    }
    return render_to_response("paste/view.html", ctx, mimetype="text/html",
        context_instance=RequestContext(request))


@cache_page(60**2)
def paste_view_raw(request, pasteid):
    paste_obj = get_object_or_404(Paste, pk=int(pasteid))
    return HttpResponse(paste_obj.text, mimetype="text/plain")
