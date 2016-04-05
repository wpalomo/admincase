# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse, JsonResponse

from .models import TipoTramite


def get_requisitos_tipo_tramite(request):
    tipo = request.GET.get('id_tipo')

    requisitos_del_tramite = TipoTramite.objects.get(pk=int(tipo))

    result = {}

    for check in requisitos_del_tramite.requisitos.all():

        result[check.id] = check.descripcion

    # return JsonResponse(result)
    return HttpResponse(json.dumps(result), content_type='application/json')

# def get_numero_autoincremental(tipo):
#     numero_autoincremental = NumeroAutoincremental.objects.get(tipo=tipo)
#     numero = int(numero_autoincremental.numero) + 1
#
#     return numero
#
#
# def guardar_numero_autoincremental(tipo, numero):
#     numero_autoincremental = NumeroAutoincremental.objects.get(tipo=tipo)
#
#     if int(numero) > numero_autoincremental.numero:
#         numero_autoincremental.numero = numero
#         numero_autoincremental.save()
#
#
# def numero_es_valido(tipo, numero):
#     numero_autoincremental = NumeroAutoincremental.objects.get(tipo=tipo)
#     return int(numero) <= numero_autoincremental.numero
#
#
# def get_numero_ingreso_manual_es_valido(request):
#     tipo = request.GET.get('tipo')
#     numero = int(request.GET.get('numero'))
#
#     result = numero_es_valido(tipo, numero)
#
#     return HttpResponse(json.dumps(result), content_type='application/json')
#
#
# def registrar_numeros_autoincrementales(listado):
#     for (tipo, numero) in list(listado.items()):
#         guardar_numero_autoincremental(tipo, numero)
#
#
# def get_tipo_transaccion(request):
#
#     importe = float(request.GET.get('importe'))
#
#     if importe < IMPORTE_MINIMO_TRANSACCION_RESOLUCION:
#         result = {'result': 'error', 'msg': 'Verifique el importe ingresado'}
#
#     elif importe >= IMPORTE_MINIMO_TRANSACCION_RESOLUCION \
#                 and importe <= IMPORTE_MEDIO_TRANSACCION_RESOLUCION:
#         result = get_valores_compra_directa()
#
#     elif importe > IMPORTE_MEDIO_TRANSACCION_RESOLUCION:
#         result = get_valores_contratacion_directa()
#
#     return HttpResponse(json.dumps(result), content_type='application/json')
#
#
# def get_valores_compra_directa():
#     numero = get_numero_autoincremental('COMPRA_DIRECTA')
#
#     result = {
#         'result': 'ok',
#         'tipo_transaccion': 'COMPRA DIRECTA',
#         'numero_identificacion_transaccion': numero
#         }
#
#     return result
#
#
# def get_valores_contratacion_directa():
#     numero = get_numero_autoincremental('CONTRATACION_DIRECTA')
#
#     result = {
#         'result': 'ok',
#         'tipo_transaccion': 'CONTRATACION DIRECTA',
#         'numero_identificacion_transaccion': numero
#         }
#
#     return result
#
#
# def get_tipo_transaccion_disposicion(request):
#
#     importe = request.POST.get('importe', '0')
#     result = {'msg': ''}
#
#     if float(importe) >= float(IMPORTE_MAXIMO_TRANSACCION_DISPOSICION):
#         result = {
#             'msg': 'Verifique el importe ingresado, debe ser menor a $1200'}
#
#     return HttpResponse(json.dumps(result), content_type='application/json')
#
#
# def get_etapa(request):
#
#     etapa_id = request.GET.get('etapa_id')
#
#     try:
#         etapa = Etapa.objects.get(pk=etapa_id)
#         result = {"etapa_id": etapa.id, "valor": etapa.valor}
#     except:
#         result = []
#
#     return HttpResponse(json.dumps(result), content_type='application/json')
#
#
# def get_estado_valor(request):
#
#     estado_id = request.GET.get('estado_id')
#
#     try:
#         estado = Estado.objects.get(pk=estado_id)
#         result = estado.valor
#     except:
#         result = []
#
#     return HttpResponse(json.dumps(result), content_type='application/json')
#
#
# #VERIFICAR
# def get_fecha_resolucion_pago_es_valido(request):
#
#     fecha = request.GET.get('fecha')
#
#     try:
#         datetime.datetime.strptime(fecha, "%d/%m/%Y").date()
#         result = True
#     except:
#         result = False
#
#     return HttpResponse(json.dumps(result), content_type='application/json')
#
#
# def get_clase_valor(request):
#
#     clase_id = request.GET.get('clase_id')
#
#     try:
#         clase = Clase.objects.get(pk=clase_id)
#         result = {"valor": clase.valor}
#     except:
#         result = []
#
#     return HttpResponse(json.dumps(result), content_type='application/json')
#
#
# def get_numero_autoincremental_ajax(request):
#
#     tipo = request.GET.get('tipo')
#     numero = get_numero_autoincremental(tipo)
#     numero = str(numero).zfill(4)  # formato 0000
#
#     result = {'numero': numero}
#
#     return HttpResponse(json.dumps(result), content_type='application/json')
#
#
# def get_expedientes_con_reserva_mayor_15_dias(request):
#     """
#     Devuelve 1 si hay expedientes con ESTADO: RESERVADO con fechas de reservas
#     mayores a 15 dias
#     Si no, devuelve 0
#     """
#
#     fecha_actual = datetime.now()
#     dias = timedelta(days=15)
#     hoy_menos_15_dias = fecha_actual - dias
#
#     try:
#         expedientes = Expediente.objects.filter(
#             fecha__lte=hoy_menos_15_dias.date(), estado__valor="RESERVADO")
#
#         if len(expedientes) > 0:
#             result = 1
#         else:
#             result = 0
#
#     except:
#         result = 0
#
#     return HttpResponse(json.dumps(result), content_type='application/json')
#

# def get_numero_expediente(request):
#
#     try:
#         anio_actual = time.strftime("%y")
#         expediente = Expediente.objects.filter(anio=anio_actual).exclude(
#             numero__isnull=True).exclude(numero='').latest('id')
#         numero = int(expediente.numero) + 1
#     except:
#         numero = 1
#
#     # para que me genere con formato 0000
#     numero = str(numero).zfill(4)
#     result = {'numero': numero}
#
#     return HttpResponse(json.dumps(result), content_type='application/json')