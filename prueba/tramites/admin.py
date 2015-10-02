from django.contrib import admin
from .models import TipoTramite, Requisito, Entidad, Tramite, RequisitosPresentados

class TipoTramiteAdmin(admin.ModelAdmin):
    ordering=['id']


class RequisitoAdmin(admin.ModelAdmin):
    ordering=['id']

class EntidadAdmin(admin.ModelAdmin):
    ordering=['id']

class TramiteAdmin(admin.ModelAdmin):
    ordering=['id']

class RequisitosPresentadosAdmin(admin.ModelAdmin):
    list_display=['id','tramite', 'requisito', 'estado']

    ordering=['id']


admin.site.register(TipoTramite, TipoTramiteAdmin)
admin.site.register(Entidad, EntidadAdmin)
admin.site.register(Requisito, RequisitoAdmin)
admin.site.register(Tramite, TramiteAdmin)
admin.site.register(RequisitosPresentados, RequisitosPresentadosAdmin)