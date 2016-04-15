# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArbolItem',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('padre_id', models.IntegerField(default=0)),
                ('visible', models.BooleanField(default=True)),
                ('is_folder', models.BooleanField(default=True)),
                ('modulo', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Modulos ArbolItem',
            },
        ),
    ]
