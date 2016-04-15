# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import (PersonaObraSocialCreate, PersonaObraSocialUpdate,
                    PersonaObraSocialDelete)

urlpatterns = patterns('',
    url(r'^alta/(?P<id>[0-9]+)/$', PersonaObraSocialCreate.as_view()),
    url(r'^modi/(?P<pk>[0-9]+)/$', PersonaObraSocialUpdate.as_view()),
    url(r'^eliminar/(?P<pk>[0-9]+)/$', PersonaObraSocialDelete.as_view()),
)
