# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2019-02-18 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0008_auto_20190218_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='tercerizacion',
            field=models.PositiveIntegerField(choices=[(1, 'NO'), (2, 'SI')], default=2, null=True),
        ),
    ]