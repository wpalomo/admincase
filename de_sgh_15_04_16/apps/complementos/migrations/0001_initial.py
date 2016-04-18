# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('descripcion', models.CharField(unique=True, max_length=5)),
            ],
            options={
                'verbose_name_plural': 'Categorias',
                'ordering': ['descripcion'],
            },
        ),
        migrations.CreateModel(
            name='SituacionLaboral',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('descripcion', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'verbose_name': 'Situacion Laboral',
                'verbose_name_plural': 'Situaciones Laborales',
            },
        ),
        migrations.CreateModel(
            name='TipoIVA',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('descripcion', models.CharField(unique=True, max_length=25)),
            ],
            options={
                'verbose_name': 'Tipo de IVA',
                'verbose_name_plural': 'Tipos de IVA',
            },
        ),
    ]
