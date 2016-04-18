
import json

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.complementos.salud.models import UnidadMedida

from . import helpers
from .forms import (MedicamentoForm, MedicamentoLaboratorioForm)
from .models import (Medicamento, MedicamentoLineaTerapeutica, Composicion,
                     PrincipioActivo, LineaTerapeutica, AdministracionForma,
                     ViaAdministracion, FormaFarmaceutica,
                     MedicamentoLaboratorio)


class MedicamentoCreate(CreateView):

    model = Medicamento
    form_class = MedicamentoForm

    def post(self, request, *args, **kwargs):

        form = MedicamentoForm(data=self.request.POST)

        if form.is_valid():
            medicamento = form.save()

            datos_composicion = \
                json.loads(self.request.POST['items_composicion'])
            datos_linea_terapeutica = \
                json.loads(self.request.POST['items_linea_terapeutica'])
            datos_administracion_forma = \
                json.loads(self.request.POST['items_administracion_forma'])

            if len(datos_composicion) > 0:
                self.guardar_items_composicion(datos_composicion, medicamento)

            if len(datos_linea_terapeutica) > 0:
                self.guardar_items_linea_terapeutica(
                    datos_linea_terapeutica, medicamento)

            if len(datos_administracion_forma) > 0:
                self.guardar_items_administracion_forma(
                    datos_administracion_forma, medicamento)

            self.guardar_numeros_autoincrementales(medicamento)

            messages.add_message(
                request, messages.SUCCESS, 'MEDICAMENTO CREADO CON EXITO')

            return HttpResponseRedirect(
                '/medicamentos/modi/' + str(form.instance.id))

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'medicamentos/medicamento_form.html',
            {'form': form},
            context_instance=RequestContext(request)
        )

    def guardar_items_composicion(self, datos, medicamento):

        for item in datos:
            principio_activo = PrincipioActivo.objects.get(
                descripcion=item['principio_activo'])
            potencia_numerador = item['potencia_numerador'].split()
            unidad_medida_numerador = UnidadMedida.objects.get(
                descripcion=potencia_numerador[1])

            potencia_denominador = item['potencia_denominador'].split()
            unidad_medida_denominador = UnidadMedida.objects.get(
                descripcion=potencia_denominador[1])

            Composicion.objects.create(
                medicamento=medicamento,
                principio_activo=principio_activo,
                potencia_numerador=potencia_numerador[0],
                unidad_medida_numerador=unidad_medida_numerador,
                potencia_denominador=potencia_denominador[0],
                unidad_medida_denominador=unidad_medida_denominador
            )

    def guardar_items_linea_terapeutica(self, datos, medicamento):

        for item in datos:
            linea_terapeutica = LineaTerapeutica.objects.get(
                descripcion=item['linea_terapeutica'])

            MedicamentoLineaTerapeutica.objects.create(
                medicamento=medicamento,
                linea_terapeutica=linea_terapeutica
            )

    def guardar_items_administracion_forma(self, datos, medicamento):

        for item in datos:
            via_administracion = ViaAdministracion.objects.get(
                descripcion=item['via_administracion'])

            forma_farmaceutica = FormaFarmaceutica.objects.get(
                descripcion=item['forma_farmaceutica'])

            AdministracionForma.objects.create(
                medicamento=medicamento,
                via_administracion=via_administracion,
                forma_farmaceutica=forma_farmaceutica
            )

    def guardar_numeros_autoincrementales(self, medicamento):

        listado = {'MEDICAMENTO': medicamento.codigo}

        helpers.registrar_numeros_autoincrementales(listado)


class MedicamentoUpdate(UpdateView):

    model = Medicamento
    form_class = MedicamentoForm

    def get(self, request, *args, **kwargs):

        medicamento = Medicamento.objects.get(pk=kwargs['pk'])
        form = MedicamentoForm(instance=medicamento)

        return render_to_response(
            'medicamentos/medicamento_form.html',
            {
                'form': form,
                'medicamento': medicamento
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        medicamento = Medicamento.objects.get(pk=kwargs['pk'])

        form = MedicamentoForm(self.request.POST, instance=medicamento)

        if form.is_valid():

            medicamento = form.save()

            datos_composicion = \
                json.loads(self.request.POST['items_composicion'])

            datos_linea_terapeutica = \
                json.loads(self.request.POST['items_linea_terapeutica'])

            datos_administracion_forma = \
                json.loads(self.request.POST['items_administracion_forma'])

            self.guardar_items_composicion(datos_composicion, medicamento)

            self.guardar_items_linea_terapeutica(
                datos_linea_terapeutica, medicamento)

            self.guardar_items_administracion_forma(
                datos_administracion_forma, medicamento)

            messages.add_message(
                request, messages.SUCCESS, 'MEDICAMENTO MODIFICADO CON EXITO')

            return HttpResponseRedirect(self.get_success_url())

        messages.add_message(
            request, messages.ERROR, 'EL FORMULARIO CONTIENE ERRORES')

        return render_to_response(
            'expedientes/expediente_form.html',
            {'form': form, 'medicamento': medicamento},
            context_instance=RequestContext(request)
        )

    def guardar_items_composicion(self, datos, medicamento):
        for item in datos:
            principio_activo = PrincipioActivo.objects.get(
                descripcion=item['principio_activo'])
            potencia_numerador = item['potencia_numerador'].split()
            unidad_medida_numerador = UnidadMedida.objects.get(
                descripcion=potencia_numerador[1])

            potencia_denominador = item['potencia_denominador'].split()
            unidad_medida_denominador = UnidadMedida.objects.get(
                descripcion=potencia_denominador[1])

            composicion_medicamento = \
                Composicion.objects.filter(medicamento=medicamento)

            if len(composicion_medicamento) >= 0:

                composicion_principio_activo_ids = [
                    id_principio_activo.principio_activo.id
                    for id_principio_activo in composicion_medicamento
                ]

                if principio_activo.id not in composicion_principio_activo_ids:
                    Composicion.objects.create(
                        medicamento=medicamento,
                        principio_activo=principio_activo,
                        potencia_numerador=potencia_numerador[0],
                        unidad_medida_numerador=unidad_medida_numerador,
                        potencia_denominador=potencia_denominador[0],
                        unidad_medida_denominador=unidad_medida_denominador
                    )

    def guardar_items_linea_terapeutica(self, datos, medicamento):

        for item in datos:
            linea_terapeutica = LineaTerapeutica.objects.get(
                descripcion=item['linea_terapeutica'])

            linea_terapeutica_medicamento = \
                MedicamentoLineaTerapeutica.objects.filter(
                    medicamento=medicamento)

            if len(linea_terapeutica_medicamento) >= 0:

                lineas_terapeuticas_ids = [
                    id_lineas_terapeuticas.linea_terapeutica.id
                    for id_lineas_terapeuticas in linea_terapeutica_medicamento
                ]

                if linea_terapeutica.id not in lineas_terapeuticas_ids:

                    MedicamentoLineaTerapeutica.objects.create(
                        medicamento=medicamento,
                        linea_terapeutica=linea_terapeutica
                    )

    def guardar_items_administracion_forma(self, datos, medicamento):

        datos_a_tupla = []
        vias_administracion_forma = []

        via_administracion_medicamento = \
                AdministracionForma.objects.filter(medicamento=medicamento)

        if len(via_administracion_medicamento) >= 0:

            for via in via_administracion_medicamento:
                vias_administracion_forma.append(
                    (via.via_administracion.id, via.forma_farmaceutica.id))

            for item in datos:
                via_administracion = ViaAdministracion.objects.get(
                    descripcion=item['via_administracion'])

                forma_farmaceutica = FormaFarmaceutica.objects.get(
                    descripcion=item['forma_farmaceutica'])

                datos_a_tupla.append(
                    (via_administracion.id, forma_farmaceutica.id))

            items = set(datos_a_tupla) - set(vias_administracion_forma)

            if len(items) > 0:
                for item in items:
                    via_administracion_item = \
                        ViaAdministracion.objects.get(pk=item[0])

                    forma_farmaceutica_item = \
                        FormaFarmaceutica.objects.get(pk=item[1])

                    AdministracionForma.objects.create(
                        medicamento=medicamento,
                        via_administracion=via_administracion_item,
                        forma_farmaceutica=forma_farmaceutica_item
                    )

    def get_success_url(self):
        return self.request.get_full_path()


class MedicamentoListView(ListView):

    model = Medicamento
    paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super(MedicamentoListView, self).get_context_data(**kwargs)
    #     context['estados'] = Estado.objects.all()
    #     context['empleado_solicitante'] = Empleado.objects.all()
    #
    #     return context

    # def get_queryset(self):
    #
    #     query = super(MedicamentoListView, self).get_queryset()
    #
    #     parametro1 = self.request.GET.get('parametro1')
    #     parametro2 = self.request.GET.get('parametro2')
    #
    #     if self.request.GET.get('filtro') == 'NUMERO_EXPEDIENTE':
    #
    #         query = self.buscar_por_numero(parametro1, parametro2)
    #
    #     if self.request.GET.get('filtro') == 'NUMERO_RESOLUCION_PAGO':
    #
    #         query = self.buscar_por_numero_resolucion_pago(parametro1)
    #
    #     if self.request.GET.get('filtro') == 'FECHA_EXPEDIENTE':
    #
    #         query = self.buscar_por_fecha_expediente(
    #             parametro1, parametro2)
    #
    #     if self.request.GET.get('filtro') == 'FECHA_RESOLUCION_PAGO':
    #
    #         query = self.buscar_por_fecha_resolucion_pago(
    #             parametro1, parametro2)
    #
    #     if self.request.GET.get('filtro') == 'ESTADO':
    #
    #         query = self.buscar_por_estado(
    #             self.request.GET.get('estado'))
    #
    #     if self.request.GET.get('filtro') == 'SOLICITANTE':
    #
    #         query = self.buscar_por_empleado_solicitante(
    #             self.request.GET.get('solicitante'))
    #
    #     return query
    #
    # def buscar_por_numero(self, numero, anio):
    #
    #     numero = numero.strip()
    #     anio = anio.strip()
    #
    #     medicamentos = Medicamento.objects.filter(
    #         numero=numero,
    #         anio__icontains=anio
    #     )
    #
    #     return medicamentos
    #
    # def buscar_por_estado(self, estado):
    #
    #     expedientes = Expediente.objects.filter(
    #         estado__descripcion__icontains=estado)
    #
    #     return expedientes
    #
    # def buscar_por_empleado_solicitante(self, empleadoId):
    #
    #     expedientes = Expediente.objects.filter(
    #         empleado_solicitante__persona=empleadoId
    #     )
    #
    #     # expedientes = Expediente.objects.filter(
    #     #     Q(empleado_solicitante__persona__apellido__icontains=empleado) |
    #     #     Q(empleado_solicitante__persona__nombre__icontains=empleado)
    #     # )
    #
    #     return expedientes


class MedicamentoLaboratorioCreate(CreateView):

    model = MedicamentoLaboratorio
    form_class = MedicamentoLaboratorioForm
    # template_name = 'medicamentos/medicamentolaboratorio_form.html'

    def get(self, request, *args, **kwargs):

        medicamento = Medicamento.objects.get(pk=self.kwargs['pk'])
        medicamento_laboratorio_form = MedicamentoLaboratorioForm()
        laboratorio = MedicamentoLaboratorio.objects.filter(
            medicamento=self.kwargs['pk'])
        return render_to_response(
            'medicamentos/medicamentolaboratorio_form.html',
            {
                'laboratorios_list': laboratorio,
                'form': medicamento_laboratorio_form,
                'medicamento': medicamento
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, *args, **kwargs):

        medicamento_id = self.kwargs['pk']
        medicamento_laboratorio_form = MedicamentoLaboratorioForm(
            helpers.set_id_medicamento(self.request, medicamento_id),
            self.request.FILES)

        medicamento_laboratorio_form.medicamento = self.kwargs['pk']

        if medicamento_laboratorio_form.is_valid():

            medicamento_laboratorio_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'EL LABORATORIO SE REGISTRO CON EXITO')
            return HttpResponseRedirect('/medicamentos/laboratorios/alta/' +
                                        str(medicamento_id))
        else:

            medicamento_laboratorio = MedicamentoLaboratorio.objects.filter(
                medicamento=medicamento_id)

            medicamento = Medicamento.objects.get(pk=self.kwargs['pk'])

            return render_to_response(
                'medicamentos/medicamentolaboratorio_form.html',
                {
                    'laboratorios_list': medicamento_laboratorio,
                    'form': medicamento_laboratorio_form,
                    'medicamento': medicamento
                },
                context_instance=RequestContext(request)
            )


class MedicamentoLaboratorioUpdate(UpdateView):

        model = MedicamentoLaboratorio
        form_class = MedicamentoLaboratorioForm
        # template_name = 'medicamentos/medicamentolaboratorio_form.html'

        def get_context_data(self, **kwargs):
            context = super(MedicamentoLaboratorioUpdate, self).\
                get_context_data(**kwargs)

            medicamento_laboratorio = MedicamentoLaboratorio.objects.filter(
                medicamento=self.object.medicamento.id)
            context['laboratorios_list'] = medicamento_laboratorio
            context['medicamento'] = self.object.medicamento
            return context

        def post(self, request, *args, **kwargs):

            medicamento_laboratorio_id = self.kwargs['pk']
            medicamento_laboratorio = MedicamentoLaboratorio.objects.get(
                pk=medicamento_laboratorio_id)

            medicamento_laboratorio_form = \
                MedicamentoLaboratorioForm(helpers.set_id_medicamento(
                    self.request, medicamento_laboratorio.medicamento.id),
                    self.request.FILES,
                    instance=medicamento_laboratorio)

            if medicamento_laboratorio_form.is_valid():
                medicamento_laboratorio_form.save()
                messages.add_message(
                                request, messages.SUCCESS,
                                'EL LABORATORIO SE MODIFICO CON EXITO')
                return HttpResponseRedirect('/medicamentos/laboratorios/modi/' +
                                            str(medicamento_laboratorio.id))
            else:

                medicamento = Medicamento.objects.get(
                    pk=medicamento_laboratorio.medicamento.id)
                medicamento_laboratorio = MedicamentoLaboratorio.objects.filter(
                    medicamento=medicamento_laboratorio.medicamento)

                return render_to_response(
                    'medicamentos/medicamentolaboratorio_form.html',
                    {
                        'laboratorios_list': medicamento_laboratorio,
                        'form': medicamento_laboratorio_form,
                        'medicamento': medicamento
                    },
                    context_instance=RequestContext(request)
                )


class MedicamentoLaboratorioDelete(DeleteView):

    model = MedicamentoLaboratorio

    def get_success_url(self):

        medicamento = Medicamento.objects.get(
            pk=MedicamentoLaboratorio.objects.get(
                pk=self.kwargs['pk']).medicamento.id)
        messages.add_message(self.request, messages.SUCCESS,
                                 'Se ha eliminado la asignación')
        return '/medicamentos/laboratorios/alta/' + str(medicamento.pk)
