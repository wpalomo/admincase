# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organigrama', '0001_initial'),
        ('instituciones', '__first__'),
        ('salud', '0001_initial'),
        ('personas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionFormal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('fecha_desde', models.DateField(null=True, blank=True)),
                ('fecha_hasta', models.DateField(null=True, blank=True)),
                ('cargo', models.ForeignKey(null=True, blank=True, to='organigrama.Cargo')),
                ('departamento', models.ForeignKey(null=True, blank=True, to='organigrama.Departamento')),
                ('destino', models.ForeignKey(null=True, blank=True, to='instituciones.Institucion')),
                ('direccion', models.ForeignKey(null=True, blank=True, to='organigrama.Direccion')),
                ('division', models.ForeignKey(null=True, blank=True, to='organigrama.Division')),
            ],
            options={
                'verbose_name_plural': 'Asignaciones Formales de Empleados',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('cuil', models.CharField(max_length=15, null=True, blank=True)),
                ('cuit', models.CharField(max_length=15, null=True, blank=True)),
                ('fecha_ingreso', models.DateField(null=True, blank=True)),
                ('fecha_egreso', models.DateField(null=True, blank=True)),
                ('persona', models.OneToOneField(to='personas.Persona')),
            ],
            options={
                'verbose_name_plural': 'Empleados',
                'ordering': ['persona__apellido'],
            },
        ),
        migrations.CreateModel(
            name='EmpleadoEspecialidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('empleado', models.ForeignKey(to='empleados.Empleado')),
                ('especialidad', models.ForeignKey(to='salud.Especialidad')),
            ],
            options={
                'verbose_name_plural': 'Empleado-Especialidad',
            },
        ),
        migrations.CreateModel(
            name='SituacionLaboral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('descripcion', models.CharField(max_length=70, unique=True)),
                ('abreviatura', models.CharField(max_length=5, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Situacion del Empleado',
            },
        ),
        migrations.AddField(
            model_name='empleado',
            name='situacion_laboral',
            field=models.ForeignKey(null=True, blank=True, to='empleados.SituacionLaboral'),
        ),
        migrations.AddField(
            model_name='asignacionformal',
            name='empleado',
            field=models.ForeignKey(null=True, blank=True, to='empleados.Empleado'),
        ),
        migrations.AddField(
            model_name='asignacionformal',
            name='seccion',
            field=models.ForeignKey(null=True, blank=True, to='organigrama.Seccion'),
        ),
        migrations.AddField(
            model_name='asignacionformal',
            name='servicio',
            field=models.ForeignKey(null=True, blank=True, to='organigrama.Servicio'),
        ),
    ]
