# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complementos', '0001_initial'),
        ('fichassociales', '0002_auto_20160402_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichasocial',
            name='situacion_laboral',
            field=models.ForeignKey(null=True, blank=True, to='complementos.SituacionLaboral'),
        ),
    ]
