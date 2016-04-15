# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '__first__'),
        ('salud', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=70, unique=True)),
                ('abreviatura', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'verbose_name_plural': 'Clases de Pacientes',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_alta_sistema', models.DateTimeField(auto_now_add=True)),
                ('clase', models.ForeignKey(blank=True, to='pacientes.Clase', null=True)),
                ('grupo_sanguineo', models.ForeignKey(blank=True, to='salud.GrupoSanguineo', null=True)),
                ('persona', models.OneToOneField(to='personas.Persona')),
            ],
            options={
                'verbose_name_plural': 'Pacientes',
            },
        ),
        migrations.CreateModel(
            name='TipoPaciente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=70, unique=True)),
                ('abreviatura', models.CharField(blank=True, max_length=5, null=True)),
                ('valor', models.CharField(null=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Pacientes',
            },
        ),
        migrations.AddField(
            model_name='paciente',
            name='tipo',
            field=models.ForeignKey(to='pacientes.TipoPaciente'),
        ),
    ]
