# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from .models import (Composicion, MedicamentoLineaTerapeutica,
                     AdministracionForma, NumeroAutoincremental)


def get_numero_autoincremental(tipo):
    numero_autoincremental = NumeroAutoincremental.objects.get(
        tipo__descripcion=tipo)
    numero = int(numero_autoincremental.numero) + 1

    return numero


def guardar_numero_autoincremental(tipo, numero):
    numero_autoincremental = \
        NumeroAutoincremental.objects.get(tipo__descripcion=tipo)

    if int(numero) > numero_autoincremental.numero:
        numero_autoincremental.numero = numero
        numero_autoincremental.save()


def registrar_numeros_autoincrementales(listado):
    for (tipo, numero) in list(listado.items()):
        guardar_numero_autoincremental(tipo, numero)


def get_eliminar_item(request):
    tipo = request.GET.get('tipo')
    id_item = request.GET.get('id')

    try:
        if tipo == "COMPOSICION":
            Composicion.objects.get(pk=id_item).delete()
        if tipo == "LINEA_TERAPEUTICA":
            MedicamentoLineaTerapeutica.objects.get(pk=id_item).delete()
        if tipo == "ADMINISTRACION_FORMA":
            AdministracionForma.objects.get(pk=id_item).delete()

        result = {"mensaje": "Se ha eliminado correctamente!"}
    except:
        result = []

    return HttpResponse(json.dumps(result), content_type='application/json')


def set_id_medicamento(request, id_medicamento):
    '''
    :param request: recibe el request completo
    :param id_medicamento: recibe el id de medicamento
    :return: devuelve un request con el id de medicamento
    '''
    request.POST._mutable = True
    request.POST['medicamento'] = id_medicamento
    request.POST._mutable = False
    return request.POST
