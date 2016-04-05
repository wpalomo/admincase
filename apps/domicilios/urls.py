# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import DomicilioUpdate, DomicilioCreate, DomicilioDelete


urlpatterns = patterns('',
    url(r'^modi/(?P<pk>[0-9]+)/$',
        DomicilioUpdate.as_view(), name='domicilio_update'),
    url(r'^alta/(?P<id>[0-9]+)/$',
        DomicilioCreate.as_view(), name='domicilio-create'),
    url(r'^delete/(?P<pk>[0-9]+)/$',
        DomicilioDelete.as_view(), name='domicilio-delete'),
    url(r'^empleados/modi/(?P<pk>[0-9]+)/$',
        DomicilioUpdate.as_view(), name='domicilio_update'),
    url(r'^pacientes/modi/(?P<pk>[0-9]+)/$',
        DomicilioUpdate.as_view(), name='domicilio_update'),
    )
