# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.http import HttpResponse

from apps.empleados.models import EmpleadoEspecialidad
from apps.complementos.salud.models import Especialidad
from apps.seguridad.models import EmpleadoAgenda

from .models import Agenda, AgendaDiaConfiguracion, TipoAgenda


def hay_superposicion_entre_agendas(agenda):

    agendas_listado = Agenda.objects.filter(
        institucion=agenda.institucion,
        profesional=agenda.profesional,
        especialidad=agenda.especialidad
        )

    for agenda_generada in list(agendas_listado):

        if agenda.id == agenda_generada.id:
            continue

        fechas_1 = {
            'fecha_desde': agenda.fecha_desde,
            'fecha_hasta': agenda.fecha_hasta
            }
        fechas_2 = {
            'fecha_desde': agenda_generada.fecha_desde,
            'fecha_hasta': agenda_generada.fecha_hasta
            }

        if hay_superposicion_fecha(fechas_1, fechas_2):
            return True
    else:
        return False


def hay_superposicion_fecha_hora(dia_configuracion):

    listado_dias = AgendaDiaConfiguracion.objects.filter(
        agenda=dia_configuracion.agenda, dia=dia_configuracion.dia)

    for dia in listado_dias:

        if dia_configuracion.id == dia.id:
            continue

        fechas_1 = {
            'fecha_desde': dia_configuracion.fecha_desde,
            'fecha_hasta': dia_configuracion.fecha_hasta
            }
        fechas_2 = {
            'fecha_desde': dia.fecha_desde,
            'fecha_hasta': dia.fecha_hasta
            }

        if hay_superposicion_fecha(fechas_1, fechas_2):
            horas_1 = {
                'hora_desde': dia_configuracion.hora_desde,
                'hora_hasta': dia_configuracion.hora_hasta
                }
            horas_2 = {
                'hora_desde': dia.hora_desde,
                'hora_hasta': dia.hora_hasta
                }

            if hay_superposicion_hora(horas_1, horas_2):
                return True
    else:
        return False


def hay_superposicion_fecha(fechas_1, fechas_2):

    fecha_desde1 = datetime.strptime(str(fechas_1['fecha_desde']), '%Y-%m-%d')
    fecha_hasta1 = datetime.strptime(str(fechas_1['fecha_hasta']), '%Y-%m-%d')

    fecha_desde2 = datetime.strptime(str(fechas_2['fecha_desde']), '%Y-%m-%d')
    fecha_hasta2 = datetime.strptime(str(fechas_2['fecha_hasta']), '%Y-%m-%d')

    if fecha_desde1 <= fecha_hasta2 and fecha_hasta1 >= fecha_desde2:
        return True
    else:
        return False


def hay_superposicion_hora(horas_1, horas_2):

    hora_desde1 = datetime.strptime(
        str(horas_1['hora_desde']), '%H:%M:%S').time()
    hora_hasta1 = datetime.strptime(
        str(horas_1['hora_hasta']), '%H:%M:%S').time()

    hora_desde2 = horas_2['hora_desde']
    hora_hasta2 = horas_2['hora_hasta']

    if hora_desde1 <= hora_hasta2 and hora_hasta1 >= hora_desde2:
        return True
    else:
        return False


def get_especialidad_por_profesional(request):

    profesional_id = request.GET.get('profesional_id')

    try:
        empleado_especialidad = EmpleadoEspecialidad.objects.filter(
            empleado__id=profesional_id)

        result = []

        for registro in list(empleado_especialidad):
            result.append({
                'id': registro.especialidad.id,
                'nombre': registro.especialidad.nombre,
            })
    except:
        result = []

    return HttpResponse(json.dumps(result), content_type='application/json')


def get_cantidad_dias_entre_fechas(fecha_desde, fecha_hasta):
    fecha_desde = datetime.strptime(str(fecha_desde), '%Y-%m-%d')
    fecha_hasta = datetime.strptime(str(fecha_hasta), '%Y-%m-%d')

    resta_fechas = fecha_hasta - fecha_desde
    cantidad_dias = resta_fechas.days

    return cantidad_dias


def get_profesionales_con_agenda(request):

    listado_empleado_agenda = EmpleadoAgenda.objects.all()

    result = []

    for empleado_agenda in listado_empleado_agenda:
        result.append({
            'id': empleado_agenda.empleado.id,
            'nombre': empleado_agenda.empleado.persona.apellido + ', ' +
                      empleado_agenda.empleado.persona.nombre
            })

    return HttpResponse(json.dumps(result), content_type='application/json')


def get_especialidades(request):

    especialidades = Especialidad.objects.all()

    result = []

    for especialidad in especialidades:
        result.append({'id': especialidad.id, 'nombre': especialidad.nombre})

    return HttpResponse(json.dumps(result), content_type='application/json')


def get_tipos_agendas(request):

    tipos_agendas = TipoAgenda.objects.all()

    result = []

    for tipo in tipos_agendas:
        result.append({'id': tipo.id, 'descripcion': tipo.descripcion})

    return HttpResponse(json.dumps(result), content_type='application/json')