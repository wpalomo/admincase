# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateField(auto_now=True)),
                ('hora', models.TimeField(auto_now=True)),
                ('descripcion', models.TextField(max_length=3000)),
                ('persona', models.ForeignKey(to='personas.Persona')),
            ],
            options={
                'verbose_name_plural': 'Notas',
                'verbose_name': 'Nota',
            },
        ),
        migrations.CreateModel(
            name='TipoNota',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Notas',
                'verbose_name': 'Tipo de Nota',
            },
        ),
        migrations.AddField(
            model_name='nota',
            name='tipo_nota',
            field=models.ForeignKey(to='notas.TipoNota'),
        ),
        migrations.AddField(
            model_name='nota',
            name='usuario',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
