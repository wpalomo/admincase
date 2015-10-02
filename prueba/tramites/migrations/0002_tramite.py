# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tramites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tramite',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('tipo_tramite', models.ForeignKey(to='tramites.TipoTramite', blank=True, null=True)),
            ],
        ),
    ]
