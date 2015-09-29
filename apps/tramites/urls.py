
from django.conf.urls import url

from .views import (home, AnsesListView, AnsesUpdate,
                    CajaPrevisionListView, FamiliaListView,
                    CivilComercialListView)


urlpatterns = [
    url(r'^home/$', home, name='tramite_home'),
    url(r'^anses/listado/$', AnsesListView.as_view(), name='anses_listado'),
    url(r'^anses/modi/(?P<pk>[0-9]+)/$', AnsesUpdate.as_view(), name='anses_modi'),
    url(r'^caja/listado/$', CajaPrevisionListView.as_view(),
        name='anses_listado'),
    url(r'^familia/listado/$', FamiliaListView.as_view(),
        name='familia_listado'),
    url(r'^civil_comercial/listado/$', CivilComercialListView.as_view(),
        name='civil_comercial_listado'),
]

