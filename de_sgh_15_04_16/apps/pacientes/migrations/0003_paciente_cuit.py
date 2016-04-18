# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0002_paciente_cuil'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='cuit',
            field=models.CharField(max_length=80, null=True, blank=True),
        ),
    ]
