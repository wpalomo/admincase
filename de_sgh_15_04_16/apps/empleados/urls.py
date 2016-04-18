# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import helpers

from .views import (EmpleadoListView, EmpleadoCreate, EmpleadoUpdate,
                    AuditoriaList, AsignacionFormalCreate,
                    AsignacionFormalUpdate, AsignacionFormalDelete)

from apps.proveedores import helpers as helper_proveedor


urlpatterns = patterns('',
    url(r'^listado/$', EmpleadoListView.as_view(),
        name='empleado_listado'),

    url(r'^alta/$', EmpleadoCreate.as_view(),
        name='empleado_alta'),

    url(r'^modi/(?P<pk>[0-9]+)/$',
        EmpleadoUpdate.as_view(),
        name='empleado_update'),

    url(r'^listado_auditoria/$', AuditoriaList.as_view(),
        name='auditoria_listado'),

    url(r'^get_empleado_autocomplete/$', helpers.get_empleado_autocomplete,
        name='get_empleado_autocomplete'),

    url(r'^get_proveedor_autocomplete/$',
        helper_proveedor.get_proveedor_autocomplete,
        name='get_proveedor_autocomplete'),

    url(r'^asignacionformal/alta/(?P<pk>[0-9]+)/$',
        AsignacionFormalCreate.as_view(),
        name='empleado_asignacion_formal_alta'),

    url(r'^asignacionformal/modi/(?P<pk>[0-9]+)/$',
        AsignacionFormalUpdate.as_view(),
        name='empleado_asignacion_formal_modi'),

    url(r'^asignacionformal/delete/(?P<pk>[0-9]+)/$',
        AsignacionFormalDelete.as_view(),
        name='empleado_asignacion_formal_baja'),

    url(r'^get_validar_fechas_historial_asigancion_formal/$',
        helpers.get_validar_fechas_historial_asigancion_formal,
        name='get_validar_fechas_historial_asigancion_formal'),

    url(r'^get_datos_para_select_asignacion_formal/$',
        helpers.get_datos_para_select_asignacion_formal,
        name='get_datos_para_select_asignacion_formal'),

)