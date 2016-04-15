# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import NotaCreate, NotaUpdate, NotaDelete

urlpatterns = patterns('',
    url(r'^alta/(?P<id>[0-9]+)/$',
        NotaCreate.as_view(), name='notas-create'),
    url(r'^delete/(?P<pk>[0-9]+)/$',
        NotaDelete.as_view(), name='notas-delete'),
    url(r'^modi/(?P<pk>[0-9]+)/$',
        NotaUpdate.as_view(), name='notas_update'),
    )

