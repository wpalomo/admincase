
from django.conf.urls import url
# from apps.tramites import helpers

from .views import (TramiteListView, TramiteCreate, TramiteUpdate,
                    TramiteClienteListView)

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
    url(
        r'^get_requisitos_tipo_tramite/$', helpers.get_requisitos_tipo_tramite,
        name='get_requisitos_tipo_tramite'
    ),
]

