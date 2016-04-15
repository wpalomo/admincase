# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fichassociales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichasocial',
            name='cantidad_ambiente',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='cantidad_cama',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='cantidad_dormitorio',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
