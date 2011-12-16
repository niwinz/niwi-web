# -*- coding: utf-8 -*-

from django.views.decorators.cache import cache_page
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, ImageFormatter
from pygments.styles import get_style_by_name

from niwi.web.models import Paste
from niwi.web.forms import PasteForm
from niwi.web.views.generic import GenericView

import logging
logger = logging.getLogger("niwi")


class PasteHomeView(GenericView):
    template_name = "paste/post.html"

    def get_pastes(self):
        return Paste.objects.order_by('-created')[:20]

    def get(self, request):
        form = PasteForm(request=request)
        context = {'form':form, 'pastes':self.get_pastes()}
        return self.render_to_response(self.template_name, context)

    def post(self, request):
        form = PasteForm(request.POST, request=request)
        if form.is_valid():
            paste_obj = Paste.objects.create(
                text = form.cleaned_data.get('paste'),
                lexer = form.cleaned_data.get('lexer'),
                title = form.cleaned_data.get('title'),
                group = form.cleaned_data.get('group'),
            )
            return HttpResponseRedirect(reverse('web:paste-view', args=[paste_obj.id]))
        
        context = {'form':form, 'pastes':self.get_pastes()}
        return self.render_to_response(self.template_name, context)


class PasteDetailView(GenericView):
    template_name = "paste/view.html"

    def get(self, request, pasteid):
        paste_obj = get_object_or_404(Paste, pk=int(pasteid))
        style = get_style_by_name('trac')
        lexer = get_lexer_by_name(paste_obj.lexer, stripall=True)
        formatter = HtmlFormatter(
            linenos=False, 
            nobackground=True,
            encoding="utf-8",
            style=style
        )
        result = highlight(paste_obj.text, lexer, formatter)
        context = {
            'result': result,
            'obj':paste_obj,
            'style': formatter.get_style_defs('.highlight')
        }
        return self.render_to_response(self.template_name, context)


class PasteDetailRawView(GenericView):
    def get(self, request, pasteid):
        paste_obj = get_object_or_404(Paste, pk=int(pasteid))
        return HttpResponse(paste_obj.text, mimetype="text/plain")
