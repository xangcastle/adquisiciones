# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2019-02-18 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0006_auto_20190218_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='buro',
            field=models.CharField(blank=True, max_length=165, null=True, verbose_name='calificacion de credito'),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='r_legal',
            field=models.CharField(blank=True, max_length=165, null=True, verbose_name='Nombre del Representante Legal'),
        ),
    ]