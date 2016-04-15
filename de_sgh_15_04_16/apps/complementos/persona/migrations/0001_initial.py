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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('descripcion', models.CharField(unique=True, max_length=70)),
                ('abreviatura', models.CharField(null=True, max_length=3, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Estados Civiles',
            },
        ),
        migrations.CreateModel(
            name='Etnia',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('descripcion', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Etnias',
            },
        ),
        migrations.CreateModel(
            name='NivelEducacion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('descripcion', models.CharField(unique=True, max_length=70)),
                ('abreviatura', models.CharField(null=True, max_length=3, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Nivel  de Educacion',
            },
        ),
        migrations.CreateModel(
            name='Parentesco',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nombre', models.CharField(unique=True, max_length=40)),
                ('abreviatura', models.CharField(null=True, max_length=3, blank=True)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Parentesco',
            },
        ),
        migrations.CreateModel(
            name='Sexo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('descripcion', models.CharField(unique=True, max_length=50)),
                ('abreviatura', models.CharField(null=True, max_length=1, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Sexo',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('descripcion', models.CharField(unique=True, max_length=70)),
                ('abreviatura', models.CharField(null=True, max_length=5, blank=True)),
                ('longitud', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Tipos de Documentos',
            },
        ),
    ]
