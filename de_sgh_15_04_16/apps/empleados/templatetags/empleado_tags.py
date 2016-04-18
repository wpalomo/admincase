from datetime import datetime
from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.filter
def get_estado_asignacion(asigancionformal):
    fecha = datetime.now()
    # hoy = fecha.strftime('%d/%m/%Y')

    if asigancionformal.fecha_hasta >= fecha.date():
        return 'ACTIVO'
    else:
        return 'INACTIVO'