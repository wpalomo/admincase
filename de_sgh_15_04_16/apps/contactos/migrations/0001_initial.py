# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('proveedor', models.CharField(blank=True, null=True, max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
                ('observacion', models.TextField(blank=True, null=True, max_length=200)),
                ('persona', models.ForeignKey(to='personas.Persona')),
            ],
            options={
                'verbose_name': 'Contacto',
                'verbose_name_plural': 'Contactos',
            },
        ),
        migrations.CreateModel(
            name='TipoContacto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Tipo de contacto',
                'verbose_name_plural': 'Tipos de contactos',
            },
        ),
        migrations.AddField(
            model_name='contacto',
            name='tipo_contacto',
            field=models.ForeignKey(to='contactos.TipoContacto', blank=True, null=True),
        ),
    ]
