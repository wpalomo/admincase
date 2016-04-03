# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '__first__'),
        ('empleados', '__first__'),
        ('expedientes', '0005_auto_20151028_1228'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpedienteComodato',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('resolucion_contratacion', models.IntegerField(blank=True, null=True)),
                ('fecha_resolucion_contratacion', models.DateField(blank=True, null=True)),
                ('numero_contratacion_directa', models.IntegerField(blank=True, null=True)),
                ('importe', models.FloatField(blank=True, null=True)),
                ('orden_provision', models.IntegerField(blank=True, null=True)),
                ('resolucion_pago', models.IntegerField(blank=True, null=True)),
                ('fecha_resolucion_pago', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('expediente', models.ForeignKey(to='expedientes.Expediente')),
                ('fuente_financiamiento', models.ForeignKey(to='expedientes.FuenteFinanciamiento', blank=True, null=True)),
                ('proveedor', models.ForeignKey(to='proveedores.Proveedor', blank=True, null=True)),
                ('solicitante_resolucion_pago', models.ForeignKey(to='empleados.Empleado', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Comodato',
            },
        ),
        migrations.AlterModelOptions(
            name='expedientelicitacion',
            options={'verbose_name_plural': 'Tipo Expediente: Licitacion'},
        ),
        migrations.AlterModelOptions(
            name='expedientelicitacioncompromiso',
            options={'verbose_name_plural': 'Tipo Expediente: Licitacion - Etapa: Compromiso'},
        ),
        migrations.AlterModelOptions(
            name='expedientelicitacionordenado',
            options={'verbose_name_plural': 'Tipo Expediente: Licitacion - Etapa: Ordenado'},
        ),
    ]
