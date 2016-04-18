# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organigrama', '0004_departamento_direccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargo',
            name='institucion',
        ),
        migrations.DeleteModel(
            name='Cargo',
        ),
    ]
