from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.clientes.models import Cliente
from apps.personas.models import Persona
from apps.tramites.models import Tramite, TipoTramite


def home(request):
    if request.user.is_authenticated():
        return render(request, 'tramites/home.html')


class AnsesListView(ListView):
    model = Cliente
    context_object_name = 'cliente_anses'
    template_name = 'tramites/tramite_anses_list.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(AnsesListView, self).get_context_data(*args, **kwargs)
        context['tipo_tramite_anses'] = Tramite.objects.filter(entidad__id=1)
        return context


class CajaPrevisionListView(ListView):
    queryset = Tramite.objects.filter(entidad__id=2)
    context_object_name = 'cliente_caja'
    template_name = 'tramites/tramite_caja_list.html'
    paginate_by = 10


class FamiliaListView(ListView):
    model = Cliente
    template_name = 'tramites/tramite_familia_list.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(FamiliaListView, self).get_context_data(*args, **kwargs)
        context['tipo_tramite_familia'] = Tramite.objects.filter(entidad__id=3)
        return context


class CivilComercialListView(ListView):
    queryset = Tramite.objects.filter(entidad__id=4)
    context_object_name = 'cliente_civil_comercial'
    template_name = 'tramites/tramite_civilcomercial_list.html'
    paginate_by = 10

