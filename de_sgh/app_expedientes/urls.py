# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import helpers
from .views import (ExpedienteListView, ExpedienteCreate, ExpedienteUpdate,
                    ExpedienteResolucionCreate, ExpedienteResolucionUpdate,
                    ExpedienteDisposicionCreate, ExpedienteDisposicionUpdate,
                    ExpedienteServicioMedicoCreate,
                    ExpedienteServicioMedicoUpdate, ExpedienteLicitacionCreate,
                    ExpedienteLicitacionUpdate, ExpedienteComodatoCreate,
                    ExpedienteComodatoUpdate)


urlpatterns = patterns('',
    url(r'^alta/$', ExpedienteCreate.as_view(), name='expediente_alta'),

    url(r'^modi/(?P<pk>[0-9]+)/$',
        ExpedienteUpdate.as_view(), name='expediente_modi'),

    url(r'^listado/$', ExpedienteListView.as_view(), name='expediente_listado'),

    url(
        r'^resolucion/alta/(?P<pk>[0-9]+)/$',
        ExpedienteResolucionCreate.as_view(),
        name='expediente_resolucion_create'
    ),

    url(
        r'^resolucion/modi/(?P<pk>[0-9]+)/$',
        ExpedienteResolucionUpdate.as_view(),
        name='expediente_resolucion_update'
    ),

    url(r'^disposicion/alta/(?P<pk>[0-9]+)/$',
        ExpedienteDisposicionCreate.as_view(),
        name='expediente_disposicion_update'
    ),

    url(r'^disposicion/modi/(?P<pk>[0-9]+)/$',
        ExpedienteDisposicionUpdate.as_view(),
        name='expediente_disposicion_update'
    ),

    url(r'^get_tipo_transaccion/',
        helpers.get_tipo_transaccion,
        name='get_tipo_transaccion'
    ),

    url(r'^get_etapa/', helpers.get_etapa, name='get_etapa'),

    url(
        r'^get_estado_valor/',
        helpers.get_estado_valor,
        name='get_estado_valor'
    ),

    url(r'^get_valores_iniciales/',
        helpers.get_valores_iniciales,
        name='get_valores_iniciales'
    ),

    url(r'^disposicion/get_tipo_transaccion_disposicion/$',
       helpers.get_tipo_transaccion_disposicion,
       name='get_tipo_transaccion_disposicion'
    ),

    url(
        r'^servicio_medico/alta/(?P<pk>[0-9]+)/$',
        ExpedienteServicioMedicoCreate.as_view(),
        name='expediente_serviciomedico_create'
    ),

    url(
        r'^servicio_medico/modi/(?P<pk>[0-9]+)/$',
        ExpedienteServicioMedicoUpdate.as_view(),
        name='expediente_serviciomedico_update'
    ),

    url(
        r'^licitacion/alta/(?P<pk>[0-9]+)/$',
        ExpedienteLicitacionCreate.as_view(),
        name='expediente_licitacion_create'
    ),

    url(
        r'^licitacion/modi/(?P<pk>[0-9]+)/$',
        ExpedienteLicitacionUpdate.as_view(),
        name='expediente_licitacion_update'
    ),

    url(
        r'^comodato/alta/(?P<pk>[0-9]+)/$',
        ExpedienteComodatoCreate.as_view(),
        name='expediente_comodato_create'
    ),

    url(
        r'^comodato/ajax/',
        ExpedienteComodatoCreate.as_view(),
        name='expediente_comodato_create'
    ),

    url(
        r'^comodato/modi/(?P<pk>[0-9]+)/$',
        ExpedienteComodatoUpdate.as_view(),
        name='expediente_comodato_update'
    ),

    url(r'^licitacion/get_numero_ingreso_manual_es_valido/$',
       helpers.get_numero_ingreso_manual_es_valido,
       name='numero_ingreso_manual_es_valido'
    )

)