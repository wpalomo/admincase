from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.clientes.models import Cliente
from apps.personas.models import Persona
from apps.tramites.models import Tramite


def home(request):
    if request.user.is_authenticated():
        return render(request, 'tramites/home.html')


class AnsesListView(ListView):
    queryset = Tramite.objects.filter(entidad__id=1)
    context_object_name = 'cliente_anses'
    template_name = 'tramites/tramite_anses_list.html'
    paginate_by = 10


class CajaPrevisionListView(ListView):
    queryset = Tramite.objects.filter(entidad__id=2)
    context_object_name = 'cliente_caja'
    template_name = 'tramites/tramite_caja_list.html'
    paginate_by = 10


class FamiliaListView(ListView):
    model = Cliente
    paginate_by = 10


class CivilComercialListView(ListView):
    model = Cliente
    paginate_by = 10

