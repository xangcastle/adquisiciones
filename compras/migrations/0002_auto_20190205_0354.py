# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2019-02-05 03:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evaluacion',
            options={'verbose_name_plural': 'evaluaciones'},
        ),
        migrations.RemoveField(
            model_name='proveedor',
            name='pago_anual',
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='fecha',
            field=models.DateField(),
        ),
    ]