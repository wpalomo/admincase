# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '__first__'),
        ('locacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domicilio',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('descripcion', models.CharField(blank=True, null=True, max_length=200)),
                ('barrio', models.ForeignKey(null=True, blank=True, to='locacion.Barrio')),
                ('departamento', models.ForeignKey(null=True, blank=True, to='locacion.Departamento')),
                ('localidad', models.ForeignKey(null=True, blank=True, to='locacion.Localidad')),
                ('pais', models.ForeignKey(null=True, blank=True, to='locacion.Pais')),
                ('persona', models.ForeignKey(to='personas.Persona')),
                ('provincia', models.ForeignKey(null=True, blank=True, to='locacion.Provincia')),
            ],
            options={
                'verbose_name_plural': 'Domicilios de las Personas',
            },
        ),
        migrations.CreateModel(
            name='TipoDomicilio',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Domicilios',
            },
        ),
        migrations.AddField(
            model_name='domicilio',
            name='tipo',
            field=models.ForeignKey(null=True, blank=True, to='domicilios.TipoDomicilio'),
        ),
    ]
