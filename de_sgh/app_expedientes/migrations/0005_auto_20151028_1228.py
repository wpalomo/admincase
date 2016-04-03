# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '__first__'),
        ('proveedores', '__first__'),
        ('expedientes', '0004_auto_20151028_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='expedientelicitacionordenado',
            name='acta_recepcion',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='expedientelicitacionordenado',
            name='fecha_resolucion_pago',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='expedientelicitacionordenado',
            name='monto',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='expedientelicitacionordenado',
            name='monto_total',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='expedientelicitacionordenado',
            name='numero_resolucion_pago',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='expedientelicitacionordenado',
            name='observaciones',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='expedientelicitacionordenado',
            name='orden_provision',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='expedientelicitacionordenado',
            name='proveedor',
            field=models.ForeignKey(null=True, blank=True, to='proveedores.Proveedor'),
        ),
        migrations.AddField(
            model_name='expedientelicitacionordenado',
            name='solicitante_resolucion_pago',
            field=models.ForeignKey(null=True, blank=True, to='empleados.Empleado'),
        ),
    ]
