# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('organigrama', '0001_initial'),
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requisito',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('descripcion', models.CharField(null=True, blank=True, max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Requisitos',
            },
        ),
        migrations.CreateModel(
            name='RequisitoRequerido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('presentado', models.BooleanField(default=False)),
                ('requisito', models.ForeignKey(blank=True, to='tramites.Requisito')),
            ],
            options={
                'verbose_name_plural': 'Requisitos Requeridos del Tramite',
            },
        ),
        migrations.CreateModel(
            name='TipoTramite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('descripcion', models.CharField(max_length=50)),
                ('entidad', models.ForeignKey(null=True, to='organigrama.Entidad', blank=True)),
                ('requisitos', models.ManyToManyField(blank=True, to='tramites.Requisito')),
            ],
            options={
                'verbose_name_plural': 'Tipos de Tramite',
            },
        ),
        migrations.CreateModel(
            name='Tramite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('fecha_alta', models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)),
                ('fecha_turno', models.DateField(null=True, blank=True)),
                ('fecha_alarma', models.DateField(null=True, blank=True)),
                ('fecha_fin', models.DateField(null=True, blank=True)),
                ('estado', models.BooleanField(default=False)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('cliente', models.ForeignKey(null=True, to='clientes.Cliente', blank=True)),
                ('tipo', models.ForeignKey(null=True, to='tramites.TipoTramite', blank=True)),
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
