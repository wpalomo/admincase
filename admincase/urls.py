"""admincase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .views import autenticarse
from django.conf import settings
from admincase import views

urlpatterns = [
    url(r'^$', autenticarse),
    url(r'^autenticar_usuario/', views.autenticar_usuario),
    url(r'^ayuda/', views.ayuda),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clientes/', include('apps.clientes.urls', namespace='clientes')),
    url(r'^domicilios/', include('apps.domicilios.urls',
                                 namespace='domicilios')),
    url(r'^inicio/', views.inicio),
    url(r'^internos/', views.internos),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, }),
    url(r'^personas/', include('apps.personas.urls', namespace='personas')),
    url(r'^salir/', views.salir),
    url(r'^tramites/', include('apps.tramites.urls', namespace='tramites')),
]

