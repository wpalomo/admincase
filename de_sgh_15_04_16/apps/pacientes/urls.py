# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import (PacienteListView, PacienteCreate, PacienteUpdate)


urlpatterns = patterns('',
   url(r'^listado/$', PacienteListView.as_view(),
       name='pacientes_listado'),
   url(r'^alta/$', PacienteCreate.as_view(),
       name='paciente_alta'),
   url(r'^modi/(?P<pk>[0-9]+)/$',
       PacienteUpdate.as_view(),
       name='paciente_update'),
   )
