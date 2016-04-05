# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import apps.personas.models


class Migration(migrations.Migration):

    dependencies = [
        ('organigrama', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persona', '0001_initial'),
        ('salud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('foto', models.ImageField(upload_to=apps.personas.models._generar_ruta_imagen, blank=True, null=True)),
                ('apellido', models.CharField(max_length=30, blank=True, null=True)),
                ('nombre', models.CharField(max_length=30, blank=True, null=True)),
                ('numero_documento', models.CharField(max_length=20, blank=True, null=True)),
                ('fecha_nacimiento', models.DateField(default='01/01/1900')),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('estado_civil', models.ForeignKey(null=True, blank=True, to='persona.EstadoCivil')),
                ('nivel_educacion', models.ForeignKey(null=True, blank=True, to='persona.NivelEducacion')),
                ('obra_social', models.ForeignKey(null=True, blank=True, to='salud.ObraSocial')),
                ('profesion', models.ForeignKey(null=True, blank=True, to='organigrama.Profesion')),
                ('sexo', models.ForeignKey(null=True, blank=True, to='persona.Sexo')),
                ('tipo_documento', models.ForeignKey(to='persona.TipoDocumento', default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('persona', models.OneToOneField(to='personas.Persona')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
