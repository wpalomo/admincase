# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instituciones', '0001_initial'),
        ('organigrama', '0005_auto_20160413_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=30)),
                ('institucion', models.ForeignKey(to='instituciones.Institucion', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Cargos de la Institucion',
            },
        ),
    ]
