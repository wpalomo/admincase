# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import ContactoCreate, ContactoDelete, ContactoUpdate


urlpatterns = patterns('',
    url(r'^alta/(?P<pk>[0-9]+)/$',
        ContactoCreate.as_view(), name='contacto_create'),
    url(r'^modi/(?P<pk>[0-9]+)/$',
        ContactoUpdate.as_view(), name='contacto_update'),
    url(r'^delete/(?P<pk>[0-9]+)/$',
        ContactoDelete.as_view(), name='contacto_delete'),
)
