# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('cuil', models.CharField(blank=True, null=True, max_length=15)),
                ('fecha_alta_sistema', models.DateTimeField(auto_now_add=True)),
                ('persona', models.OneToOneField(blank=True, to='personas.Persona')),
            ],
            options={
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='SituacionLaboral',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('descripcion', models.CharField(max_length=70, unique=True)),
                ('abreviatura', models.CharField(blank=True, null=True, max_length=5)),
            ],
            options={
                'verbose_name_plural': 'Situacion Laboral',
            },
        ),
        migrations.AddField(
            model_name='cliente',
            name='situacion_laboral',
            field=models.ForeignKey(blank=True, to='clientes.SituacionLaboral', null=True),
        ),
    ]
