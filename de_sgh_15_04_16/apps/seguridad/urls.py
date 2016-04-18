# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import (PerfilCreate, PerfilUpdate, PerfilListView, PerfilDelete,
                    PerfilModuloCreate, PerfilModuloDelete)


urlpatterns = patterns('',
    url(r'^perfil/alta/$', PerfilCreate.as_view(), name='perfil_alta'),

    url(r'^perfil/modi/(?P<pk>[0-9]+)/$',
        PerfilUpdate.as_view(),
        name='perfil_modi'
        ),

    url(r'^perfil/listado/$', PerfilListView.as_view(), name='perfil_listado'),

    url(
        r'^perfil/borrar/(?P<pk>[0-9]+)/$',
        PerfilDelete.as_view(),
        name='perfil_borrar'
        ),

    url(
        r'^perfil/modulos/(?P<pk>[0-9]+)/$',
        PerfilModuloCreate.as_view(),
        name='perfil_modulo_create'
        ),

    url(
        r'^perfil/modulos/borrar/(?P<pk>[0-9]+)/$',
        PerfilModuloDelete.as_view(),
        name='perfil_modulo_delete'
        ),
)