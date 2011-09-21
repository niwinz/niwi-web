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
from niwi_photo.models import *
from niwi.views.generic import GenericView

import logging, itertools
logger = logging.getLogger("niwi")


class PhotoHome(GenericView):
    template_name = 'photo/index.html'

    def get(self, request):
        photos = Photo.objects.order_by('-created_date')[:20]
        years_queryset = Photo.objects.dates('created_date','year')
        
        context = {
            'photos': photos,
            'years': [x.year for x in years_queryset],
        }

        return self.render_to_response(self.template_name, context)
 

class AlbumsView(GenericView):
    template_name = 'photo/albums.html'

    def get(self, request):
        albums = Album.objects.order_by('-created_date')[:20]
        years_queryset = Album.objects.dates('created_date','year')
        
        context = {
            'albums': albums,
            'years': [x.year for x in years_queryset],
        }
        return self.render_to_response(self.template_name, context)


class AlbumPhotosView(GenericView):
    template_name = 'photo/album_detail.html'

    def get(self, request, aslug):
        album = get_object_or_404(Album, slug=aslug)
        photos = album.photos.all()
        years_queryset = photos.dates('created_date','year')

        context = {
            'album': album,
            'photos': photos,
            'years': [x.year for x in years_queryset],
        }
        return self.render_to_response(self.template_name, context)
