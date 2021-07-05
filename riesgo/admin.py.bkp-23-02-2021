from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
import xlwt
from django.shortcuts import HttpResponse


@admin.register(Profesion)
class ProfesionAdmin(ImportExportModelAdmin):
    search_fields = ('descripcion',)


@admin.register(ActividadEconomica)
class ActividadEconomicaAdmin(ImportExportModelAdmin):
    search_fields = ('grupo', 'actividad')
    list_display = ('grupo', 'actividad', 'clasificacion')


@admin.register(Pais)
class PaisAdmin(ImportExportModelAdmin):
    search_fields = ('codigo', 'pais', 'nacionalidad', 'iso_num', 'iso_cha')
    list_display = ('codigo', 'pais', 'nacionalidad', 'iso_num', 'iso_cha')


@admin.register(Jurisdiccion)
class JurisdiccionAdmin(ImportExportModelAdmin):
    search_fields = ('codigo', 'jurisdiccion', 'peso', 'control')
    list_display = ('codigo', 'jurisdiccion', 'peso', 'control')


@admin.register(EvaluacionRiesgo)
class EvaluacionRiesgoAdmin(ImportExportModelAdmin):
    date_hierarchy = 'created'
    list_display = ('proveedor', 'user', 'nivel_riesgo', 'calculo_riesgo')
    fieldsets = (
        ('', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                'proveedor',
                'user',
            )
        }),
        ('Evaluación según tipo de servicio', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                'acceso_sistema',
                'acceso_equipos',
                'acceso_info',
                'acceso_red',
                'tiene_sucursal',
                'usa_intermediarios',
                'riesgo_tipo_servicio',
            )
        }),
        ('Evaluación de riesgo DDP', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                'en_lista',
                'materialmente_importante',
                'es_cliente',
                'tiene_alerta',
                'evaluacion_proveedor',
                'no_contingencia',
                'tiene_experiencia',
                'estados_financieros',
                'tiene_quejas',
                'riesgo_proveedor',
            )
        }),
        ('Evaluación de riesgo LDFT', {
            'classes': ('grp-collapse', 'grp-open'),
            'fields': (
                'actividad_economica',
                'nacionalidad',
                'jurisdiccion',
                'nivel_riesgo',
                'calculo_riesgo',
            )
        }),
    )
    readonly_fields = ('riesgo_tipo_servicio', 'riesgo_proveedor', 'nivel_riesgo', 'calculo_riesgo',
                       'proveedor', 'user')

    change_list_template = "riesgo/evaluacion_change_list.html"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        usuario = request.user
        if usuario.is_superuser:
            return queryset
        else:
            return queryset.filter(user=usuario)

    @staticmethod
    def write_header(sheet):
        fill_grey_style = xlwt.easyxf('pattern: back_color gray25;')
        primera_linea = ["Codigo", "Nombre", "Actividad Economica",
                         "Identificacion", "Direccion", "Contacto",
                         "Telefono", "Monto Anual Facturado", "Resultado de Consulta de Credito",

                         "¿Tiene Acceso al código fuente del"
                         " sistema propio del banco?",
                         "¿Tiene acceso como administrador en "
                         "los equipos del banco?",
                         "¿Modifica información en los "
                         "sistemas operativos del banco?",
                         "¿Tiene acceso directo a la base de datos, "
                         "redes y seguridad informatica?",
                         "¿Posee sucursales a nivel internacional "
                         "en juridicciones de alto riesgo?",
                         "¿Utiliza intermediarios para realizar su función?",
                         "¿Tiene filtros en las lista de riesgo nacionales, "
                         "internacionales y de referencia?",
                         "¿Es materialmente importante?",
                         "¿Es cliente del banco?",
                         "¿Ha presentado alguna señal de alerta?",
                         "¿Como es su evaluación desempeño "
                         "como proveedor de servicios?",
                         "¿Posee Plan de Continuidad de Negocios "
                         "y/o Plan de contingecia?",
                         "¿Tiene experiencia en la materia?",
                         "¿Tiene estados financieros auditados?",
                         "¿Ha ha tenido quejas, mala reputación, "
                         "incumplimientos o litigios?",

                         "Actividad económica",
                         "Nacionalidad",
                         "Jurisdicción",
                         "Nivel riesgo ripo de servicio",
                         "Nivel riesgo debida diligencia proveedor",
                         "Nivel de riesto",
                         "Cálculo de riesgo",
                         "Usuario Evaluador"
                         ]
        c1 = 9
        c2 = 10
        for r, d in enumerate(primera_linea[:9]):
            sheet.write_merge(0, 1, r, r, d, style=fill_grey_style)
        for r, d in enumerate(primera_linea[9:27]):
            sheet.write_merge(0, 0, c1 + (r * 2), c2 + (r * 2), d, style=fill_grey_style)
            sheet.write(1, c1 + (r * 2), "Respuesta", style=fill_grey_style)
            sheet.write(1, c2 + (r * 2), "Valor", style=fill_grey_style)
        for r, d in enumerate(primera_linea[27:35]):
            sheet.write_merge(0, 1, r + 45, r + 45, d, style=fill_grey_style)

    @staticmethod
    def datos_evaluacion(evaluaciones):
        data = []
        for p in EvaluacionRiesgo.objects.all():
            row = [
                p.proveedor.codigo_cliente, p.proveedor.nombre, p.proveedor.actividad_economica,
                p.proveedor.identificacion, p.proveedor.direccion, p.proveedor.contacto,
                p.proveedor.telefono, p.proveedor.pago_anual, p.proveedor.buro,

                p.get_acceso_sistema_display(), p.acceso_sistema,
                p.get_acceso_equipos_display(), p.acceso_equipos,
                p.get_acceso_info_display(), p.acceso_info,
                p.get_acceso_red_display(), p.acceso_red,
                p.get_tiene_sucursal_display(), p.tiene_sucursal,
                p.get_usa_intermediarios_display(), p.usa_intermediarios,
                p.get_en_lista_display(), p.en_lista,
                p.get_materialmente_importante_display(), p.materialmente_importante,
                p.get_es_cliente_display(), p.es_cliente,
                p.get_tiene_alerta_display(), p.tiene_alerta,
                p.get_evaluacion_proveedor_display(), p.evaluacion_proveedor,
                p.get_no_contingencia_display(), p.no_contingencia,
                p.get_tiene_experiencia_display(), p.tiene_experiencia,
                p.get_estados_financieros_display(), p.estados_financieros,
                p.get_tiene_quejas_display(), p.tiene_quejas,
                p.actividad_economica.actividad, p.actividad_economica.clasificacion,
                p.nacionalidad.nacionalidad, p.nacionalidad.peso,
                p.jurisdiccion.jurisdiccion, p.jurisdiccion.peso,
                p.riesgo_tipo_servicio,
                p.riesgo_proveedor,
                p.get_nivel_riesgo_display(),
                p.calculo_riesgo,
                p.user.username
            ]
            data.append(row)
        return data

    @staticmethod
    def write_data(sheet, data, start_row=0, start_col=0):
        for row, datarow in enumerate(data, start_col):
            for column, value in enumerate(datarow):
                sheet.write(start_row + row, start_col + column, value)

    def reporte(self, request, queryset):
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet("Reporte de Evaluacion de riesgo")
        self.write_header(sheet)
        data = self.datos_evaluacion(queryset)
        self.write_data(sheet, data, 2, 0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Reporte de Evaluacion.xls'
        book.save(response)
        return response

    reporte.short_description = "Generar reporte de evaluaciones de riesgo"

    actions = [reporte, ]
