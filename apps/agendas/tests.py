
from django.test import TestCase
from .models import Agenda, AgendaCalendario, TipoAgenda
from apps.empleados.models import Empleado
from apps.personas.models import Persona
import datetime

class SimpleTest(TestCase):

    def test_print_asignar_calendario(self):

        persona1 = Persona.objects.create(
            nombre="pepe",
            apellido="perez"
        )

        empleado = Empleado.objects.create(
            persona=persona1,
            cuil="23-30194000-9"
        )

        tipo_agenda = TipoAgenda.objects.create(
            descripcion = 'inmediata',

        )

        agenda1 =Agenda.objects.create(
            empleado = empleado,
            fecha_desde = '2015-08-02',
            fecha_hasta = '2015-08-08',
            estado = 1,
            tipo_agenda = tipo_agenda
        )

        f1 = datetime.date(2015, 8, 2)

        #f2 = datetime('07/01/2015')
        d = 7
        datelist = []
        agenda_calendario_list = []

        for x in range(0, d):
            datelist.append(f1 + datetime.timedelta(days = x))

            agenda_calendario_list.append(AgendaCalendario.objects.create(
                agenda = agenda1,
                fecha = f1 + datetime.timedelta(days = x),
                bloqueado = 0
            ))
        #agenda1.agenda_set = agenda_calendario_list
        print ("------------")
        print (datelist)
        print ("------------")
        print (agenda_calendario_list)
        print ("------------")




        # agendas_calendarios
        #
        # personas = Persona.objects.all()
        # empleados = Empleado.objects.all()
        #
        # print(personas)
        # print(empleados)
        # print(areas)
        #
        # print("###")
        #
        # ar1 = Area.objects.get(pk=1)
        #
        # print(ar1)
        #
        # print("###")
        #
        # print(ar1.empleado_set.all())  ## DESDE AREA 1 - IMPRIMO TODOS SUS
        # # EMPLEADOS
        #
        # print("###")
        #
        # print(Empleado.objects.filter(area__id=1))  ## DESDE LOS EMPLEADOS
        # # IMPRIMO SOLO LOS QUE PERTENCEN A AREA 1