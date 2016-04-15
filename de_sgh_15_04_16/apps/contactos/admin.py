from django.contrib import admin

from .models import Contacto, TipoContacto

from .forms import ContactoForm


class TipoContactoAdmin(admin.ModelAdmin):

    list_display = [
        'descripcion'
    ]

    search_fields = [
        'descripcion'
    ]

    list_filter = [
        'descripcion'
    ]


# class Meta:
#         form = TipoContactoForm


class ContactoAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'descripcion',
        'proveedor',
        'observacion'
    ]

    search_fields = [
        'descripcion',
        'proveedor',
        'observacion'
    ]

    list_filter = [
        'descripcion',
        'proveedor',
        'observacion'
    ]

    class Meta:
        form = ContactoForm

admin.site.register(TipoContacto, TipoContactoAdmin)
admin.site.register(Contacto, ContactoAdmin)