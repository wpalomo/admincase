# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instituciones', '0001_initial'),
        ('organigrama', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='institucion',
            field=models.ForeignKey(blank=True, to='instituciones.Institucion', null=True),
        ),
        migrations.AddField(
            model_name='direccion',
            name='institucion',
            field=models.ForeignKey(blank=True, to='instituciones.Institucion', null=True),
        ),
    ]
