# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tramites', '0005_auto_20160414_1927'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipotramite',
            options={'verbose_name_plural': 'Tipos de Tramite', 'ordering': ['entidad']},
        ),
        migrations.AlterModelOptions(
            name='tramite',
            options={'verbose_name_plural': 'Tramites', 'ordering': ['-fecha_alta']},
        ),
        migrations.AddField(
            model_name='requisitotipotramite',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]
