# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.conf import settings

from functools import wraps

from boto.exception import S3CreateError
from boto.exception import S3ResponseError
from boto.s3.connection import S3Connection
from boto.s3.key import Key

import os.path, random, string, uuid, Image, logging

from .models import Upload
log = logging.getLogger("niwi")


def random_filename(chars=string.ascii_lowercase, length=16, prefix='',suffix=''):
    """ Examples:
    >>> random_filename(length=20)
    'nlxplmqmkgppdraokpbc'
    >>> random_filename(length=20, prefix="foo-")
    'foo-fjqaqpcfgosamrdk'
    >>> random_filename(length=20, prefix="foo-", suffix=".txt")
    'foo-yppuoaltkjfz.txt'
    >>> random_filename(chars="xc", length=20, prefix="foo-", suffix=".txt")
    'foo-xcxxxxcccxxx.txt'
    """

    if length - len(prefix)-len(suffix) < 0:
        raise ValueError("length - len(prefix)-len(suffix) is < 0")

    filename = ''.join([random.choice(chars) for i in range(length-len(prefix)-len(suffix))])
    filename = prefix + filename + suffix
    return filename


def test_settings(function):
    @wraps(function)
    def __wrapper(request, *args, **kwargs):
        request.aws_access_key = getattr(settings, 'AWS_ACCESS_KEY', False)
        request.aws_secret_key = getattr(settings, 'AWS_SECRET_KEY', False)
        request.aws_bucket = getattr(settings, 'AWS_BUCKET', False)
        request.aws_base_url = getattr(settings, 'AWS_BASE_URL', False)
        request.aws_s3uploader_prefix = getattr(settings,'AWS_S3UPLOADER_PREFIX', 'uploads')
        try:
            assert request.aws_access_key and request.aws_secret_key \
                and request.aws_bucket and request.aws_base_url
            return function(request, *args, **kwargs)
        except AssertionError:
            log.error('Application s3uploader not configured correctly')
            return HttpResponseForbidden("test")

    return __wrapper


class UploaderView(View):
    @method_decorator(test_settings)
    def get(self, request, *args, **kwargs):
        uploads = Upload.objects.all().order_by("-created")
        return render_to_response("index.html", {'uploads':uploads}, 
            context_instance=RequestContext(request))
 
    @method_decorator(test_settings)
    def post(self, request, *args, **kwargs):
        if not request.FILES:
            return HttpResponseRedirect(reverse("s3uploader:home"))

        self.s3connection = S3Connection(request.aws_access_key, request.aws_secret_key)
        self.s3bucket = self.s3connection.get_bucket(request.aws_bucket)
        for filekey in request.FILES:
            self.process_file(request, request.FILES[filekey])

        return HttpResponseRedirect(reverse("s3uploader:home"))

    def process_file(self, request, fileobj):
        extension = fileobj.name.split(".")[-1]
        if extension not in ['jpeg', 'jpg', 'png']:
            messages.info(request, _(u"The file %s is not image. Upload only: .jpeg, .jpg, .png" % (fileobj.name)))
            return

        random_name = "%(random)s-%(uuid)s" % {'random': random_filename(length=20), 'uuid': unicode(uuid.uuid4())}
        boto_key = "%(prefix)s/%(name)s.%(extension)s" % {'prefix': request.aws_s3uploader_prefix, \
            'name': random_name, 'extension': extension}

        key = Key(self.s3bucket, name=boto_key)
        key.set_contents_from_file(fileobj)
        key.make_public()

        imgobj = Image.open(fileobj)
        uploadobj = Upload(name=boto_key, path=boto_key)
        uploadobj.size = "%s x %s" % imgobj.size
        uploadobj.save()


class UploaderFileView(View):
    def get(self, request, *args, **kwargs):
        uploadobj = get_object_or_404(Upload, id=kwargs.get('id'))
        context = {'obj':uploadobj}
        return render_to_response("file.html", context,
            context_instance=RequestContext(request))


class UploaderDeleteFile(View):
    def get(self, request, *args, **kwargs):
        uploadobj = get_object_or_404(Upload, id=kwargs.get('id'))
        context = {'obj': uploadobj}
        return render_to_response("delete_file.html", context,
            context_instance=RequestContext(request))
    
    @method_decorator(test_settings)
    def post(self, request, *args, **kwargs):
        self.s3connection = S3Connection(request.aws_access_key, request.aws_secret_key)
        self.s3bucket = self.s3connection.get_bucket(request.aws_bucket)

        uploadobj = get_object_or_404(Upload, id=kwargs.get('id'))
        key = Key(self.s3bucket, name=uploadobj.path)
        key.delete()
        
        uploadobj.delete()
        return HttpResponseRedirect(reverse("s3uploader:home"))
