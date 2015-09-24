
from django.conf.urls import url

from .views import (home, AnsesListView, CajaPrevisionListView, FamiliaListView,
                    CivilComercialListView)


urlpatterns = [
    url(r'^home/$', home, name='tramite_home'),
    url(r'^anses/listado/$', AnsesListView.as_view(), name='anses_listado'),
    url(r'^caja/listado/$', CajaPrevisionListView.as_view(),
        name='anses_listado'),
    url(r'^familia/listado/$', FamiliaListView.as_view(),
        name='familia_listado'),
    url(r'^civil_comercial/listado/$', CivilComercialListView.as_view(),
        name='civil_comercial_listado'),
]

