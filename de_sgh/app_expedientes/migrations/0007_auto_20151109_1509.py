# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expedientes', '0006_auto_20151109_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expedientecomodato',
            name='resolucion_contratacion',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
