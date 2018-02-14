# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-02-13 23:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now=True)),
                ('importacia', models.PositiveIntegerField(choices=[(15, 'SI'), (0, 'NO')], null=True, verbose_name='Importante para el funcionamiento estrategico del Banco y para atencion de clientes?')),
                ('complejidad', models.PositiveIntegerField(choices=[(10, 'ALTA'), (0, 'BAJA')], null=True, verbose_name='Complejidad de la contratacion')),
                ('reemplazo', models.PositiveIntegerField(choices=[(10, 'ALTA COMPLEJIDAD'), (0, 'COMPLEJIDAD ACEPTABLE')], null=True, verbose_name='Habilidad para reemplazar a la empresa por otra')),
                ('credito', models.PositiveIntegerField(choices=[(10, 'B, C, D o D'), (0, 'Excelentes (A), No encontrado/consultado, Ninguna')], null=True, verbose_name='Reputacion financiera y solvencia')),
                ('anual', models.PositiveIntegerField(choices=[(10, 'Mayor 5% Utilidades Netas del periodo anterior'), (0, 'Menor al 5% Utilidades Netas del periodo anterior')], null=True, verbose_name='Monto total anual pagado al proveedor')),
                ('incumplimiento', models.PositiveIntegerField(choices=[(10, 'SI'), (0, 'NO')], null=True, verbose_name='La interrupcion del servicio genera incumplimiento regulatorio/legales al Banco')),
                ('actividad', models.PositiveIntegerField(choices=[(8, 'SI'), (0, 'NO')], null=True, verbose_name='Importancia de la actividad a ser contratada en relacion al giro principal de negocios de la institucion')),
                ('recurrente', models.PositiveIntegerField(choices=[(7, 'Nueva Relacion'), (0, 'Contrato Recurrente')], null=True, verbose_name='Relacion del Proveedor de servicios con la institucion financiera')),
                ('transversal', models.PositiveIntegerField(choices=[(5, 'SI'), (0, 'NO')], null=True, verbose_name='Interrelacion de la operacion contratada con el resto de operacions de la institucion financiera')),
                ('incidencia', models.PositiveIntegerField(choices=[(5, 'ALTA INCIDENCIA'), (0, 'POCA INCIDENCIA')], null=True, verbose_name='Fallas del proveedor pone en riesgo las ganancias, solvencia, liquidez, capital, reputacion, fondeo o sistemas de control interno')),
                ('multicontrato', models.PositiveIntegerField(choices=[(5, 'MAYOR A DOS'), (0, 'DOS O MENOR')], null=True, verbose_name='Existen mas de dos contratos vigentes con este mismo proveedor')),
                ('marco', models.PositiveIntegerField(choices=[(5, 'INFORMAL'), (0, 'REGULADO')], null=True, verbose_name='Marco regulatorio del proveedor')),
                ('puntaje', models.PositiveIntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('documento', models.FileField(upload_to='expedientes')),
                ('fecha_vence', models.DateField()),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Expediente',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=15, verbose_name='Codigo del Proveedor')),
                ('codigo_cliente', models.CharField(max_length=15)),
                ('nombre', models.CharField(max_length=125)),
                ('actividad_economica', models.CharField(max_length=125, null=True, verbose_name='Actividad Comercial')),
                ('servicio', models.CharField(max_length=125, verbose_name='Servicios Prestados')),
                ('identificacion', models.CharField(max_length=24, verbose_name='RUC/CEDULA')),
                ('direccion', models.TextField(blank=True, max_length=600, null=True)),
                ('pago_anual', models.FloatField(blank=True, null=True)),
                ('forma_pago', models.CharField(choices=[('NC', 'NOTA DE CREDITO'), ('CK', 'CHEQUE'), ('TFI', 'TRANSFERENCIA INTERNACIONAL'), ('TFCI', 'TRANSFERENCIA CUENTA INTEGRA')], max_length=4)),
                ('contacto', models.CharField(blank=True, max_length=120, null=True)),
                ('email', models.EmailField(blank=True, max_length=120, null=True)),
                ('telefono', models.CharField(blank=True, max_length=60, null=True)),
                ('r_legal', models.CharField(blank=True, max_length=165, null=True, verbose_name='Nombre del Representante Legal')),
                ('buro', models.CharField(blank=True, max_length=165, null=True, verbose_name='calificacion de credito')),
                ('cuenta_cordobas', models.CharField(blank=True, max_length=18, null=True)),
                ('beneficiario_cordobas', models.CharField(blank=True, max_length=160, null=True)),
                ('cuenta_dolares', models.CharField(blank=True, max_length=18, null=True)),
                ('beneficiario_dolares', models.CharField(blank=True, max_length=160, null=True)),
                ('relacionado', models.BooleanField(default=False)),
                ('contrato', models.BooleanField(default=False)),
                ('activo', models.BooleanField(default=True)),
                ('temp_user', models.CharField(blank=True, max_length=125, null=True)),
                ('importacia', models.PositiveIntegerField(choices=[(15, 'SI'), (0, 'NO')], null=True, verbose_name='Importante para el funcionamiento estrategico del Banco y para atencion de clientes?')),
                ('complejidad', models.PositiveIntegerField(choices=[(10, 'ALTA'), (0, 'BAJA')], null=True, verbose_name='Complejidad de la contratacion')),
                ('reemplazo', models.PositiveIntegerField(choices=[(10, 'ALTA COMPLEJIDAD'), (0, 'COMPLEJIDAD ACEPTABLE')], null=True, verbose_name='Habilidad para reemplazar a la empresa por otra')),
                ('credito', models.PositiveIntegerField(choices=[(10, 'B, C, D o D'), (0, 'Excelentes (A), No encontrado/consultado, Ninguna')], null=True, verbose_name='Reputacion financiera y solvencia')),
                ('anual', models.PositiveIntegerField(choices=[(10, 'Mayor 5% Utilidades Netas del periodo anterior'), (0, 'Menor al 5% Utilidades Netas del periodo anterior')], null=True, verbose_name='Monto total anual pagado al proveedor')),
                ('incumplimiento', models.PositiveIntegerField(choices=[(10, 'SI'), (0, 'NO')], null=True, verbose_name='La interrupcion del servicio genera incumplimiento regulatorio/legales al Banco')),
                ('actividad', models.PositiveIntegerField(choices=[(8, 'SI'), (0, 'NO')], null=True, verbose_name='Importancia de la actividad a ser contratada en relacion al giro principal de negocios de la institucion')),
                ('recurrente', models.PositiveIntegerField(choices=[(7, 'Nueva Relacion'), (0, 'Contrato Recurrente')], null=True, verbose_name='Relacion del Proveedor de servicios con la institucion financiera')),
                ('transversal', models.PositiveIntegerField(choices=[(5, 'SI'), (0, 'NO')], null=True, verbose_name='Interrelacion de la operacion contratada con el resto de operacions de la institucion financiera')),
                ('incidencia', models.PositiveIntegerField(choices=[(5, 'ALTA INCIDENCIA'), (0, 'POCA INCIDENCIA')], null=True, verbose_name='Fallas del proveedor pone en riesgo las ganancias, solvencia, liquidez, capital, reputacion, fondeo o sistemas de control interno')),
                ('multicontrato', models.PositiveIntegerField(choices=[(5, 'MAYOR A DOS'), (0, 'DOS O MENOR')], null=True, verbose_name='Existen mas de dos contratos vigentes con este mismo proveedor')),
                ('marco', models.PositiveIntegerField(choices=[(5, 'INFORMAL'), (0, 'REGULADO')], null=True, verbose_name='Marco regulatorio del proveedor')),
                ('puntaje', models.PositiveIntegerField(default=0, null=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'proveedores',
            },
        ),
        migrations.AddField(
            model_name='expediente',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.Proveedor'),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.Proveedor'),
        ),
    ]