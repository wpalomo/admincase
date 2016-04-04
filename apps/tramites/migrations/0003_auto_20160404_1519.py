# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tramites', '0002_auto_20160404_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tramite',
            name='persona',
            field=models.ForeignKey(to='personas.Persona'),
        ),
    ]
