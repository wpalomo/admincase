# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import helpers
from .views import (MedicamentoListView, MedicamentoCreate, MedicamentoUpdate,
                    MedicamentoLaboratorioCreate, MedicamentoLaboratorioUpdate,
                    MedicamentoLaboratorioDelete)


urlpatterns = patterns('',
   url(r'^listado/$', MedicamentoListView.as_view(),
       name='medicamento_listado'),
   url(r'^alta/$', MedicamentoCreate.as_view(),
       name='medicamento_alta'),
   url(r'^modi/(?P<pk>[0-9]+)/$',
       MedicamentoUpdate.as_view(), name='medicamento_modi'
       ),
   url(r'^get_eliminar_item/$', helpers.get_eliminar_item,
       name='eliminar_item'
       ),
   url(r'^laboratorios/alta/(?P<pk>[0-9]+)/$',
       MedicamentoLaboratorioCreate.as_view(),
       name='medicamento_laboratorio_create'
       ),
   url(r'^laboratorios/modi/(?P<pk>[0-9]+)/$',
       MedicamentoLaboratorioUpdate.as_view(),
       name='medicamento_laboratorio_update'
       ),
   url(r'^laboratorios/delete/(?P<pk>[0-9]+)/$',
       MedicamentoLaboratorioDelete.as_view(),
       name='medicamento_laboratorio_delete'
       ),
)
