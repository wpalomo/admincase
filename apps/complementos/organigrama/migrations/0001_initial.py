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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50)),
                ('imagen', models.ImageField(blank=True, upload_to=apps.complementos.organigrama.models._generar_ruta_imagen, null=True)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Entidades',
            },
        ),
        migrations.CreateModel(
            name='Profesion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=70)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Profesiones',
            },
        ),
    ]
