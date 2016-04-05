
from django.conf.urls import patterns, url

from .views import (ClienteListView, ClienteCreate, ClienteUpdate,
                    ClienteDelete) #, ClienteAnsesListView, ClienteCajaListView,
                    # DomiciliosAnidadosAjax)


urlpatterns = patterns('',
    url(r'^listado/$', ClienteListView.as_view(), name='cliente_listado'),
    url(r'^alta/$', ClienteCreate.as_view(), name='cliente_alta'),
    url(r'^modi/(?P<pk>[0-9]+)/$',
        ClienteUpdate.as_view(), name='cliente_update'),
    # url(r'^delete/(?P<pk>[0-9]+)/$',
    #     EmpleadoDelete.as_view(), name='empleado_delete'),
    # url(r'^anses/listado/$', ClienteAnsesListView.as_view(),
    #     name='anses_listado'),
    # url(r'^caja/listado/$', ClienteCajaListView.as_view(),
    #     name='caja_listado'),
    # url(r'^domicilios_ajax/$', DomiciliosAnidadosAjax.as_view()),
)

# url(r'^anses/listado/$', AnsesListView.as_view(), name='anses_listado'),
#     url(r'^anses/modi/(?P<pk>[0-9]+)/$', AnsesUpdate.as_view(), name='anses_modi'),
#     url(r'^caja/listado/$', CajaPrevisionListView.as_view(),
#         name='anses_listado'),
#     url(r'^familia/listado/$', FamiliaListView.as_view(),
#         name='familia_listado'),
#     url(r'^civil_comercial/listado/$', CivilComercialListView.as_view(),
#         name='civil_comercial_listado'),