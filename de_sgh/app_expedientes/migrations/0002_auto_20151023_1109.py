# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expedientes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expedientelicitacion',
            old_name='numero_licitacion',
            new_name='anio',
        ),
        migrations.AddField(
            model_name='expedientelicitacion',
            name='numero',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
