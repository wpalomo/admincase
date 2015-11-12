# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '__first__'),
        ('proveedores', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=100, unique=True)),
                ('valor', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Estado Expedientes',
            },
        ),
        migrations.CreateModel(
            name='Etapa',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=100)),
                ('resolucion', models.IntegerField(default=0)),
                ('disposicion', models.IntegerField(default=0)),
                ('licitacion', models.IntegerField(default=0)),
                ('comodato', models.IntegerField(default=0)),
                ('servicio_medico', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('letra', models.CharField(max_length=1)),
                ('numero', models.CharField(max_length=15)),
                ('anio', models.CharField(max_length=2)),
                ('fecha', models.DateField(null=True, blank=True)),
                ('descripcion', models.CharField(max_length=500, null=True, blank=True)),
                ('clase', models.ForeignKey(null=True, to='expedientes.Clase', blank=True)),
                ('empleado_solicitante', models.ForeignKey(related_name='empleado_solicitante', null=True, to='empleados.Empleado', blank=True)),
                ('estado', models.ForeignKey(null=True, to='expedientes.Estado', blank=True)),
                ('etapa', models.ForeignKey(null=True, to='expedientes.Etapa', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Expediente',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteDisposicion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('contratacion_directa', models.IntegerField(null=True, blank=True)),
                ('importe', models.FloatField(null=True, blank=True)),
                ('numero_disposicion', models.IntegerField(null=True, blank=True)),
                ('fecha_disposicion', models.DateField(null=True, blank=True)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('expediente', models.OneToOneField(to='expedientes.Expediente', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Disposicion',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteLicitacion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('numero_licitacion', models.IntegerField(null=True, blank=True)),
                ('numero_disposicion', models.IntegerField(null=True, blank=True)),
                ('resolucion_aprobacion', models.CharField(max_length=100, null=True, blank=True)),
                ('fecha_resolucion_aprobacion', models.DateField(null=True, blank=True)),
                ('resolucion_adjudicacion', models.IntegerField(null=True, blank=True)),
                ('fecha_resolucion_adjudicacion', models.DateField(null=True, blank=True)),
                ('expediente', models.OneToOneField(to='expedientes.Expediente', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Licitación',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteLicitacionCompromiso',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('monto', models.FloatField(null=True, blank=True)),
                ('monto_total', models.FloatField(null=True, blank=True)),
                ('orden_provision', models.IntegerField(null=True, blank=True)),
                ('acta_recepcion', models.IntegerField(null=True, blank=True)),
                ('expediente_licitacion', models.ForeignKey(null=True, to='expedientes.ExpedienteLicitacion', blank=True)),
                ('proveedor', models.ForeignKey(null=True, to='proveedores.Proveedor', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Licitación - Etapa: Compromiso',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteResolucion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('resolucion_adjudicacion', models.IntegerField(null=True, blank=True)),
                ('fecha_resolucion_adjudicacion', models.DateField(null=True, blank=True)),
                ('importe', models.FloatField(null=True, blank=True)),
                ('tipo_transaccion', models.CharField(max_length=100, null=True, blank=True)),
                ('numero_identificacion_transaccion', models.IntegerField(null=True, blank=True)),
                ('orden_provision', models.IntegerField(null=True, blank=True)),
                ('acta_recepcion', models.IntegerField(null=True, blank=True)),
                ('numero_resolucion_pago', models.IntegerField(null=True, blank=True)),
                ('fecha_resolucion_pago', models.DateField(null=True, blank=True)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('expediente', models.OneToOneField(to='expedientes.Expediente', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Resolucion',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteServicioMedico',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('resolucion_contratacion', models.CharField(max_length=100, null=True, blank=True)),
                ('fecha_resolucion_contratacion', models.DateField(null=True, blank=True)),
                ('orden_provision', models.IntegerField(null=True, blank=True)),
                ('acta_recepcion', models.IntegerField(null=True, blank=True)),
                ('numero_resolucion_pago', models.IntegerField(null=True, blank=True)),
                ('fecha_resolucion_pago', models.DateField(null=True, blank=True)),
                ('importe', models.FloatField(null=True, blank=True)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('expediente', models.OneToOneField(to='expedientes.Expediente', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Servicios Medicos',
            },
        ),
        migrations.CreateModel(
            name='FuenteFinanciamiento',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('cuenta', models.CharField(max_length=100)),
                ('fondo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NumeroAutoincremental',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('numero', models.IntegerField()),
                ('tipo', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='expedienteserviciomedico',
            name='fuente_financiamiento',
            field=models.ForeignKey(null=True, to='expedientes.FuenteFinanciamiento', blank=True),
        ),
        migrations.AddField(
            model_name='expedienteserviciomedico',
            name='profesional',
            field=models.ForeignKey(related_name='profesional', null=True, to='empleados.Empleado', blank=True),
        ),
        migrations.AddField(
            model_name='expedienteserviciomedico',
            name='solicitante_resolucion_pago',
            field=models.ForeignKey(null=True, to='empleados.Empleado', blank=True),
        ),
        migrations.AddField(
            model_name='expedienteresolucion',
            name='fuente_financiamiento',
            field=models.ForeignKey(null=True, to='expedientes.FuenteFinanciamiento', blank=True),
        ),
        migrations.AddField(
            model_name='expedienteresolucion',
            name='proveedor',
            field=models.ForeignKey(null=True, to='proveedores.Proveedor', blank=True),
        ),
        migrations.AddField(
            model_name='expedientelicitacion',
            name='fuente_financiamiento',
            field=models.ForeignKey(null=True, to='expedientes.FuenteFinanciamiento', blank=True),
        ),
        migrations.AddField(
            model_name='expedientedisposicion',
            name='fuente_financiamiento',
            field=models.ForeignKey(null=True, to='expedientes.FuenteFinanciamiento', blank=True),
        ),
        migrations.AddField(
            model_name='expedientedisposicion',
            name='proveedor',
            field=models.ForeignKey(null=True, to='proveedores.Proveedor', blank=True),
        ),
    ]
