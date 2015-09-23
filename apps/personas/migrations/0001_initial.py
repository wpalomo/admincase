# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import apps.personas.models


class Migration(migrations.Migration):

    dependencies = [
        ('salud', '__first__'),
        ('persona', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organigrama', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foto', models.ImageField(null=True, upload_to=apps.personas.models._generar_ruta_imagen, blank=True)),
                ('apellido', models.CharField(max_length=30, null=True, blank=True)),
                ('nombre', models.CharField(max_length=30, null=True, blank=True)),
                ('numero_documento', models.CharField(max_length=20, null=True, blank=True)),
                ('fecha_nacimiento', models.DateField(default='01/01/1900')),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('estado_civil', models.ForeignKey(blank=True, to='persona.EstadoCivil', null=True)),
                ('nivel_educacion', models.ForeignKey(blank=True, to='persona.NivelEducacion', null=True)),
                ('obra_social', models.ForeignKey(blank=True, to='salud.ObraSocial', null=True)),
                ('profesion', models.ForeignKey(blank=True, to='organigrama.Profesion', null=True)),
                ('sexo', models.ForeignKey(blank=True, to='persona.Sexo', null=True)),
                ('tipo_documento', models.ForeignKey(default=1, to='persona.TipoDocumento')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('persona', models.OneToOneField(to='personas.Persona')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
