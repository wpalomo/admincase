from django import template

register = template.Library()


@register.filter()
def agregar_ceros(value, cantidad_ceros):
    return str(value).zfill(cantidad_ceros)