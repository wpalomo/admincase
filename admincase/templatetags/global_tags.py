from django import template
from datetime import date, datetime, timedelta
from apps.contactos.models import Contacto
from apps.tramites.models import RequisitoTramite

register = template.Library()


@register.filter()
def set_color_estado(fecha_turno):
    fecha = datetime.now()
    dif = (fecha_turno - fecha.date()).days
    # print(dif)
    if 0 <= int(dif) <= 4:  # ROJO
        return 'red'

    if 4 < int(dif) <= 10:  # AMARILLO
        return '#FFA500'

    if 10 < int(dif) <= 20:  # VERDE
        return 'green'


@register.filter()
def get_danger(fecha_turno):
    fecha = datetime.now()
    dif = (fecha_turno - fecha.date()).days

    if int(dif) == 0:
        return ' -- HOY!'
    return ''


@register.filter()
def get_contactos(cliente, tipo):
    contactos = Contacto.objects.filter(persona__id=cliente.persona.id)
    lista = ''
    for contacto in contactos.filter(tipo_contacto__valor=tipo):
        lista += str(contacto.descripcion) + ' - '

    return lista[:-2]


@register.filter()
def get_estado_requisitos(tramite):

    estado_requisitos = RequisitoTramite.objects.filter(tramite__id=tramite.id)

    for requisito in estado_requisitos:
        if not requisito.presentado:
            return 'Incompleto'
    return 'Completo'