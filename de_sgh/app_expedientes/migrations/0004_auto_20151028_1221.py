# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expedientes', '0003_expedientelicitacionordenado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expedientelicitacionordenado',
            name='acta_recepcion',
        ),
        migrations.RemoveField(
            model_name='expedientelicitacionordenado',
            name='fecha_resolucion_pago',
        ),
        migrations.RemoveField(
            model_name='expedientelicitacionordenado',
            name='monto',
        ),
        migrations.RemoveField(
            model_name='expedientelicitacionordenado',
            name='monto_total',
        ),
        migrations.RemoveField(
            model_name='expedientelicitacionordenado',
            name='numero_resolucion_pago',
        ),
        migrations.RemoveField(
            model_name='expedientelicitacionordenado',
            name='observaciones',
        ),
        migrations.RemoveField(
            model_name='expedientelicitacionordenado',
            name='orden_provision',
        ),
        migrations.RemoveField(
            model_name='expedientelicitacionordenado',
            name='proveedor',
        ),
        migrations.RemoveField(
            model_name='expedientelicitacionordenado',
            name='solicitante_resolucion_pago',
        ),
    ]
