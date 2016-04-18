# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0001_initial'),
        ('persona', '0001_initial'),
        ('personas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Familiar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('vive', models.BooleanField(default=True)),
                ('motivo_fallecimiento', models.TextField(blank=True, null=True, max_length=600)),
                ('otra_ayuda_economica', models.CharField(blank=True, null=True, max_length=60)),
                ('economicamente_activo', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Familiar',
                'verbose_name_plural': 'Familiares',
            },
        ),
        migrations.CreateModel(
            name='FamiliarPaciente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('responsable', models.BooleanField(default=False)),
                ('convive_misma_vivienda', models.BooleanField(default=False)),
                ('observacion', models.TextField(blank=True, null=True, max_length=600)),
                ('familiar', models.ForeignKey(to='familiares.Familiar')),
                ('paciente', models.ForeignKey(to='pacientes.Paciente')),
                ('parentesco', models.ForeignKey(to='persona.Parentesco')),
            ],
            options={
                'verbose_name': 'Familiar y paciente',
                'verbose_name_plural': 'Familiares y pacientes',
            },
        ),
        migrations.CreateModel(
            name='Ocupacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('descripcion', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name': 'Ocupación',
                'verbose_name_plural': 'Ocupaciones',
            },
        ),
        migrations.CreateModel(
            name='SituacionLaboral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('descripcion', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name': 'Situación laboral',
                'verbose_name_plural': 'Situaciones laborales',
            },
        ),
        migrations.CreateModel(
            name='TipoRelacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('descripcion', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name': 'Tipo de relación',
                'verbose_name_plural': 'Tipos de relaciones',
            },
        ),
        migrations.AddField(
            model_name='familiarpaciente',
            name='tipo_relacion',
            field=models.ForeignKey(blank=True, to='familiares.TipoRelacion', null=True),
        ),
        migrations.AddField(
            model_name='familiar',
            name='ocupacion',
            field=models.ForeignKey(blank=True, to='familiares.Ocupacion', null=True),
        ),
        migrations.AddField(
            model_name='familiar',
            name='persona',
            field=models.OneToOneField(to='personas.Persona'),
        ),
        migrations.AddField(
            model_name='familiar',
            name='situacion_laboral',
            field=models.ForeignKey(blank=True, to='familiares.SituacionLaboral', null=True),
        ),
    ]
