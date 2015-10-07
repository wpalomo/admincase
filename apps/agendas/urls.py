# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import AgendaCreate


urlpatterns = patterns('',
                       url(r'^alta/$', AgendaCreate.as_view(), name='agenda_alta'),
                       )

