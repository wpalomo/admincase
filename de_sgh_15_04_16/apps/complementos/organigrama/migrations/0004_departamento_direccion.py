# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organigrama', '0003_remove_departamento_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='departamento',
            name='direccion',
            field=models.ForeignKey(blank=True, null=True, to='organigrama.Direccion'),
        ),
    ]
