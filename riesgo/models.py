# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from compras.models import Proveedor
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Pais(models.Model):
    codigo = models.PositiveIntegerField(unique=True)
    pais = models.CharField(max_length=120)
    nacionalidad = models.CharField(max_length=120)
    iso_num = models.PositiveIntegerField(null=True, blank=True)
    iso_cha = models.CharField(max_length=3, null=True, blank=True)
    peso = models.PositiveIntegerField(null=True, blank=True)
    control = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nacionalidad

    class Meta:
        verbose_name_plural = "paises"
        ordering = ['nacionalidad', ]


class Jurisdiccion(models.Model):
    codigo = models.PositiveIntegerField(verbose_name="código pais")
    jurisdiccion = models.CharField(max_length=120)
    peso = models.PositiveIntegerField(null=True, blank=True)
    control = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.jurisdiccion

    class Meta:
        verbose_name_plural = "jurisdicciones"
        ordering = ['jurisdiccion', ]


class ActividadEconomica(models.Model):
    grupo = models.CharField(max_length=120)
    actividad = models.CharField(max_length=250)
    clasificacion = models.PositiveIntegerField()

    def __str__(self):
        return self.actividad

    class Meta:
        ordering = ['actividad', ]


class Profesion(models.Model):
    descripcion = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "profesiones"
        ordering = ['descripcion', ]

    def __str__(self):
        return self.descripcion


class NivelRiesgo(models.IntegerChoices):
    BAJO = 1, "Bajo"
    MEDIO = 2, "Medio"
    ALTO = 3, "Alto"


# region tipo de servicio
class AccesoSitema(models.IntegerChoices):
    BAJO = 1, "No tiene acceso"
    MEDIO = 2, "Tiene Acceso al Codigo Fuente del Sistema Propio del Puesto Bajo supervisión"
    ALTO = 3, "Tiene Acceso al Codigo Fuente del Sistema Propio del banco"


class AccesoEquipos(models.IntegerChoices):
    BAJO = 1, "No tiene acceso"
    MEDIO = 2, "No aplica"
    ALTO = 3, "Acceso como Administrador en los Equipos del banco"


class AccesoInfo(models.IntegerChoices):
    BAJO = 1, "No tiene acceso"
    MEDIO = 2, "No aplica"
    ALTO = 3, "Modifica información en los sistemas operativos del banco"


class AccesoRed(models.IntegerChoices):
    BAJO = 1, "No tiene acceso"
    MEDIO = 2, "Tiene acceso directo a la Base de Datos, Redes y seguridad informatica bajo supervisión"
    ALTO = 3, "Tiene acceso directo a la Base de Datos, Redes y seguridad informatica"


class TieneSucursal(models.IntegerChoices):
    BAJO = 1, "Posee sucursales a nivel nacional o no posee surcursales"
    MEDIO = 2, "Posee sucursales a nivel internacional pero no en Jurisdicciones de alto riesgo"
    ALTO = 3, "Posee Sucursales a nivel Internacional en Juridicciones de Alto Riesgo"


class UsaIntermediarios(models.IntegerChoices):
    BAJO = 1, "No utiliza intermediarios"
    MEDIO = 2, "No aplica"
    ALTO = 3, "Utiliza Intermediarios para realizar su función"


# endregion


# region ddp
class EnLista(models.IntegerChoices):
    BAJO = 1, "No hay coincidencias en listas"
    MEDIO = 2, "No aplica"
    ALTO = 3, "Filtros en las Lista de Riesgo nacionales, internacionales y de referencia"


class MaterialmenteImportante(models.IntegerChoices):
    BAJO = 1, "Es inmaterialmente importante"
    MEDIO = 2, "Es Materialmente Importante entre 50% y  60%"
    ALTO = 3, "Es Materialmente Importante  de 61% a mas"


class EsCliente(models.IntegerChoices):
    BAJO = 1, "Es cliente del banco"
    MEDIO = 2, "No aplica"
    ALTO = 3, "No posee cuentas PB"


class TieneAlerta(models.IntegerChoices):
    BAJO = 1, "No ha presentado"
    MEDIO = 2, "No aplica"
    ALTO = 3, "Ha presentado alguna señal de alerta"


class EvaProveedor(models.IntegerChoices):
    BAJO = 1, "Su evaluación desempeño  como Proveedor de Servicios es mayor a 80%"
    MEDIO = 2, "Su evaluación desempeño  como Proveedor de Servicios esta entre %51 y 79% "
    ALTO = 3, "Su evaluación desempeño  como Proveedor de Servicios es Menor al 50%"


class NoContingencia(models.IntegerChoices):
    BAJO = 1, "Posee Plan de Continuidad de Negocios y/o Plan de contingecia"
    MEDIO = 2, "No aplica"
    ALTO = 3, "No Posee Plan de Continuidad de Negocios y/o Plan de contingecia"


class TieneExperiencia(models.IntegerChoices):
    BAJO = 1, "Tiene amplia experiencia en la materia"
    MEDIO = 2, "No aplica"
    ALTO = 3, "Su experiencia como Proveedor de servicio es menor a 3 años"


class EstadosFinancieros(models.IntegerChoices):
    BAJO = 1, "Estados financieros auditados actualizados (según aplique)"
    MEDIO = 2, "Estados financieros auditados (según aplique) desactualizados"
    ALTO = 3, "No posee Estados financieros auditados (según aplique)"


class TieneQuejas(models.IntegerChoices):
    BAJO = 1, "No ha tenido quejas, mala reputación, incumplimientos o litigios"
    MEDIO = 2, "No aplica"
    ALTO = 3, "Reputación comercial, quejas, cumplimiento y litigios pendientes"


# endregion

class EvaluacionRiesgo(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="usuario")
    proveedor = models.ForeignKey(Proveedor, null=True, blank=True, on_delete=models.SET_NULL)
    # riesgo en servicios
    acceso_sistema = models.PositiveIntegerField(choices=AccesoSitema.choices, default=AccesoSitema.BAJO,
                                                 verbose_name="¿Tiene Acceso al código fuente del"
                                                              " sistema propio del banco?")
    acceso_equipos = models.PositiveIntegerField(choices=AccesoEquipos.choices, default=AccesoEquipos.BAJO,
                                                 verbose_name="¿Tiene acceso como administrador en "
                                                              "los equipos del banco?")
    acceso_info = models.PositiveIntegerField(choices=AccesoInfo.choices, default=AccesoInfo.BAJO,
                                              verbose_name="¿Modifica información en los "
                                                           "sistemas operativos del banco?")
    acceso_red = models.PositiveIntegerField(choices=AccesoRed.choices, default=AccesoRed.BAJO,
                                             verbose_name="¿Tiene acceso directo a la base de datos, "
                                                          "redes y seguridad informatica?")
    tiene_sucursal = models.PositiveIntegerField(choices=TieneSucursal.choices, default=TieneSucursal.BAJO,
                                                 verbose_name="¿Posee sucursales a nivel internacional "
                                                              "en juridicciones de alto riesgo?")
    usa_intermediarios = models.PositiveIntegerField(choices=UsaIntermediarios.choices, default=UsaIntermediarios.BAJO,
                                                     verbose_name="¿Utiliza intermediarios para realizar su función?")
    # riesgo ddp
    en_lista = models.PositiveIntegerField(choices=EnLista.choices, default=EnLista.BAJO,
                                           verbose_name="¿Tiene filtros en las lista de riesgo nacionales, "
                                                        "internacionales y de referencia?")
    materialmente_importante = models.PositiveIntegerField(choices=MaterialmenteImportante.choices,
                                                           default=MaterialmenteImportante.BAJO,
                                                           verbose_name="¿Es materialmente importante?")
    es_cliente = models.PositiveIntegerField(choices=EsCliente.choices, default=EsCliente.BAJO,
                                             verbose_name="¿Es cliente del banco?")
    tiene_alerta = models.PositiveIntegerField(choices=UsaIntermediarios.choices,
                                               default=UsaIntermediarios.BAJO,
                                               verbose_name="¿Ha presentado alguna señal de alerta?")
    evaluacion_proveedor = models.PositiveIntegerField(choices=EvaProveedor.choices,
                                                       default=EvaProveedor.BAJO,
                                                       verbose_name="¿Como es su evaluación desempeño "
                                                                    "como proveedor de servicios?")
    no_contingencia = models.PositiveIntegerField(choices=NoContingencia.choices,
                                                  default=NoContingencia.BAJO,
                                                  verbose_name="¿Posee Plan de Continuidad de Negocios "
                                                               "y/o Plan de contingecia?")
    tiene_experiencia = models.PositiveIntegerField(choices=TieneExperiencia.choices,
                                                    default=TieneExperiencia.BAJO,
                                                    verbose_name="¿Tiene experiencia en la materia?")
    estados_financieros = models.PositiveIntegerField(choices=EstadosFinancieros.choices,
                                                      default=EstadosFinancieros.BAJO,
                                                      verbose_name="¿Tiene estados financieros auditados?")
    tiene_quejas = models.PositiveIntegerField(choices=TieneQuejas.choices,
                                               default=TieneQuejas.BAJO,
                                               verbose_name="¿Ha ha tenido quejas, mala reputación, "
                                                            "incumplimientos o litigios?"
                                               )
    # riesgo ldft
    actividad_economica = models.ForeignKey(ActividadEconomica, null=True, on_delete=models.SET_NULL,
                                            verbose_name="Actividad económica")
    jurisdiccion = models.ForeignKey(Jurisdiccion, null=True, on_delete=models.SET_NULL)
    nacionalidad = models.ForeignKey(Pais, null=True, on_delete=models.SET_NULL)
    riesgo_tipo_servicio = models.FloatField(null=True, blank=True,
                                             verbose_name="Nivel riesgo ripo de servicio")
    riesgo_proveedor = models.FloatField(null=True, blank=True,
                                         verbose_name="Nivel riesgo debida diligencia proveedor")
    nivel_riesgo = models.PositiveIntegerField(choices=NivelRiesgo.choices, null=True, blank=True)
    calculo_riesgo = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "evaluación de riesgo"
        verbose_name_plural = "evaluaciones de riesgo"

    @property
    def riesgo_nacionalidad(self):
        if self.nacionalidad:
            return self.nacionalidad.peso
        else:
            return 0

    @property
    def riesgo_jurisdiccion(self):
        if self.jurisdiccion:
            return self.jurisdiccion.peso
        else:
            return 0


@receiver(pre_save, sender=EvaluacionRiesgo)
def calcular_evaluacion(sender, instance, **kwargs):
    instance.riesgo_tipo_servicio = round((instance.acceso_sistema + instance.acceso_equipos
                                           + instance.acceso_info + instance.acceso_red
                                           + instance.tiene_sucursal + instance.usa_intermediarios) / 6, 2)
    instance.riesgo_proveedor = round((instance.en_lista + instance.materialmente_importante
                                       + instance.es_cliente + instance.tiene_alerta
                                       + instance.evaluacion_proveedor + instance.no_contingencia
                                       + instance.tiene_experiencia + instance.estados_financieros
                                       + instance.tiene_quejas) / 9, 2)
    instance.calculo_riesgo = round((instance.riesgo_tipo_servicio + instance.riesgo_proveedor
                                     + instance.riesgo_nacionalidad + instance.riesgo_jurisdiccion) / 4, 2)

    instance.nivel_riesgo = int(round(instance.calculo_riesgo, 0))
