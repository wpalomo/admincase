# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salud', '__first__'),
        ('instituciones', '__first__'),
        ('empleados', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fecha_desde', models.DateField()),
                ('fecha_hasta', models.DateField()),
                ('especialidad', models.ForeignKey(to='salud.Especialidad')),
                ('institucion', models.ForeignKey(to='instituciones.Institucion')),
                ('profesional', models.ForeignKey(to='empleados.Empleado')),
            ],
            options={
                'verbose_name_plural': 'Agenda',
            },
        ),
        migrations.CreateModel(
            name='AgendaDiaConfiguracion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fecha_desde', models.DateField()),
                ('fecha_hasta', models.DateField()),
                ('hora_desde', models.TimeField()),
                ('hora_hasta', models.TimeField()),
                ('duracion_minutos', models.IntegerField(default=0)),
                ('agenda', models.ForeignKey(to='agendas.Agenda')),
            ],
            options={
                'verbose_name_plural': 'Configuracion Dias de Agenda',
            },
        ),
        migrations.CreateModel(
            name='AgendaDiaConfiguracionBloqueo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fecha_desde', models.DateField()),
                ('fecha_hasta', models.DateField()),
                ('observacion', models.CharField(null=True, max_length=500, blank=True)),
                ('agenda', models.ForeignKey(to='agendas.Agenda')),
                ('dia_configuracion', models.ForeignKey(to='agendas.AgendaDiaConfiguracion')),
            ],
            options={
                'verbose_name_plural': 'Agenda Dia Bloqueos',
            },
        ),
        migrations.CreateModel(
            name='AgendaFechaDetalle',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora_desde', models.TimeField()),
                ('hora_hasta', models.TimeField()),
                ('duracion_minutos', models.IntegerField(default=0)),
                ('agenda', models.ForeignKey(to='agendas.Agenda')),
                ('dia_configuracion', models.ForeignKey(to='agendas.AgendaDiaConfiguracion')),
                ('practica', models.ForeignKey(null=True, blank=True, to='salud.Practica')),
            ],
            options={
                'verbose_name_plural': 'Detalle Agenda por Fecha',
            },
        ),
        migrations.CreateModel(
            name='AgendaFechaDetalleBloqueo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('observacion', models.CharField(null=True, max_length=500, blank=True)),
                ('agenda', models.ForeignKey(null=True, to='agendas.Agenda')),
                ('dia_configuracion', models.ForeignKey(null=True, to='agendas.AgendaDiaConfiguracion')),
                ('fecha_detalle', models.ForeignKey(to='agendas.AgendaFechaDetalle')),
            ],
            options={
                'verbose_name_plural': 'Agenda Fecha Detalle Bloqueos',
            },
        ),
        migrations.CreateModel(
            name='AgendaPeriodoBloqueo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fecha_desde', models.DateField()),
                ('fecha_hasta', models.DateField()),
                ('observacion', models.CharField(null=True, max_length=500, blank=True)),
                ('agenda', models.ForeignKey(to='agendas.Agenda')),
            ],
            options={
                'verbose_name_plural': 'Agenda Bloqueos',
            },
        ),
        migrations.CreateModel(
            name='Dia',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('numero', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Dias de la semana',
            },
        ),
        migrations.CreateModel(
            name='MotivoBloqueo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Motivo de Bloqueo',
            },
        ),
        migrations.CreateModel(
            name='TipoAgenda',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Agenda',
            },
        ),
        migrations.AddField(
            model_name='agendaperiodobloqueo',
            name='motivo_bloqueo',
            field=models.ForeignKey(to='agendas.MotivoBloqueo'),
        ),
        migrations.AddField(
            model_name='agendafechadetallebloqueo',
            name='motivo_bloqueo',
            field=models.ForeignKey(to='agendas.MotivoBloqueo'),
        ),
        migrations.AddField(
            model_name='agendadiaconfiguracionbloqueo',
            name='motivo_bloqueo',
            field=models.ForeignKey(to='agendas.MotivoBloqueo'),
        ),
        migrations.AddField(
            model_name='agendadiaconfiguracion',
            name='dia',
            field=models.ForeignKey(to='agendas.Dia'),
        ),
        migrations.AddField(
            model_name='agendadiaconfiguracion',
            name='practica',
            field=models.ForeignKey(null=True, blank=True, to='salud.Practica'),
        ),
        migrations.AddField(
            model_name='agenda',
            name='tipo_agenda',
            field=models.ForeignKey(to='agendas.TipoAgenda'),
        ),
    ]
