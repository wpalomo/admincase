# -*- encoding: utf-8 -*-
import json
from PIL import Image
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.core import serializers


from apps.complementos.organigrama.models import (Cargo, Direccion, Departamento, Division, Servicio, Seccion)
from apps.instituciones.models import Institucion
from .models import Empleado, AsignacionFormal


def cambiar_nombre_imagen(nombre_foto, numero_documento_persona):

    fecha = datetime.today()
    extension = nombre_foto.split('.')[-1]

    fecha_hora_texto = str(fecha.year) + str(fecha.month) + \
                       str(fecha.day) + str(fecha.hour) + \
                       str(fecha.minute) + str(fecha.second)

    nombre = "foto_personal/{documento}_{fecha_nombre}.{ext}".format(
        documento=numero_documento_persona, fecha_nombre=fecha_hora_texto,
        ext=extension)

    return nombre


def redimensionar_imagen(foto, nombre_foto):

    imagen = Image.open(foto)
    # Imagen para Abrir

    resolucion_normal = (300, 400)
    resolucion_miniatura = (100, 100)

    # Ingresa el size de la imagen para poder comparar y darle porcentajes
    alto_tamanio_maximo = 300
    ancho_tamanio_maximo = 400
    alto_original = imagen.size[0]
    ancho_original = imagen.size[1]
    if alto_tamanio_maximo < alto_original:

        alto_tamanio = alto_original - (alto_original - alto_tamanio_maximo)

        alto_porcentaje = (alto_original - alto_tamanio_maximo) \
                           * 100 / alto_original
        ancho_tamanio = ancho_original - (ancho_original *
                                          alto_porcentaje)/100

        resolucion_normal = (int(alto_tamanio), int(ancho_tamanio))

    elif ancho_tamanio_maximo < ancho_original:
        ancho_tamanio = ancho_original - (ancho_original - ancho_tamanio_maximo)

        ancho_porcentaje = (ancho_original - ancho_tamanio_maximo) \
                            * 100 / ancho_original

        alto_tamanio = alto_original - (alto_original *
                                        ancho_porcentaje)/100

        resolucion_normal = (int(alto_tamanio), int(ancho_tamanio))

    imagen_normal = imagen.resize(resolucion_normal, Image.ANTIALIAS)
    imagen_miniatura = imagen.resize(resolucion_miniatura, Image.ANTIALIAS)

    ubicacion_foto_normal = \
        foto.path.rsplit('/', 1)[0] + '/foto_personal/normal/' + nombre_foto
    ubicacion_foto_miniatura = \
        foto.path.rsplit('/', 1)[0] + '/foto_personal/miniatura/' + nombre_foto

    imagen_normal.save(ubicacion_foto_normal)
    imagen_miniatura.save(ubicacion_foto_miniatura)

    foto = nombre_foto

    return foto


def get_empleado_autocomplete(request):
    data = []
    # empleados = Empleado.objects.filter(
    #     persona__apellido__startswith=request.GET.get('query'))
    # PARA QUE TRAIGA SOLO LOS EMPLEADOS SIN FECHA DE EGRESO
    # empleados = Empleado.objects.filter(
    #     persona__apellido__startswith=request.GET.get('query')).exclude(
    #     fecha_egreso__isnull=False)

    # PARA QUE BUSQUE POR TEXTO O POR CODIGO

    try:  # POR CODIGO
        empleados = Empleado.objects.filter(pk=int(request.GET.get('query'))).exclude(
            fecha_egreso__isnull=False)

    except:  # POR TEXTO
        empleados = Empleado.objects.filter(
            persona__apellido__icontains=request.GET.get('query')).exclude(
            fecha_egreso__isnull=False)

    if len(empleados) > 0:
        for empleado in empleados:
            data.append({"data": str(empleado.id), "value": str(empleado)})

        result = '{"query": "Unit","suggestions":'+json.dumps(data)+'}'
    else:
        data.append("No existe resultado")
        result = '{"query": "Unit","suggestions":'+json.dumps(data)+'}'

    return HttpResponse(result)


def get_validar_fechas_historial_asigancion_formal(request):

    empleado_id = request.GET.get('empleado')
    asignacion_id = request.GET.get('asignacion')
    fecha_desde = request.GET.get('fecha_desde')

    if asignacion_id:
        asignaciones = AsignacionFormal.objects.filter(
            empleado__id=int(empleado_id))\
            .exclude(pk=asignacion_id).values('fecha_hasta')
    else:
        asignaciones = AsignacionFormal.objects.filter(
            empleado__id=int(empleado_id)).values('fecha_hasta')

    if len(asignaciones) == 0:
        result = {'msj': 0}
        return HttpResponse(json.dumps(result), content_type='application/json')

    try:
        fecha_desde_format = datetime.strptime(
            str(fecha_desde), '%d/%m/%Y').date()

        for fecha_hasta_asignacion_formal in asignaciones:
            if fecha_desde_format <= fecha_hasta_asignacion_formal[
                    'fecha_hasta']:

                result = {'msj': 1}
                return HttpResponse(json.dumps(result),
                                    content_type='application/json')
                # print('hay uno')

        result = {'msj': 0}
        # print('no hay ninguno')
    except:
        result = {'msj': 99}

    return HttpResponse(json.dumps(result), content_type='application/json')


tablas = {
    'institucion': Institucion,
    'cargo': Cargo,
    'direccion': Direccion,
    'departamento': Departamento,
    'division': Division,
    'servicio': Servicio,
    'seccion': Seccion
}


def get_datos_para_select_asignacion_formal(request):
    id_padre = request.GET.get('id')
    tabla = request.GET.get('tabla')

    if tabla == "institucion":
        cargos = tablas['cargo'].objects.filter(institucion__id=int(id_padre))

        array_cargos = [{'id': cargo.id, 'value': cargo.descripcion}
                        for cargo in cargos]

        array_cargos.insert(0, {'id': '', 'value': '---------'})

        direcciones = tablas['direccion'].objects.filter(
            institucion__id=int(id_padre))

        array_direcciones = [
            {'id': direccion.id, 'value': direccion.descripcion}
            for direccion in direcciones
        ]

        array_direcciones.insert(0, {'id': '', 'value': '---------'})

        divisiones = tablas['division'].objects.filter(
            institucion__id=int(id_padre))

        array_divisiones = [
            {'id': division.id, 'value': division.descripcion}
            for division in divisiones
        ]

        array_divisiones.insert(0, {'id': '', 'value': '---------'})

        servicios = tablas['servicio'].objects.filter(
            institucion__id=int(id_padre))

        array_servicios = [
            {'id': servicio.id, 'value': servicio.descripcion}
            for servicio in servicios
        ]

        array_servicios.insert(0, {'id': '', 'value': '---------'})

        secciones = tablas['seccion'].objects.filter(
            institucion__id=int(id_padre))

        array_secciones = [
            {'id': seccion.id, 'value': seccion.descripcion}
            for seccion in secciones
        ]

        array_secciones.insert(0, {'id': '', 'value': '---------'})

        query = {
            'cargos': array_cargos,
            'direcciones': array_direcciones,
            'divisiones': array_divisiones,
            'servicios': array_servicios,
            'secciones': array_secciones
        }

        return HttpResponse(json.dumps(query), content_type='application/json')

    if tabla == "departamento":
        # departamentos de la direccion_id seleccionada
        datos = tablas[tabla].objects.filter(direccion__id=int(id_padre))

    # if tabla == "division":
    #     # divisiones del departamento_id seleccionada
    #     datos = tablas[tabla].objects.filter(departamento__id=int(id_padre))
    #
    # if tabla == "servicio":
    #     # servicios de la division_id seleccionada
    #     datos = tablas[tabla].objects.filter(division__id=int(id_padre))
    #
    # if tabla == "seccion":
    #     # secciones del servicio_id seleccionada
    #     datos = tablas[tabla].objects.filter(servicio__id=int(id_padre))

    array_datos = [
        {'id': dato.id, 'value': dato.descripcion}
        for dato in datos
    ]

    array_datos.insert(0, {'id': '', 'value': '---------'})

    query = {'query': array_datos}

    return HttpResponse(json.dumps(query), content_type='application/json')