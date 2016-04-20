# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('proveedor', models.CharField(null=True, blank=True, max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
                ('observacion', models.TextField(null=True, blank=True, max_length=200)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
