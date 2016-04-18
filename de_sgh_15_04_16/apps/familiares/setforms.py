

from apps.familiares.models import FamiliarPaciente
from apps.pacientes.models import Paciente
from apps.personas.models import Persona

from . import helpers


class SetMultipleFormsBuscar(object):

    def get_context_data(self, **kwargs):

        context = super(SetMultipleFormsBuscar, self).get_context_data(**kwargs)

        form = self.form_class()
        form_1 = self.form_class_1()
        form_2 = self.form_class_2()
        form_3 = self.form_class_3()

        helpers.deshabilitar_campos(form, form_1, form_2, form_3)

        self.objeto_unico = Persona.objects.get(pk=self.kwargs['id'])
        self.objetos_lista = FamiliarPaciente.objects.filter(
            paciente__persona=self.objeto_unico)

        context['familiares_list'] = self.objetos_lista
        context['persona'] = self.objeto_unico
        context['persona_form'] = form
        context['familiar_form'] = form_1
        context['lugar_nacimiento_form'] = form_2
        context['familiar_paciente_form'] = form_3
        context['mensaje'] = self.mensaje

        return context


class SetMultipleFormsCreate(object):

    def get_context_data(self, **kwargs):

        context = super(SetMultipleFormsCreate, self).get_context_data(**kwargs)

        self.objeto_unico = Persona.objects.get(pk=self.kwargs['id'])
        self.objetos_lista = FamiliarPaciente.objects.filter(
            paciente=Paciente.objects.get(persona=self.objeto_unico))

        form = self.form_class(
            initial={
                'numero_documento':
                    self.request.session['numero_documento_busqueda']
            })

        form_1 = self.form_class_1()
        form_2 = self.form_class_2()
        form_3 = self.form_class_3()

        context['familiares_list'] = self.objetos_lista
        context['persona'] = self.objeto_unico
        context['persona_form'] = form
        context['familiar_form'] = form_1
        context['lugar_nacimiento_form'] = form_2
        context['familiar_paciente_form'] = form_3
        context['mensaje'] = self.mensaje

        return context

