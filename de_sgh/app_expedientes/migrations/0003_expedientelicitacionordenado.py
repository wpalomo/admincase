# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '__first__'),
        ('empleados', '__first__'),
        ('expedientes', '0002_auto_20151023_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpedienteLicitacionOrdenado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('monto', models.FloatField(null=True, blank=True)),
                ('monto_total', models.FloatField(null=True, blank=True)),
                ('orden_provision', models.IntegerField(null=True, blank=True)),
                ('acta_recepcion', models.IntegerField(null=True, blank=True)),
                ('numero_resolucion_pago', models.IntegerField(null=True, blank=True)),
                ('fecha_resolucion_pago', models.DateField(null=True, blank=True)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('expediente_licitacion', models.ForeignKey(blank=True, to='expedientes.ExpedienteLicitacion', null=True)),
                ('proveedor', models.ForeignKey(blank=True, to='proveedores.Proveedor', null=True)),
                ('solicitante_resolucion_pago', models.ForeignKey(blank=True, to='empleados.Empleado', null=True)),
            ],
            options={
                'verbose_name_plural': 'Tipo Expediente: Licitación - Etapa: Ordenado',
            },
        ),
    ]
