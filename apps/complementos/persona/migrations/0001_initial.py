# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoCivil',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=70, unique=True)),
                ('abreviatura', models.CharField(null=True, max_length=3, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Estados Civiles',
            },
        ),
        migrations.CreateModel(
            name='NivelEducacion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=70, unique=True)),
                ('abreviatura', models.CharField(null=True, max_length=3, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Nivel  de Educacion',
            },
        ),
        migrations.CreateModel(
            name='Sexo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50, unique=True)),
                ('abreviatura', models.CharField(null=True, max_length=1, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Sexo',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=70, unique=True)),
                ('abreviatura', models.CharField(null=True, max_length=5, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Documentos',
            },
        ),
    ]
