# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse, JsonResponse

from .models import TipoTramite, RequisitoTipoTramite


def get_requisitos_tipo_tramite(request):
    tipo = request.GET.get('id_tipo')

    requisito_tipo_tramite = RequisitoTipoTramite.objects.filter(
        tipo_tramite__id=int(tipo), estado=True)

    requisitos = [
        {
            'id': tipo.requisito.id,
            'descripcion': tipo.requisito.descripcion,
            'valor': tipo.requisito.valor,
        }
        for tipo in requisito_tipo_tramite
    ]

    print(requisitos)

    return HttpResponse(json.dumps(requisitos), content_type='application/json')