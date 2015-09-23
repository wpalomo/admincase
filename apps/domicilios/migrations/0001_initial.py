# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locacion', '__first__'),
        ('personas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domicilio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=200, null=True, blank=True)),
                ('barrio', models.ForeignKey(blank=True, to='locacion.Barrio', null=True)),
                ('persona', models.ForeignKey(to='personas.Persona')),
            ],
            options={
                'verbose_name_plural': 'Domicilios de las Personas',
            },
        ),
        migrations.CreateModel(
            name='TipoDomicilio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Domicilios',
            },
        ),
        migrations.AddField(
            model_name='domicilio',
            name='tipo',
            field=models.ForeignKey(to='domicilios.TipoDomicilio'),
        ),
    ]
