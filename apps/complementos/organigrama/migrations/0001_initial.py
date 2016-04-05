# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.complementos.organigrama.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('valor', models.CharField(max_length=50, unique=True, null=True)),
                ('imagen', models.ImageField(upload_to=apps.complementos.organigrama.models._generar_ruta_imagen, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Entidades',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Profesion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(max_length=70, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Profesiones',
                'ordering': ['nombre'],
            },
        ),
    ]
