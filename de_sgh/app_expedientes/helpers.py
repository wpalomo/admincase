# -*- coding: utf-8 -*-

import datetime
import json

from django.http import HttpResponse

from .models import NumeroAutoincremental, Etapa, Estado

IMPORTE_MINIMO_TRANSACCION_RESOLUCION = 1200
IMPORTE_MEDIO_TRANSACCION_RESOLUCION = 12000
IMPORTE_MAXIMO_TRANSACCION_DISPOSICION = 1200

"""
    REFACTORIZAR FUNCION numero_es_valido

    esta funcion trae el ultimo numero autoincrementado y le suma 1

    Se requiere alctualmente que traiga sólo el ultimo numero creado
    por lo cual se CREA:

    FUNCION numero_ingreso_manual_es_valido

"""

# METODO NUEVO CREADO POR NANDO
# def numero_ingreso_manual_es_valido(tipo, numero):
#     numero_autoincremental = NumeroAutoincremental.objects.get(tipo=tipo)
#     return (numero <= numero_autoincremental.numero)


def get_valores_iniciales_resolucion(etapa):
    result = {}
    if etapa == 'ORDENADO':
        numero = get_numero_autoincremental('RESOLUCION_PAGO')
        fecha = datetime.datetime.now()
        result['numero_resolucion_pago'] = numero
        result['fecha_resolucion_pago'] = fecha.strftime('%d/%m/%Y')

    return result


def get_valores_iniciales_servicios_medicos(etapa):
    result = {}
    if etapa == 'COMPROMISO_ORDENADO':
        orden_provision = get_numero_autoincremental('ORDEN_PROVISION')
        acta_recepcion = get_numero_autoincremental('ACTA_RECEPCION')
        resolucion_pago = get_numero_autoincremental('RESOLUCION_PAGO')
        result['orden_provision'] = orden_provision
        result['acta_recepcion'] = acta_recepcion
        result['resolucion_pago'] = resolucion_pago

    return result


get_valores_iniciales_por_expediente = {
    'RESOLUCION': get_valores_iniciales_resolucion,
    'SERVICIO_MEDICO': get_valores_iniciales_servicios_medicos,
    }


def get_valores_iniciales(request):

    tipo_expediente = request.GET.get('tipo_expediente')
    etapa = request.GET.get('etapa')

    try:
        result = get_valores_iniciales_por_expediente[tipo_expediente](etapa)
    except:
        result = {}

    return HttpResponse(json.dumps(result), content_type='application/json')


def get_numero_autoincremental(tipo):
    numero_autoincremental = NumeroAutoincremental.objects.get(tipo=tipo)
    numero = int(numero_autoincremental.numero) + 1

    return numero


def guardar_numero_autoincremental(tipo, numero):
    numero_autoincremental = NumeroAutoincremental.objects.get(tipo=tipo)

    if numero > numero_autoincremental.numero:
        numero_autoincremental.numero = numero
        numero_autoincremental.save()


def numero_es_valido(tipo, numero):
    numero_por_sistema = get_numero_autoincremental(tipo)
    return (numero <= numero_por_sistema)


# METODO NUEVO CREADO POR NANDO: REQUEST PORQUE VOY A CONSULTAR CON AJAX -- VER
def get_numero_ingreso_manual_es_valido(request):
    tipo = request.GET.get('tipo')
    numero = int(request.GET.get('numero'))

    numero_autoincremental = NumeroAutoincremental.objects.get(tipo=tipo)

    result = numero <= numero_autoincremental.numero

    return HttpResponse(json.dumps(result), content_type='application/json')


def registrar_numeros_autoincrementales(listado):
    for (tipo, numero) in list(listado.items()):
        if numero_es_valido(tipo, numero):
            guardar_numero_autoincremental(tipo, numero)


def get_tipo_transaccion(request):

    importe = float(request.GET.get('importe'))

    if importe < IMPORTE_MINIMO_TRANSACCION_RESOLUCION:

        result = {'result': 'error', 'msg': 'Verifique el importe ingresado'}

    elif importe >= IMPORTE_MINIMO_TRANSACCION_RESOLUCION \
                and importe <= IMPORTE_MEDIO_TRANSACCION_RESOLUCION:

        result = get_valores_compra_directa()

    elif importe > IMPORTE_MEDIO_TRANSACCION_RESOLUCION:

        result = get_valores_contratacion_directa()

    return HttpResponse(json.dumps(result), content_type='application/json')


def get_valores_compra_directa():
    numero = get_numero_autoincremental('COMPRA_DIRECTA')

    result = {
        'result': 'ok',
        'tipo_transaccion': 'COMPRA DIRECTA',
        'numero_identificacion_transaccion': numero
        }

    return result


def get_valores_contratacion_directa():
    numero = get_numero_autoincremental('CONTRATACION_DIRECTA')

    result = {
        'result': 'ok',
        'tipo_transaccion': 'CONTRATACION DIRECTA',
        'numero_identificacion_transaccion': numero
        }

    return result


def get_tipo_transaccion_disposicion(request):

    importe = request.POST.get('importe', '0')

    result = {'msg': ''}

    if float(importe) >= float(IMPORTE_MAXIMO_TRANSACCION_DISPOSICION):
        result = {
            'msg': 'Verifique el importe ingresado, debe ser menor a $1200'}

    return HttpResponse(json.dumps(result), content_type='application/json')


def get_etapa(request):

    etapa_id = request.GET.get('etapa_id')

    try:
        etapa = Etapa.objects.get(pk=etapa_id)
        result = {"etapa_id": etapa.id, "valor": etapa.valor}
    except:
        result = []

    return HttpResponse(json.dumps(result), content_type='application/json')


def get_estado_valor(request):

    estado_id = request.GET.get('estado_id')

    try:
        estado = Estado.objects.get(pk=estado_id)
        result = estado.valor
    except:
        result = []

    return HttpResponse(json.dumps(result), content_type='application/json')