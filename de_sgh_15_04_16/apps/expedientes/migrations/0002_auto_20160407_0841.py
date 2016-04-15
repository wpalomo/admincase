# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expedientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expedientelicitacion',
            name='resolucion_adjudicacion',
            field=models.CharField(max_length=4, blank=True, null=True),
        ),
    ]
