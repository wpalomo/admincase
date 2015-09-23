
from django.conf.urls import patterns, url

from .views import (ClienteListView, ClienteCreate, ClienteUpdate,
                    ClienteDelete)


urlpatterns = patterns('',
    url(r'^listado/$', ClienteListView.as_view(), name='cliente_listado'),
    url(r'^alta/$', ClienteCreate.as_view(), name='cliente_alta'),
    url(r'^modi/(?P<pk>[0-9]+)/$',
        ClienteUpdate.as_view(), name='cliente_update'),
    # url(r'^delete/(?P<pk>[0-9]+)/$',
    #     EmpleadoDelete.as_view(), name='empleado_delete'),
)

