
from django.conf.urls import url

from .views import (TramiteListView, TramiteCreate, TramiteUpdate,
                    TramiteClienteListView, AnsesListView,
                    AnsesCreate, AnsesUpdate, CajaPrevisionListView,
                    CajaPrevisionCreate, CajaPrevisionUpdate)


urlpatterns = [
    url(r'^listado/$', TramiteListView.as_view(),
        name='tramite_list'),
    url(r'^listado/(?P<pk>[0-9]+)/$', TramiteClienteListView.as_view(),
        name='tramite_cliente_list'),
    url(r'^alta/$', TramiteCreate.as_view(), name='tramite_add'),
    url(r'^alta/(?P<pk>[0-9]+)/$', TramiteCreate.as_view(), name='tramite_add'),
    url(r'^modi/(?P<pk>[0-9]+)/$', TramiteUpdate.as_view(),
        name='tramite_update'),
    url(r'^anses/listado/$', AnsesListView.as_view(), name='anses_list'),
    url(r'^anses/alta/$', AnsesCreate.as_view(), name='anses_add'),
    url(r'^anses/modi/(?P<pk>[0-9]+)/$', AnsesUpdate.as_view(),
        name='anses_update'),
    url(r'^caja/listado/$', CajaPrevisionListView.as_view(),
        name='caja_list'),
    url(r'^caja/alta/$', CajaPrevisionCreate.as_view(), name='caja_add'),
    url(r'^caja/modi/(?P<pk>[0-9]+)/$', CajaPrevisionUpdate.as_view(),
        name='caja_update'),
#     url(r'^familia/listado/$', FamiliaListView.as_view(),
#         name='familia_listado'),
#     url(r'^civil_comercial/listado/$', CivilComercialListView.as_view(),
#         name='civil_comercial_listado'),
]

