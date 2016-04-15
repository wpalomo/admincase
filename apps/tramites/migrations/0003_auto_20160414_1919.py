# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tramites', '0002_requisito_valor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipotramite',
            name='requisitos',
        ),
        migrations.AddField(
            model_name='requisito',
            name='tipo_tramite',
            field=models.ForeignKey(null=True, to='tramites.TipoTramite', blank=True),
        ),
    ]
