from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .utils import *
from django.contrib.admin import site
import adminactions.actions as actions
actions.add_to_site(site)



class expediente_admin(admin.TabularInline):
    model = Expediente
    extra = 0
    classes = ('grp-collapse grp-open', )


class proveedor_admin(ImportExportModelAdmin):

    def get_queryset(self, request):
        queryset = super(proveedor_admin, self).get_queryset(request)
        usuario = request.user
        if usuario.is_superuser:
            return queryset
        else:
            return queryset.filter(usuario=usuario)

    change_form_template = "compras/proveedor.html"
    list_display = ('codigo', 'nombre', 'identificacion', 'r_legal', 'servicio', 'email', 'telefono', 'puntaje')
    search_fields = ('codigo', 'codigo_cliente', 'nombre', 'identificacion', 'r_legal', 'servicio', 'email', 'telefono')
    list_filter = ('usuario', 'servicio', 'relacionado', 'contrato', 'activo', 'puntaje')

    fieldsets = (
        ('Datos Generales', {
                'classes': ('grp-collapse grp-open', ),
                'fields': (
                            ('codigo', 'codigo_cliente'), ('nombre', 'identificacion'),
                            ('servicio', 'actividad_economica'), ('forma_pago', 'contacto'),
                            'email', ('telefono', 'r_legal'),'direccion',
                            ('usuario', 'buro', 'pago_anual')
                        )
        }),
        ('Informacion Adicional', {
                'classes': ('grp-collapse grp-open', ),
                'fields': (('cuenta_cordobas', 'beneficiario_cordobas'),
                          ('cuenta_dolares', 'beneficiario_dolares'),
                          ('relacionado', 'contrato', 'activo'),
                          ),}),
        ('Parametros de la Evaluacion', {
                'classes': ('grp-collapse grp-open evaluacion', ),
                'fields': ('importacia', 'complejidad', 'reemplazo', 'credito',
                           'anual', 'incumplimiento', 'actividad', 'recurrente',
                           'transversal', 'incidencia', 'multicontrato', 'marco', 'puntaje')
        }),
      )

    inlines = [expediente_admin,]

    def reporte_evaluacion(self, request, queryset):
        primera_linea = ["Codigo", "Nombre", "Actividad Economica",
                        "Identificacion", "Direccion", "Contacto", "Telefono", "Monto Anual Facturado",
                        "Resultado de Consulta de Credito",
                        "Importante para el funcionamiento estrategico del Banco y para atencion de clientes?",
                        "Complejidad de la contratacion",
                        "Habilidad para reemplazar a la empresa por otra",
                        "Reputacion financiera y solvencia",
                        "Monto total anual pagado al proveedor",
                        "La interrupcion del servicio genera incumplimiento regulatorio/legales al Banco",
                        "Importancia de la actividad a ser contratada en relacion al giro principal de negocios de la institucion",
                        "Relacion del Proveedor de servicios con la institucion financiera",
                        "Interrelacion de la operacion contratada con el resto de operacions de la institucion financiera",
                        "Fallas del proveedor pone en riesgo las ganancias, solvencia, liquidez, capital, reputacion, fondeo o sistemas de control interno",
                        "Existen mas de dos contratos vigentes con este mismo proveedor",
                        "Marco regulatorio del proveedor"
                        ]
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet("Reporte de Evaluacion")
        default_style = xlwt.Style.default_style
        font_size_style = xlwt.easyxf('font: name Calibri, bold on, height 280;')
        font_underline_style = xlwt.easyxf('font: underline on;')
        fill_grey_style = xlwt.easyxf('pattern: back_color gray25;')
        fill_yellow_style = xlwt.easyxf('pattern: back_color yellow;')
        c1 = 9
        c2 = 10
        for r, d in enumerate(primera_linea[:9]):
            sheet.write_merge(0, 1, r, r, d, style=fill_grey_style)
        for r, d in enumerate(primera_linea[9:]):
            sheet.write_merge(0, 0, c1+(r*2), c2+(r*2), d, style=fill_grey_style)
            sheet.write(1, c1+(r*2), "Respuesta", style=fill_grey_style)
            sheet.write(1, c2+(r*2), "Valor", style=fill_grey_style)
        data = datos_evaluacion(queryset)
        col = 0
        for r, d in enumerate(data):
            col = len(d)
            for c in range(0, col):
                sheet.write(r+2, c, d[c], style=default_style)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Reporte de Evaluacion.xls'
        book.save(response)
        return response

    actions = [reporte_evaluacion,]


class evaluacion_admin(ImportExportModelAdmin):
    list_display = ('proveedor', 'importacia', 'complejidad', 'reemplazo', 'credito', 'anual', 'incumplimiento', 'actividad', 'recurrente')


admin.site.register(Proveedor, proveedor_admin)
admin.site.register(Evaluacion, evaluacion_admin)