# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import DomicilioCreate, DomicilioUpdate, DomicilioDelete


urlpatterns = patterns('',
    url(r'^modi/(?P<pk>[0-9]+)/$',
        DomicilioUpdate.as_view(), name='domicilio_update'),
    url(r'^alta/(?P<id>[0-9]+)/$',
        DomicilioCreate.as_view(), name='domicilio_create'),
    url(r'^delete/(?P<pk>[0-9]+)/$',
        DomicilioDelete.as_view(), name='domicilio_delete'),
    url(r'^clientes/modi/(?P<pk>[0-9]+)/$',
        DomicilioUpdate.as_view(), name='domicilio_cliente_update')
)