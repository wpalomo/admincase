# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instituciones', '0001_initial'),
        ('organigrama', '0008_auto_20160414_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='division',
            name='departamento',
        ),
        migrations.RemoveField(
            model_name='seccion',
            name='servicio',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='division',
        ),
        migrations.AddField(
            model_name='division',
            name='institucion',
            field=models.ForeignKey(blank=True, to='instituciones.Institucion', null=True),
        ),
        migrations.AddField(
            model_name='seccion',
            name='institucion',
            field=models.ForeignKey(blank=True, to='instituciones.Institucion', null=True),
        ),
        migrations.AddField(
            model_name='servicio',
            name='institucion',
            field=models.ForeignKey(blank=True, to='instituciones.Institucion', null=True),
        ),
    ]
