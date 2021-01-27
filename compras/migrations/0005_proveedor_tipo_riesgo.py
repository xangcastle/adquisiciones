# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2019-02-05 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0004_auto_20190205_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='tipo_riesgo',
            field=models.PositiveIntegerField(choices=[(1, 'BAJO'), (2, 'MEDIO'), (3, 'ALTO')], default=1, null=True),
        ),
    ]