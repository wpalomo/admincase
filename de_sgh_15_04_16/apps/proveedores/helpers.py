# -*- encoding: utf-8 -*-

from .models import Proveedor
from django.db.models import Q
from django.http import HttpResponse
import json


def get_proveedor_autocomplete(request):

    data = []

    # PARA QUE BUSQUE POR TEXTO O POR CODIGO
    # proveedores = Proveedor.objects.filter(
    #     Q(pk__icontains=request.GET.get('query')) |
    #     Q(razon_social__startswith=request.GET.get('query')))

    try:  # POR CODIGO
        proveedores = Proveedor.objects.filter(pk=int(request.GET.get('query')))

    except:  # POR TEXTO
        proveedores = Proveedor.objects.filter(
            razon_social__startswith=request.GET.get('query'))

    if len(proveedores) > 0:
        for proveedor in proveedores:
            data.append({"data": str(proveedor.id), "value": str(proveedor)})

        result = '{"query": "Unit","suggestions":'+json.dumps(data)+'}'
    else:
        data.append("No existe resultado")
        result = '{"query": "Unit","suggestions":'+json.dumps(data)+'}'

    return HttpResponse(result)