# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import InstitucionCreate, InstitucionList, InstitucionUpdate


urlpatterns = patterns('',
    url(r'^alta/$', InstitucionCreate.as_view(), name='institucion_alta'),

    url(r'^listado/$', InstitucionList.as_view(), name='institucion_listado'),

    url(
        r'^modi/(?P<pk>[0-9]+)/$',
        InstitucionUpdate.as_view(),
        name='institucion_update'
        ),
)