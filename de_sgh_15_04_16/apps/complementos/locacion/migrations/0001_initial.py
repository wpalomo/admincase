# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True, blank=True)),
                ('descripcion', models.CharField(max_length=500, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Barrios',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True, blank=True)),
                ('departamento', models.ForeignKey(to='locacion.Departamento', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Localidades',
            },
        ),
        migrations.CreateModel(
            name='LugarNacimiento',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Paises',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True, blank=True)),
                ('pais', models.ForeignKey(to='locacion.Pais')),
            ],
            options={
                'verbose_name_plural': 'Provincias',
            },
        ),
        migrations.AddField(
            model_name='departamento',
            name='provincia',
            field=models.ForeignKey(to='locacion.Provincia'),
        ),
        migrations.AddField(
            model_name='barrio',
            name='localidad',
            field=models.ForeignKey(to='locacion.Localidad', null=True, blank=True),
        ),
    ]
