# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asignacionformal',
            options={'ordering': ['-fecha_hasta'], 'verbose_name_plural': 'Asignaciones Formales de Empleados'},
        ),
    ]
