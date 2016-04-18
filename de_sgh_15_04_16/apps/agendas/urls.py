# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import helpers
from .views import (AgendaCreate, AgendaUpdate, AgendaListView,
                    AgendaDiaConfiguracionCreate, AgendaDiaConfiguracionUpdate,
                    AgendaDiaConfiguracionDelete, AgendaFechaDetalleCreate,
                    AgendaFechaDetalleUpdate, AgendaFechaDetalleBloqueoDelete,
                    AgendaDiaConfiguracionBloqueoCreate, AgendaBloqueoCreate,
                    AgendaDiaConfiguracionBloqueoDelete,
                    AgendaPeriodoBloqueoDelete, AgendaExtension)


urlpatterns = patterns('',
    url(r'^alta/$', AgendaCreate.as_view(), name='agenda_alta'),

    url(r'^modi/(?P<pk>[0-9]+)/$',
        AgendaUpdate.as_view(), name='agenda_modificacion'),

    url(r'^listado/$', AgendaListView.as_view(), name='agenda_listado'),

    url(
        r'^configuracion_por_dias/(?P<pk>[0-9]+)/$',
        AgendaDiaConfiguracionCreate.as_view(),
        name='agenda_dia_configuracion_create'
    ),

    url(
        r'^configuracion_por_dias/modi/(?P<pk>[0-9]+)/$',
        AgendaDiaConfiguracionUpdate.as_view(),
        name='agenda_dia_configuracion_update'
    ),

    url(
        r'^configuracion_por_dias/delete/(?P<pk>[0-9]+)/$',
        AgendaDiaConfiguracionDelete.as_view(),
        name='agenda_dia_configuracion_delete'
    ),

    url(
        r'^get_especialidad_por_profesional/',
        helpers.get_especialidad_por_profesional,
        name='get_especialidad_por_profesional'
    ),

    url(
        r'^configuracion_por_fechas/(?P<pk>[0-9]+)/$',
        AgendaFechaDetalleCreate.as_view(),
        name='configuracion_por_fechas_create'
    ),

    url(
        r'^configuracion_por_fechas/modi/(?P<pk>[0-9]+)/$',
        AgendaFechaDetalleUpdate.as_view(),
        name='configuracion_por_fechas_update'
    ),

    url(
        r'^get_profesionales_con_agenda/',
        helpers.get_profesionales_con_agenda,
        name='get_profesionales_con_agenda'
    ),

    url(
        r'^get_especialidades/',
        helpers.get_especialidades,
        name='get_especialidades'
    ),

    url(
        r'^get_tipos_agendas/',
        helpers.get_tipos_agendas,
        name='get_tipos_agendas'
    ),

    url(
        r'^bloqueo/(?P<pk>[0-9]+)/$',
        AgendaBloqueoCreate.as_view(),
        name='agenda_bloqueos'
    ),

    url(
        r'^bloqueo/fecha_detalle/delete/(?P<pk>[0-9]+)/$',
        AgendaFechaDetalleBloqueoDelete.as_view(),
        name='agenda_fecha_detalle_bloqueo_delete'
    ),

    url(
        r'^bloqueo/dia_configuracion/(?P<pk>[0-9]+)/$',
        AgendaDiaConfiguracionBloqueoCreate.as_view(),
        name='agenda_dia_configuracion_bloqueo_create'
    ),

    url(
        r'^bloqueo/dia_configuracion/delete/(?P<pk>[0-9]+)/$',
        AgendaDiaConfiguracionBloqueoDelete.as_view(),
        name='agenda_dia_configuracion_bloqueo_delete'
    ),

    url(
        r'^bloqueo/periodo/delete/(?P<pk>[0-9]+)/$',
        AgendaPeriodoBloqueoDelete.as_view(),
        name='agenda_periodo_bloqueo_delete'
    ),

    url(
        r'^extender/(?P<pk>[0-9]+)/$',
        AgendaExtension.as_view(),
        name='agenda_extension'
    ),

)