# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arbolitem', '0001_initial'),
        ('empleados', '0001_initial'),
        ('instituciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpleadoAgenda',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('tiene_agenda', models.BooleanField(default=True)),
                ('empleado', models.ForeignKey(to='empleados.Empleado')),
            ],
            options={
                'verbose_name_plural': 'Permisos Empleado-Agenda',
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=500, null=True)),
                ('valor', models.CharField(blank=True, max_length=100, null=True)),
                ('institucion', models.ForeignKey(to='instituciones.Institucion', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Perfiles',
            },
        ),
        migrations.CreateModel(
            name='PerfilModulo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('modulo', models.ForeignKey(to='arbolitem.ArbolItem')),
                ('perfil', models.ForeignKey(to='seguridad.Perfil')),
            ],
            options={
                'verbose_name_plural': 'Perfiles-Modulos',
            },
        ),
    ]
