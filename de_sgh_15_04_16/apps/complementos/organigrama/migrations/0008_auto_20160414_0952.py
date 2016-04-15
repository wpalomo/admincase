# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organigrama', '0007_auto_20160414_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seccion',
            name='division',
        ),
        migrations.AddField(
            model_name='seccion',
            name='servicio',
            field=models.ForeignKey(blank=True, to='organigrama.Servicio', null=True),
        ),
    ]
