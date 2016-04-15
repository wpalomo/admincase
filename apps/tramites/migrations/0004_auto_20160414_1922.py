# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tramites', '0003_auto_20160414_1919'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requisitorequerido',
            options={'verbose_name_plural': 'Requisitos del Tramite'},
        ),
        migrations.RemoveField(
            model_name='requisito',
            name='tipo_tramite',
        ),
    ]
