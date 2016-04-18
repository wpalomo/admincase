# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import FichaSocialCreate, FichaSocialUpdate


urlpatterns = patterns('',
    url(r'^alta/(?P<id>[0-9]+)/$',
        FichaSocialCreate.as_view(), name='ficha-social-create'),
    url(r'^modi/(?P<id>[0-9]+)/(?P<pk>[0-9]+)/$',
        FichaSocialUpdate.as_view(), name='ficha-social-update'),
    url(r'^verificacion/(?P<id>[0-9]+)/$',
        'apps.fichassociales.views.redireccionar_ficha',
        name='ficha-social-update'),
    )
