from django.contrib import admin
from Aplicaciones.Caja.models import *

# Register your models here.
class MonedaAdmin(admin.ModelAdmin):
    list_display = ( "descripcion"),
    search_fields = ("descripcion", "id")
admin.site.register(Moneda,MonedaAdmin)

class CajaAdmin(admin.ModelAdmin):
    list_display = ( "nombre","estado","monto_inicio","monto_cierre","total_ingreso","total_egreso","moneda","saldo_actual")
    search_fields = ("nombre", "id")
admin.site.register(Caja,CajaAdmin)


class MovCajaAdmin(admin.ModelAdmin):
    list_display = ( "caja","fecha_movimiento","descripcion","tipo_movimiento","monto_ingreso","monto_egreso",)
    search_fields = ("descripcion", "id")
admin.site.register(MovimientoCaja,MovCajaAdmin)

class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ( "descripcion"),
    search_fields = ("descripcion", "id")
admin.site.register(FormaPago,FormaPagoAdmin)
