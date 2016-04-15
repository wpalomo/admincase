
from django.views.generic import CreateView, ListView, UpdateView
from apps.seguridad.mixins import LoginRequiredMixin
from .models import Institucion
from .forms import InstitucionForm


class InstitucionCreate(LoginRequiredMixin, CreateView):

    model = Institucion
    form_class = InstitucionForm
    success_url = '/instituciones/listado'


class InstitucionList(LoginRequiredMixin, ListView):

    model = Institucion
    paginate_by = 10

    def get_queryset(self):

        queryset = super(InstitucionList, self).get_queryset()

        if 'combo_busqueda' in self.request.GET:

            if 'input_buscar' in self.request.GET:

                queryset = Institucion.objects.all()

                buscar = self.request.GET.get('input_buscar')

                if self.request.GET.get('input_buscar'):

                    if self.request.GET.get('combo_busqueda') == 'nombre':

                        queryset = Institucion.objects.filter(
                            nombre__icontains=buscar)

                    if self.request.GET.get('combo_busqueda') == 'codigo':

                        queryset = Institucion.objects.filter(
                            pk__icontains=int(buscar))

        return queryset


class InstitucionUpdate(UpdateView):

    model = Institucion
    form_class = InstitucionForm
    success_url = '/instituciones/listado'