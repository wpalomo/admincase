# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministracionForma',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'Administracion y Formas',
            },
        ),
        migrations.CreateModel(
            name='Agrupado',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Agrupados',
            },
        ),
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Catalogos',
            },
        ),
        migrations.CreateModel(
            name='Composicion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('potencia_numerador', models.IntegerField(null=True, blank=True)),
                ('potencia_denominador', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Composicion de Medicamentos',
            },
        ),
        migrations.CreateModel(
            name='Envase',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Envase',
                'verbose_name_plural': 'Envases',
            },
        ),
        migrations.CreateModel(
            name='FormaFarmaceutica',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Formas Farmaceuticas',
            },
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Laboratorios',
            },
        ),
        migrations.CreateModel(
            name='LineaTerapeutica',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Lineas Terapeuticas',
            },
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('codigo', models.IntegerField(null=True, blank=True)),
                ('denominacion', models.CharField(max_length=100)),
                ('producto_combinado', models.BooleanField(default=False)),
                ('libre_azucar', models.BooleanField(default=False)),
                ('libre_conservante', models.BooleanField(default=False)),
                ('libre_cfc', models.BooleanField(default=False)),
                ('libre_gluten', models.BooleanField(default=False)),
                ('catalogo', models.ForeignKey(to='medicamentos.Catalogo', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Medicamentos',
            },
        ),
        migrations.CreateModel(
            name='MedicamentoLaboratorio',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre_comercial', models.CharField(max_length=100)),
                ('numero_certificado', models.IntegerField(null=True, blank=True)),
                ('numero_gtin', models.CharField(null=True, blank=True, max_length=40)),
                ('cantidad_envase_primario', models.IntegerField(null=True, blank=True)),
                ('cantidad_envase_secundario', models.IntegerField(null=True, blank=True)),
                ('agrupado_cantidad', models.IntegerField(null=True, blank=True)),
                ('pack_cantidad', models.IntegerField(null=True, blank=True)),
                ('pallet_cantidad', models.IntegerField(null=True, blank=True)),
                ('imagen_medicamento', models.ImageField(null=True, blank=True, upload_to='imagen_medicamento')),
                ('prospecto_medicamento', models.FileField(null=True, blank=True, upload_to='prospecto_medicamento')),
                ('agrupado_unidad', models.ForeignKey(to='medicamentos.Agrupado', null=True, blank=True)),
                ('envase_primario', models.ForeignKey(to='medicamentos.Envase', related_name='envase_primario', null=True, blank=True)),
                ('envase_secundario', models.ForeignKey(to='medicamentos.Envase', related_name='envase_secundario', null=True, blank=True)),
                ('forma_farmaceutica', models.ForeignKey(to='medicamentos.FormaFarmaceutica', null=True, blank=True)),
                ('laboratorio', models.ForeignKey(to='medicamentos.Laboratorio', null=True, blank=True)),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Medicamento - Laboratorios',
            },
        ),
        migrations.CreateModel(
            name='MedicamentoLineaTerapeutica',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('linea_terapeutica', models.ForeignKey(to='medicamentos.LineaTerapeutica', null=True, blank=True)),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Lineas Terapeuticas',
            },
        ),
        migrations.CreateModel(
            name='NumeroAutoincremental',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('numero', models.IntegerField()),
                ('tipo', models.OneToOneField(to='medicamentos.Catalogo', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Numero Autoincremental',
            },
        ),
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Packs de Unidades de Despachos',
            },
        ),
        migrations.CreateModel(
            name='Pallet',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Pallet de Unidades Logisticas',
            },
        ),
        migrations.CreateModel(
            name='PrincipioActivo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Principios Activos',
            },
        ),
        migrations.CreateModel(
            name='ViaAdministracion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Vias de Administracion',
            },
        ),
        migrations.AddField(
            model_name='medicamentolaboratorio',
            name='pack_unidad_despacho',
            field=models.ForeignKey(to='medicamentos.Pack', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='medicamentolaboratorio',
            name='pallet_unidad_logistica',
            field=models.ForeignKey(to='medicamentos.Pallet', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='medicamentolaboratorio',
            name='unidad_medida_envase_primario',
            field=models.ForeignKey(to='salud.UnidadMedida', related_name='unidad_medida_envase_primario', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='medicamentolaboratorio',
            name='unidad_medida_envase_secundario',
            field=models.ForeignKey(to='salud.UnidadMedida', related_name='unidad_medida_envase_secundario', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='formafarmaceutica',
            name='via_administracion',
            field=models.ForeignKey(to='medicamentos.ViaAdministracion', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='composicion',
            name='medicamento',
            field=models.ForeignKey(blank=True, to='medicamentos.Medicamento'),
        ),
        migrations.AddField(
            model_name='composicion',
            name='principio_activo',
            field=models.ForeignKey(to='medicamentos.PrincipioActivo', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='composicion',
            name='unidad_medida_denominador',
            field=models.ForeignKey(to='salud.UnidadMedida', related_name='unidad_medida_denominador', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='composicion',
            name='unidad_medida_numerador',
            field=models.ForeignKey(to='salud.UnidadMedida', related_name='unidad_medida_numerador', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='administracionforma',
            name='forma_farmaceutica',
            field=models.ForeignKey(to='medicamentos.FormaFarmaceutica', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='administracionforma',
            name='medicamento',
            field=models.ForeignKey(to='medicamentos.Medicamento', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='administracionforma',
            name='via_administracion',
            field=models.ForeignKey(to='medicamentos.ViaAdministracion', null=True, blank=True),
        ),
    ]
