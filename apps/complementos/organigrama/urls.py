
from django.conf.urls import patterns, url

from .views import (EntidadListView, EntidadCreate, EntidadUpdate,
                    EntidadDelete)


urlpatterns = patterns('',
    url(r'^listado/$', EntidadListView.as_view(), name='entidad_listado'),
    url(r'^alta/$', EntidadCreate.as_view(), name='entidad_alta'),
    url(r'^modi/(?P<pk>[0-9]+)/$', EntidadUpdate.as_view(),
        name='entidad_update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', EntidadDelete.as_view(),
        name='entidad_delete'),
)