# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0001_initial'),
        ('obrasocial', '0001_initial'),
        ('complementos', '0001_initial'),
        ('organigrama', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('apellido', models.CharField(blank=True, null=True, max_length=30)),
                ('nombre', models.CharField(blank=True, null=True, max_length=30)),
                ('numero_documento', models.CharField(blank=True, null=True, max_length=20)),
                ('fecha_nacimiento', models.DateField(default='1900-01-01')),
                ('foto', models.ImageField(upload_to='foto_personal', blank=True, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('estado_civil', models.ForeignKey(null=True, to='persona.EstadoCivil', blank=True)),
                ('etnia', models.ForeignKey(null=True, to='persona.Etnia', blank=True)),
                ('nivel_educacion', models.ForeignKey(null=True, to='persona.NivelEducacion', blank=True)),
                ('obra_social', models.ForeignKey(null=True, to='obrasocial.ObraSocial', blank=True)),
                ('profesion', models.ForeignKey(null=True, to='organigrama.Profesion', blank=True)),
                ('sexo', models.ForeignKey(null=True, to='persona.Sexo', blank=True)),
                ('tipo_documento', models.ForeignKey(null=True, to='persona.TipoDocumento', blank=True, default=1)),
            ],
            options={
                'ordering': ['apellido'],
            },
        ),
        migrations.CreateModel(
            name='PersonaObraSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('numero_afiliado', models.CharField(max_length=20)),
                ('fecha_emision', models.DateField(blank=True, null=True)),
                ('fecha_vencimiento', models.DateField(blank=True, null=True)),
                ('tipo_beneficiario', models.CharField(choices=[('T', 'Titular'), ('A', 'Adherente')], max_length=1)),
                ('habitual', models.BooleanField(default=True)),
                ('suspendida', models.BooleanField(default=False)),
                ('observacion', models.CharField(blank=True, null=True, max_length=100)),
                ('categoria', models.ForeignKey(to='complementos.Categoria')),
                ('motivo_suspension', models.ForeignKey(null=True, to='obrasocial.MotivoSuspension', blank=True)),
                ('obra_social', models.ForeignKey(to='obrasocial.ObraSocial', default=1)),
                ('parentesco', models.ForeignKey(null=True, to='persona.Parentesco', blank=True)),
                ('persona', models.ForeignKey(null=True, to='personas.Persona', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Personas - Obras Sociales',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('persona', models.OneToOneField(to='personas.Persona')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
