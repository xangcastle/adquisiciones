# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.contrib.admin import site
import adminactions.actions as actions
from django.contrib import messages
from django import forms
from datetime import datetime
from django.contrib.admin.widgets import AdminDateWidget
import xlwt
from django.shortcuts import HttpResponse

actions.add_to_site(site)


class ReporteFecha(forms.Form):
    date = datetime.now()
    _referer = forms.CharField(widget=forms.HiddenInput, required=False)
    fecha_evaluacion = forms.DateField(label="Fecha de Evaluación", widget=AdminDateWidget, initial=date,
                                       required=True)


class ExpedienteTabular(admin.TabularInline):
    model = Expediente
    extra = 0
    classes = ('grp-collapse grp-open',)


@admin.register(Proveedor)
class ProveedorAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        usuario = request.user
        if usuario.is_superuser:
            return queryset
        else:
            return queryset.filter(usuario=usuario)

    list_display = ('nombre', 'identificacion', 'r_legal', 'servicio', 'email', 'telefono', 'puntaje')
    search_fields = ('codigo', 'codigo_cliente', 'nombre', 'identificacion', 'r_legal', 'servicio', 'email', 'telefono')
    list_filter = ('usuario', 'servicio', 'relacionado', 'contrato', 'activo', 'puntaje')

    fieldsets = (
        ('Datos Generales', {
            'classes': ('grp-collapse grp-open',),
            'fields': (
                ('codigo', 'codigo_cliente'), ('nombre', 'identificacion'),
                ('servicio', 'actividad_economica'), ('forma_pago', 'contacto'),
                'email', ('telefono', 'r_legal'), 'direccion',
                ('usuario', 'buro'),
                ('tipo_riesgo', 'tercerizacion')
            )
        }),
        ('Informacion Adicional', {
            'classes': ('grp-collapse grp-open',),
            'fields': (('cuenta_cordobas', 'beneficiario_cordobas'),
                       ('cuenta_dolares', 'beneficiario_dolares'),
                       ('relacionado', 'contrato'),
                       ('pago_anual', 'activo'),
                       ), })
    )

    inlines = [ExpedienteTabular, ]

    def generar_evaluacion(self, request, queryset):
        for o in queryset:
            e = Evaluacion()
            e.fecha = datetime.now()
            e.proveedor = o
            e.codigo = o.codigo
            e.codigo_cliente = o.codigo_cliente
            e.nombre = o.nombre
            e.identificacion = o.identificacion
            e.r_legal = o.r_legal
            e.servicio = o.servicio
            e.actividad_economica = o.actividad_economica
            e.email = o.email
            e.telefono = o.telefono
            e.direccion = o.direccion
            e.tipo_riesgo = o.tipo_riesgo
            e.tercerizacion = o.tercerizacion
            e.buro = o.buro
            e.relacionado = o.relacionado
            e.user = o.usuario
            e.save()
        messages.add_message(request, messages.INFO,
                             "%s formularios de evaluación fueron generados con éxito" % queryset.count())

    generar_evaluacion.short_description = "Generar evaluación de proveedores"

    def generar_usuarios(self, request, queryset):
        for o in queryset:
            o.get_user()
        messages.add_message(request, messages.INFO,
                             "%s usuarios fueron generados con éxito" % queryset.count())

    generar_usuarios.short_description = "Generar usuarios asignados"

    actions = [generar_evaluacion, generar_usuarios]


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha'
    change_form_template = "compras/evaluacion.html"
    list_display = ('nombre', 'identificacion', 'email', 'user', 'puntaje')
    readonly_fields = ('user', 'proveedor')
    list_filter = ('user', 'puntaje')
    search_fields = ('proveedor__nombre',)
    fields = (('user', 'proveedor'),
              ('codigo', 'codigo_cliente'),
              'r_legal',
              ('servicio', 'actividad_economica'),
              ('email', 'telefono'),
              'direccion',
              ('buro', 'relacionado'),
              ('tipo_riesgo', 'tercerizacion'),
              'importacia', 'complejidad',
              'reemplazo', 'credito', 'anual', 'incumplimiento', 'actividad',
              'recurrente', 'transversal', 'incidencia', 'multicontrato',
              'marco', 'puntaje')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        usuario = request.user
        if usuario.is_superuser:
            return queryset
        else:
            return queryset.filter(user=usuario)

    def reporte_evaluacion(self, request, queryset):
        primera_linea = ["Codigo",
                         "Nombre",
                         "Actividad Economica",
                         "Identificacion",
                         "Direccion",
                         "Contacto",
                         "Telefono",
                         "Relacionado",
                         "Monto Anual Facturado",
                         "Resultado de Consulta de Credito",

                         "Importante para el funcionamiento estrategico del Banco y para atencion de clientes?",
                         "Complejidad de la contratacion",
                         "Habilidad para reemplazar a la empresa por otra",
                         "Reputacion financiera y solvencia",
                         "Monto total anual pagado al proveedor",
                         "La interrupcion del servicio genera incumplimiento regulatorio/legales al Banco",
                         "Importancia de la actividad a ser contratada en relacion al giro principal de"
                         " negocios de la institucion",
                         "Relacion del Proveedor de servicios con la institucion financiera",
                         "Interrelacion de la operacion contratada con el resto de operacions "
                         "de la institucion financiera",
                         "Fallas del proveedor pone en riesgo las ganancias, solvencia, liquidez, "
                         "capital, reputacion, fondeo o sistemas de control interno",
                         "Existen mas de dos contratos vigentes con este mismo proveedor",

                         "Marco regulatorio del proveedor",
                         "¿Es tercerización?",
                         "Tipo de riesgo",
                         "¿Es materialmente importante?",
                         "Puntaje",
                         "Usuario Evaluador"
                         ]
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet("Reporte de Evaluacion")
        default_style = xlwt.Style.default_style
        fill_grey_style = xlwt.easyxf('pattern: back_color gray25;')
        c1 = 10
        c2 = 11
        for r, d in enumerate(primera_linea[:10]):
            sheet.write_merge(0, 1, r, r, d, style=fill_grey_style)
        for r, d in enumerate(primera_linea[10:22]):
            sheet.write_merge(0, 0, c1 + (r * 2), c2 + (r * 2), d, style=fill_grey_style)
            sheet.write(1, c1 + (r * 2), "Respuesta", style=fill_grey_style)
            sheet.write(1, c2 + (r * 2), "Valor", style=fill_grey_style)
        for r, d in enumerate(primera_linea[22:27]):
            sheet.write_merge(0, 1, r + 34, r + 34, d, style=fill_grey_style)

        data = datos_evaluacion(queryset)
        col = 0
        for r, d in enumerate(data):
            col = len(d)
            for c in range(0, col):
                sheet.write(r + 2, c, d[c], style=default_style)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Reporte de Evaluacion.xls'
        book.save(response)
        return response

    actions = [reporte_evaluacion, ]
