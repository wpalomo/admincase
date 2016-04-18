from django.contrib import admin

from .models import Institucion


class InstitucionAdmin(admin.ModelAdmin):

        list_display = ['nombre']

admin.site.register(Institucion, InstitucionAdmin)