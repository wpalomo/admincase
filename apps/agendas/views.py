from django.views.generic import CreateView
from django.shortcuts import render

from .models import Agenda
from .forms import AgendaForm


class AgendaCreate(CreateView):

    model = Agenda
    form_class = AgendaForm
    template_name = 'agendas/agenda_form.html'
    success_url = '/'