# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoSanguineo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=70, unique=True)),
                ('abreviatura', models.CharField(max_length=5, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Grupos Sanguineos',
            },
        ),
        migrations.CreateModel(
            name='ObraSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('abreviatura', models.CharField(max_length=10, null=True, blank=True)),
                ('codigo_padron', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Obras Sociales',
            },
        ),
    ]
