# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0001_initial'),
        ('complementos', '0001_initial'),
        ('locacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FichaSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('numero_ficha', models.CharField(blank=True, max_length=50, unique=True, null=True)),
                ('ultima_verificacion', models.DateField(blank=True, null=True)),
                ('lugar_trabajo', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion_domicilio', models.TextField(blank=True, null=True)),
                ('codigo_postal', models.CharField(blank=True, max_length=20, null=True)),
                ('observacion_socio_economica', models.TextField(blank=True, null=True)),
                ('barrio', models.ForeignKey(blank=True, null=True, to='locacion.Barrio')),
                ('departamento', models.ForeignKey(blank=True, null=True, to='locacion.Departamento')),
                ('localidad', models.ForeignKey(blank=True, null=True, to='locacion.Localidad')),
            ],
            options={
                'verbose_name': 'Ficha Social',
                'verbose_name_plural': 'Fichas Sociales',
            },
        ),
        migrations.CreateModel(
            name='OtroServicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Otro Servicio',
                'verbose_name_plural': 'Otros Servicios',
            },
        ),
        migrations.CreateModel(
            name='ServicioAgua',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Servicio de Agua',
                'verbose_name_plural': 'Servicios de Agua',
            },
        ),
        migrations.CreateModel(
            name='ServicioLuzElectrica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Servicio de Luz Eléctrica',
                'verbose_name_plural': 'Servicios de Luz Electrica',
            },
        ),
        migrations.CreateModel(
            name='SituacionPropiedad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Situación de la Propiedad',
                'verbose_name_plural': 'Situaciones de la Propiedad',
            },
        ),
        migrations.CreateModel(
            name='TerrenoPropio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Terreno Propio',
                'verbose_name_plural': 'Terrenos Propios',
            },
        ),
        migrations.CreateModel(
            name='TipoBanio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo de Baño',
                'verbose_name_plural': 'Tipos de Baños',
            },
        ),
        migrations.CreateModel(
            name='TipoConstruccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo de Construcción',
                'verbose_name_plural': 'Tipos de Construcciones',
            },
        ),
        migrations.CreateModel(
            name='TipoPared',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo de Pared',
                'verbose_name_plural': 'Tipos de Paredes',
            },
        ),
        migrations.CreateModel(
            name='TipoPiso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo de Piso',
                'verbose_name_plural': 'Tipos de Pisos',
            },
        ),
        migrations.CreateModel(
            name='TipoProgramaSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Tipo de Programa Social',
                'verbose_name_plural': 'Tipos de Programas Sociales',
            },
        ),
        migrations.CreateModel(
            name='TipoTecho',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo de Baño',
                'verbose_name_plural': 'Tipos de Techos',
            },
        ),
        migrations.CreateModel(
            name='TipoVivienda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('descripcion', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo de Vivienda',
                'verbose_name_plural': 'Tipos de Viviendas',
            },
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='otro_servicio',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.OtroServicio'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='paciente',
            field=models.OneToOneField(to='pacientes.Paciente'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='pais',
            field=models.ForeignKey(blank=True, null=True, to='locacion.Pais'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='programa_social',
            field=models.ManyToManyField(blank=True, to='fichassociales.TipoProgramaSocial'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='provincia',
            field=models.ForeignKey(blank=True, null=True, to='locacion.Provincia'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='servicio_agua',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.ServicioAgua'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='servicio_luz_electrica',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.ServicioLuzElectrica'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='situacion_propiedad',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.SituacionPropiedad'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='terreno_propio',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.TerrenoPropio'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='tipo_banio',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.TipoBanio'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='tipo_construccion',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.TipoConstruccion'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='tipo_iva',
            field=models.ForeignKey(blank=True, null=True, to='complementos.TipoIVA'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='tipo_pared',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.TipoPared'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='tipo_piso',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.TipoPiso'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='tipo_techo',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.TipoTecho'),
        ),
        migrations.AddField(
            model_name='fichasocial',
            name='tipo_vivienda',
            field=models.ForeignKey(blank=True, null=True, to='fichassociales.TipoVivienda'),
        ),
    ]
