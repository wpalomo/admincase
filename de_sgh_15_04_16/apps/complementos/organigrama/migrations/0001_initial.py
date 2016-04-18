# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Cargos de la Institucion',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('descripcion', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Departamentos de la Institucion',
            },
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('descripcion', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Direcciones de la Institucion',
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('descripcion', models.CharField(unique=True, max_length=100)),
                ('departamento', models.ForeignKey(null=True, to='organigrama.Departamento', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Divisiones de la Institucion',
            },
        ),
        migrations.CreateModel(
            name='Profesion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(unique=True, max_length=70)),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Profesiones',
            },
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('descripcion', models.CharField(unique=True, max_length=100)),
                ('division', models.ForeignKey(null=True, to='organigrama.Division', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Secciones de la Institucion',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('descripcion', models.CharField(unique=True, max_length=100)),
                ('seccion', models.ForeignKey(null=True, to='organigrama.Seccion', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Servicios de la Institucion',
            },
        ),

        migrations.AddField(
            model_name='departamento',
            name='direccion',
            field=models.ForeignKey(null=True, to='organigrama.Direccion', blank=True),
        ),
    ]
