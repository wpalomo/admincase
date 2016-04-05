# -*- encoding: utf-8 -*-
from PIL import Image
from datetime import datetime
from .models import Cliente
from django.db.models import Q
from django.http import HttpResponse
from django.core import serializers
import json


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


# def get_empleado_autocomplete(request):
#     data = []
#     # empleados = Empleado.objects.filter(
#     #     persona__apellido__startswith=request.GET.get('query'))
#     # PARA QUE TRAIGA SOLO LOS EMPLEADOS SIN FECHA DE EGRESO
#     # empleados = Empleado.objects.filter(
#     #     persona__apellido__startswith=request.GET.get('query')).exclude(
#     #     fecha_egreso__isnull=False)
#
#     # PARA QUE BUSQUE POR TEXTO O POR CODIGO
#
#     try:  # POR CODIGO
#         empleados = Empleado.objects.filter(pk=int(request.GET.get('query'))).exclude(
#             fecha_egreso__isnull=False)
#
#     except:  # POR TEXTO
#         empleados = Empleado.objects.filter(
#             persona__apellido__icontains=request.GET.get('query')).exclude(
#             fecha_egreso__isnull=False)
#
#     if len(empleados) > 0:
#         for empleado in empleados:
#             data.append({"data": str(empleado.id), "value": str(empleado)})
#
#         result = '{"query": "Unit","suggestions":'+json.dumps(data)+'}'
#     else:
#         data.append("No existe resultado")
#         result = '{"query": "Unit","suggestions":'+json.dumps(data)+'}'
#
#     return HttpResponse(result)