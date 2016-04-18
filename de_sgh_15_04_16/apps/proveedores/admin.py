# -*- encoding: utf-8 -*-
from django.contrib import admin
from apps.proveedores.models import Proveedor


class ProveedorAdmin(admin.ModelAdmin):

    list_display = ['id', 'razon_social', 'exclusivo_administracion']
    ordering = ['razon_social']


admin.site.register(Proveedor, ProveedorAdmin)