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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=100)),
                ('resolucion', models.IntegerField(default=0)),
                ('disposicion', models.IntegerField(default=0)),
                ('licitacion', models.IntegerField(default=0)),
                ('comodato', models.IntegerField(default=0)),
                ('servicio_medico', models.IntegerField(default=0)),
                ('resoluciones_varias', models.IntegerField(default=0)),
                ('resolucion_contratacion', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('letra', models.CharField(blank=True, max_length=1, null=True)),
                ('numero', models.CharField(blank=True, max_length=15, null=True)),
                ('anio', models.CharField(blank=True, max_length=2, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=500, null=True)),
                ('clase', models.ForeignKey(blank=True, to='expedientes.Clase', null=True)),
                ('empleado_solicitante', models.ForeignKey(blank=True, to='empleados.Empleado', null=True, related_name='empleado_solicitante')),
                ('estado', models.ForeignKey(blank=True, to='expedientes.Estado', null=True)),
                ('etapa', models.ForeignKey(blank=True, to='expedientes.Etapa', null=True)),
            ],
            options={
                'verbose_name_plural': 'Expediente',
                'ordering': ['-fecha', '-numero', '-anio'],
            },
        ),
        migrations.CreateModel(
            name='ExpedienteComodato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resolucion_contratacion', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_resolucion_contratacion', models.DateField(blank=True, null=True)),
                ('numero_contratacion_directa', models.IntegerField(blank=True, null=True)),
                ('importe', models.FloatField(blank=True, null=True)),
                ('orden_provision', models.IntegerField(blank=True, null=True)),
                ('resolucion_pago', models.IntegerField(blank=True, null=True)),
                ('fecha_resolucion_pago', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('expediente', models.ForeignKey(to='expedientes.Expediente')),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Comodato',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteDisposicion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contratacion_directa', models.IntegerField(blank=True, null=True)),
                ('importe', models.FloatField(blank=True, null=True)),
                ('numero_disposicion', models.IntegerField(blank=True, null=True)),
                ('fecha_disposicion', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('expediente', models.OneToOneField(blank=True, to='expedientes.Expediente')),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Disposicion',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteLicitacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('anio', models.IntegerField(blank=True, null=True)),
                ('numero_disposicion', models.IntegerField(blank=True, null=True)),
                ('resolucion_aprobacion', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_resolucion_aprobacion', models.DateField(blank=True, null=True)),
                ('resolucion_adjudicacion', models.IntegerField(blank=True, null=True)),
                ('fecha_resolucion_adjudicacion', models.DateField(blank=True, null=True)),
                ('expediente', models.OneToOneField(blank=True, to='expedientes.Expediente')),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Licitacion',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteLicitacionCompromiso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monto', models.FloatField(blank=True, null=True)),
                ('monto_total', models.FloatField(blank=True, null=True)),
                ('orden_provision', models.IntegerField(blank=True, null=True)),
                ('acta_recepcion', models.IntegerField(blank=True, null=True)),
                ('expediente_licitacion', models.ForeignKey(blank=True, to='expedientes.ExpedienteLicitacion', null=True)),
                ('proveedor', models.ForeignKey(blank=True, to='proveedores.Proveedor', null=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Licitacion - Etapa: Compromiso',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteLicitacionOrdenado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monto', models.FloatField(blank=True, null=True)),
                ('monto_total', models.FloatField(blank=True, null=True)),
                ('orden_provision', models.IntegerField(blank=True, null=True)),
                ('acta_recepcion', models.IntegerField(blank=True, null=True)),
                ('numero_resolucion_pago', models.IntegerField(blank=True, null=True)),
                ('fecha_resolucion_pago', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('expediente_licitacion', models.ForeignKey(blank=True, to='expedientes.ExpedienteLicitacion', null=True)),
                ('proveedor', models.ForeignKey(blank=True, to='proveedores.Proveedor', null=True)),
                ('solicitante_resolucion_pago', models.ForeignKey(blank=True, to='empleados.Empleado', null=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Licitacion - Etapa: Ordenado',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteResolucion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caja_chica', models.CharField(blank=True, max_length=1, default=0, null=True)),
                ('resolucion_adjudicacion', models.CharField(blank=True, max_length=4, null=True)),
                ('fecha_resolucion_adjudicacion', models.DateField(blank=True, null=True)),
                ('importe', models.FloatField(blank=True, null=True)),
                ('tipo_transaccion', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_identificacion_transaccion', models.CharField(blank=True, max_length=4, null=True)),
                ('orden_provision', models.CharField(blank=True, max_length=4, null=True)),
                ('acta_recepcion', models.CharField(blank=True, max_length=4, null=True)),
                ('numero_resolucion_pago', models.CharField(blank=True, max_length=4, null=True)),
                ('fecha_resolucion_pago', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('expediente', models.OneToOneField(blank=True, to='expedientes.Expediente')),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Resolucion',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteResolucionContratacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero_resolucion', models.IntegerField(blank=True, null=True)),
                ('fecha_resolucion', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('expediente', models.OneToOneField(blank=True, to='expedientes.Expediente')),
                ('proveedor', models.ForeignKey(blank=True, to='proveedores.Proveedor', null=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Resolucion Contratacion',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteResolucionesVarias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resolucion_pago', models.IntegerField(blank=True, null=True)),
                ('fecha_resolucion_pago', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('expediente', models.OneToOneField(blank=True, to='expedientes.Expediente')),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Resoluciones Varias',
            },
        ),
        migrations.CreateModel(
            name='ExpedienteServicioMedico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resolucion_contratacion', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_contratacion', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_resolucion_contratacion', models.DateField(blank=True, null=True)),
                ('orden_provision', models.IntegerField(blank=True, null=True)),
                ('acta_recepcion', models.IntegerField(blank=True, null=True)),
                ('numero_resolucion_pago', models.IntegerField(blank=True, null=True)),
                ('fecha_resolucion_pago', models.DateField(blank=True, null=True)),
                ('importe', models.FloatField(blank=True, null=True)),
                ('tipo_transaccion', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_identificacion_transaccion', models.CharField(blank=True, max_length=4, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('expediente', models.OneToOneField(blank=True, to='expedientes.Expediente')),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Servicios Medicos',
            },
        ),
        migrations.CreateModel(
            name='FuenteFinanciamiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuenta', models.CharField(max_length=100)),
                ('fondo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NumeroAutoincremental',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField()),
                ('tipo', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServicioAdministracion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoResolucion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='expedienteserviciomedico',
            name='fuente_financiamiento',
            field=models.ForeignKey(blank=True, to='expedientes.FuenteFinanciamiento', null=True),
        ),
        migrations.AddField(
            model_name='expedienteserviciomedico',
            name='profesional',
            field=models.ForeignKey(blank=True, to='empleados.Empleado', null=True, related_name='profesional'),
        ),
        migrations.AddField(
            model_name='expedienteserviciomedico',
            name='servicio_administracion',
            field=models.ForeignKey(blank=True, to='expedientes.ServicioAdministracion', null=True),
        ),
        migrations.AddField(
            model_name='expedienteserviciomedico',
            name='solicitante_resolucion_pago',
            field=models.ForeignKey(blank=True, to='empleados.Empleado', null=True),
        ),
        migrations.AddField(
            model_name='expedienteresolucion',
            name='fuente_financiamiento',
            field=models.ForeignKey(blank=True, to='expedientes.FuenteFinanciamiento', null=True),
        ),
        migrations.AddField(
            model_name='expedienteresolucion',
            name='proveedor',
            field=models.ForeignKey(blank=True, to='proveedores.Proveedor', null=True),
        ),
        migrations.AddField(
            model_name='expedientelicitacion',
            name='fuente_financiamiento',
            field=models.ForeignKey(blank=True, to='expedientes.FuenteFinanciamiento', null=True),
        ),
        migrations.AddField(
            model_name='expedientedisposicion',
            name='fuente_financiamiento',
            field=models.ForeignKey(blank=True, to='expedientes.FuenteFinanciamiento', null=True),
        ),
        migrations.AddField(
            model_name='expedientedisposicion',
            name='proveedor',
            field=models.ForeignKey(blank=True, to='proveedores.Proveedor', null=True),
        ),
        migrations.AddField(
            model_name='expedientecomodato',
            name='fuente_financiamiento',
            field=models.ForeignKey(blank=True, to='expedientes.FuenteFinanciamiento', null=True),
        ),
        migrations.AddField(
            model_name='expedientecomodato',
            name='proveedor',
            field=models.ForeignKey(blank=True, to='proveedores.Proveedor', null=True),
        ),
        migrations.AddField(
            model_name='expedientecomodato',
            name='solicitante_resolucion_pago',
            field=models.ForeignKey(blank=True, to='empleados.Empleado', null=True),
        ),
        migrations.AddField(
            model_name='expediente',
            name='tipo_resolucion',
            field=models.ForeignKey(blank=True, to='expedientes.TipoResolucion', null=True),
        ),
    ]
