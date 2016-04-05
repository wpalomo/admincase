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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre', models.CharField(blank=True, null=True, max_length=50)),
                ('descripcion', models.CharField(blank=True, null=True, max_length=500)),
            ],
            options={
                'verbose_name_plural': 'Barrios',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre', models.CharField(blank=True, null=True, max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre', models.CharField(blank=True, null=True, max_length=50)),
                ('departamentos', models.ForeignKey(blank=True, null=True, to='locacion.Departamento')),
            ],
            options={
                'verbose_name_plural': 'Localidades',
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre', models.CharField(blank=True, null=True, max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Paises',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('nombre', models.CharField(blank=True, null=True, max_length=50)),
                ('pais', models.ForeignKey(to='locacion.Pais')),
            ],
            options={
                'verbose_name_plural': 'Provincias',
            },
        ),
        migrations.AddField(
            model_name='departamento',
            name='provincias',
            field=models.ForeignKey(to='locacion.Provincia'),
        ),
        migrations.AddField(
            model_name='barrio',
            name='localidades',
            field=models.ForeignKey(blank=True, null=True, to='locacion.Localidad'),
        ),
    ]
