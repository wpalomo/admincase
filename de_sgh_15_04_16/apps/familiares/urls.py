# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import BusquedaFamiliarView, FamiliarCreate, \
    FamiliarPacienteCreate, FamiliarUpdate, FamiliarDeleteView


urlpatterns = patterns('',
    url(r'^busqueda/(?P<id>[0-9]+)/$',
        BusquedaFamiliarView.as_view(), name='familiar-busqueda'),
    url(r'^alta/(?P<id>[0-9]+)/$', FamiliarCreate.as_view(), name='familiar-alta'),
    url(r'^alta/(?P<id>[0-9]+)/(?P<familiar>[0-9]+)/$',
        FamiliarPacienteCreate.as_view(), name='familiar-alta'),
    url(r'^modi/(?P<pk>[0-9]+)/(?P<paciente>[0-9]+)/$', FamiliarUpdate.as_view()
        , name='familiar-modificar'),
    url(r'^eliminar/(?P<pk>[0-9]+)/$', FamiliarDeleteView.as_view()
        , name='familiar-eliminar'),
    )
