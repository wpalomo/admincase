# -*- encoding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.helpers.FormsetMixing import FormsetMixing
from apps.personas.models import Persona
from .forms import PersonaForm, EmpleadoFormSet
from .models import Empleado


class EmpleadoCreate(FormsetMixing, CreateView):
    model = Persona
    form_class = PersonaForm
    formset_class = EmpleadoFormSet


class EmpleadoUpdate(FormsetMixing, UpdateView):
    model = Persona
    form_class = PersonaForm
    formset_class = EmpleadoFormSet


class EmpleadoListView(ListView):
    model = Empleado


class EmpleadoDelete(DeleteView):
    model = Empleado
    success_url = '/empleados/listado/'

    def delete(self, request, *args, **kwargs):
        return super(EmpleadoDelete, self).delete(request, *args, **kwargs)
