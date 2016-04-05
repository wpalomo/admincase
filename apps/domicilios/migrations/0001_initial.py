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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(blank=True, null=True, max_length=200)),
                ('barrio', models.ForeignKey(to='locacion.Barrio', blank=True, null=True)),
                ('departamento', models.ForeignKey(to='locacion.Departamento', blank=True, null=True)),
                ('localidad', models.ForeignKey(to='locacion.Localidad', blank=True, null=True)),
                ('pais', models.ForeignKey(to='locacion.Pais', blank=True, null=True)),
                ('persona', models.ForeignKey(to='personas.Persona')),
                ('provincia', models.ForeignKey(to='locacion.Provincia', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Domicilios de las Personas',
            },
        ),
        migrations.CreateModel(
            name='TipoDomicilio',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Domicilios',
            },
        ),
        migrations.AddField(
            model_name='domicilio',
            name='tipo',
            field=models.ForeignKey(to='domicilios.TipoDomicilio', blank=True, null=True),
        ),
    ]
