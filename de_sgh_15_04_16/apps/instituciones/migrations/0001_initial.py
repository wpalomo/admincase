# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('cuit', models.CharField(max_length=50, unique=True)),
                ('telefono', models.CharField(null=True, max_length=100, blank=True)),
                ('domicilio', models.CharField(null=True, max_length=1000, blank=True)),
                ('departamento', models.ForeignKey(to='locacion.Departamento')),
                ('pais', models.ForeignKey(to='locacion.Pais')),
                ('provincia', models.ForeignKey(to='locacion.Provincia')),
            ],
            options={
                'verbose_name_plural': 'Instituciones',
            },
        ),
    ]
