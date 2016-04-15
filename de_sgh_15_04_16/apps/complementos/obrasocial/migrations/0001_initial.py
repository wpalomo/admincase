# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MotivoSuspension',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'ordering': ['descripcion'],
                'verbose_name_plural': 'Motivos de Suspensiones',
            },
        ),
        migrations.CreateModel(
            name='ObraSocial',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('abreviatura', models.CharField(max_length=20, blank=True, null=True)),
                ('codigo_padron', models.IntegerField()),
            ],
            options={
                'ordering': ['nombre'],
                'verbose_name_plural': 'Obras Sociales',
            },
        ),
    ]
