# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0001_initial'),
        ('organigrama', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoTramite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
                ('estado', models.BooleanField(default=False)),
                ('observaciones', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Tramite',
            },
        ),
        migrations.CreateModel(
            name='Tramite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entidad', models.ForeignKey(to='organigrama.Entidad')),
                ('persona', models.ForeignKey(to='personas.Persona')),
                ('tipo', models.ForeignKey(blank=True, to='tramites.TipoTramite', null=True)),
            ],
        ),
    ]
