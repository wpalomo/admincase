# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organigrama', '0006_cargo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicio',
            name='seccion',
        ),
        migrations.AddField(
            model_name='servicio',
            name='division',
            field=models.ForeignKey(to='organigrama.Division', null=True, blank=True),
        ),
    ]
