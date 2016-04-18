# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Especialidades',
            },
        ),
        migrations.CreateModel(
            name='GrupoSanguineo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('descripcion', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Grupo Sanguineo',
            },
        ),
        migrations.CreateModel(
            name='Practica',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('especialidad', models.ForeignKey(to='salud.Especialidad')),
            ],
            options={
                'verbose_name_plural': 'Practicas',
            },
        ),
        migrations.CreateModel(
            name='UnidadMedida',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('descripcion', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Unidades de Medidas',
                'ordering': ['descripcion'],
            },
        ),
    ]
