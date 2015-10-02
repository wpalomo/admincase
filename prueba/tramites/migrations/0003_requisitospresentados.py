# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tramites', '0002_tramite'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequisitosPresentados',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('estado', models.BooleanField(default=False)),
                ('requisito', models.ForeignKey(to='tramites.Requisito', null=True, blank=True)),
                ('tramite', models.ForeignKey(to='tramites.TipoTramite', null=True, blank=True)),
            ],
        ),
    ]
