# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '__first__'),
        ('organigrama', '0002_entidad_valor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requisito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(null=True, max_length=50, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Requisitos',
            },
        ),
        migrations.CreateModel(
            name='RequisitoRequerido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('presentado', models.BooleanField(default=False)),
                ('requisito', models.ForeignKey(blank=True, to='tramites.Requisito')),
            ],
            options={
                'verbose_name_plural': 'Requisitos del Tramite',
            },
        ),
        migrations.CreateModel(
            name='TipoTramite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=50)),
                ('entidad', models.ForeignKey(null=True, blank=True, to='organigrama.Entidad')),
                ('requisitos', models.ManyToManyField(to='tramites.Requisito', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Tramite',
            },
        ),
        migrations.CreateModel(
            name='Tramite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha_alta', models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)),
                ('fecha_inicio', models.DateField(null=True, blank=True)),
                ('fecha_alarma', models.DateField(null=True, blank=True)),
                ('fecha_fin', models.DateField(null=True, blank=True)),
                ('estado', models.BooleanField(default=False)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('persona', models.ForeignKey(to='personas.Persona')),
                ('tipo', models.ForeignKey(null=True, blank=True, to='tramites.TipoTramite')),
            ],
            options={
                'verbose_name_plural': 'Tramites',
            },
        ),
        migrations.AddField(
            model_name='requisitorequerido',
            name='tramite',
            field=models.ForeignKey(blank=True, to='tramites.Tramite'),
        ),
    ]
