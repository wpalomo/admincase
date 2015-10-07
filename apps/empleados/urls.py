# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import (EmpleadoListView, EmpleadoCreate, EmpleadoUpdate,
                    EmpleadoDelete)


urlpatterns = patterns('',
    url(r'^listado/$', EmpleadoListView.as_view(), name='empleado_listado'),
    url(r'^alta/$', EmpleadoCreate.as_view(), name='empleado_alta'),
    url(r'^modi/(?P<pk>[0-9]+)/$',
        EmpleadoUpdate.as_view(), name='empleado_update'),
    url(r'^delete/(?P<pk>[0-9]+)/$',
        EmpleadoDelete.as_view(), name='empleado_delete'),
)