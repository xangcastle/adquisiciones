# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2019-02-18 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0007_auto_20190218_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='relacionado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='tipo_riesgo',
            field=models.PositiveIntegerField(choices=[(1, 'BAJO'), (2, 'MEDIO'), (3, 'ALTO')], default=1, null=True),
        ),
    ]