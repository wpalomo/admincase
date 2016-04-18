
from django.conf.urls import url
from apps.tramites import helpers

from .views import (TramiteListView, TramiteCreate, TramiteUpdate,
                    TramiteClienteListView) #, AnsesTramitesListView,
                    # CajaPrevisionListView, CajaPrevisionTramitesListView)

from . import helpers


urlpatterns = [
    url(r'^listado/$', TramiteListView.as_view(),
        name='tramite_list'),
    url(r'^listado/(?P<pk>[0-9]+)/$', TramiteClienteListView.as_view(),
        name='tramite_cliente_list'),
    url(r'^alta/$', TramiteCreate.as_view(), name='tramite_add'),
    url(r'^alta/(?P<pk>[0-9]+)/$', TramiteCreate.as_view(), name='tramite_add'),
    url(r'^modi/(?P<pk>[0-9]+)/$', TramiteUpdate.as_view(),
        name='tramite_update'),
    # url(r'^anses/listado/$', AnsesTramitesListView.as_view(), name='anses'),
    # url(r'^anses/requisitos/(?P<pk>[0-9]+)/$', AnsesTramitesListView.as_view(), name='anses'),
    # url(r'^anses/listado/$', AnsesListView.as_view(), name='anses_list'),
    url(r'^alta/anses/$', TramiteCreate.as_view(), name='anses_add'),
    url(r'^modi/anses/(?P<pk>[0-9]+)/$', TramiteUpdate.as_view(),
        name='anses_update'),
    # url(r'^caja/listado/$', CajaPrevisionListView.as_view(),
    #     name='caja_list'),
    # url(r'^caja/requisitos/$', CajaPrevisionTramitesListView.as_view(),
    #     name='anses'),
    url(r'^alta/caja/$', TramiteCreate.as_view(), name='caja_add'),
    url(r'^modi/caja/(?P<pk>[0-9]+)/$', TramiteUpdate.as_view(),
        name='caja_update'),

    url(
        r'^get_requisitos_tipo_tramite/$', helpers.get_requisitos_tipo_tramite,
        name='get_requisitos_tipo_tramite'
    ),
]

