# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tramites', '0004_auto_20160414_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequisitoTipoTramite',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('requisito', models.ForeignKey(blank=True, to='tramites.Requisito')),
                ('tipo_tramite', models.ForeignKey(blank=True, to='tramites.TipoTramite')),
            ],
            options={
                'verbose_name_plural': 'Requisitos del Tipo de Tramite',
            },
        ),
        migrations.CreateModel(
            name='RequisitoTramite',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('presentado', models.BooleanField(default=False)),
                ('requisito', models.ForeignKey(blank=True, to='tramites.Requisito')),
                ('tramite', models.ForeignKey(blank=True, to='tramites.Tramite')),
            ],
            options={
                'verbose_name_plural': 'Requisitos Requeridos del Tramite',
            },
        ),
        migrations.RemoveField(
            model_name='requisitorequerido',
            name='requisito',
        ),
        migrations.RemoveField(
            model_name='requisitorequerido',
            name='tramite',
        ),
        migrations.DeleteModel(
            name='RequisitoRequerido',
        ),
    ]
