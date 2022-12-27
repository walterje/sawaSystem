from django.contrib import admin
from Aplicaciones.Venta.models import *
# Register your models here.
#Orden
class OrdenVentaDetalle(admin.TabularInline):
    model = OrdenVentaDet
    raw_id_fields = ['producto','nro_orden_v']

class OrdenVentaAdmin(admin.ModelAdmin):
    list_display = ( "id","fecha_orden_v","cliente","estado")
    list_filter = ['id']
    search_fields = ("nro_orden_v","Proveedor")
    inlines = [OrdenVentaDetalle]

admin.site.register(OrdenVenta, OrdenVentaAdmin)
#Venta
class VentaDetalle(admin.TabularInline):
    model = VentasDet
    raw_id_fields = ['producto','venta']

class VentaAdmin(admin.ModelAdmin):
    list_display = ( "id","fecha_venta","cliente","tipo_venta")
    list_filter = ['id']
    search_fields = ("venta","id")
    inlines = [VentaDetalle]

admin.site.register(Venta,VentaAdmin)
#DeudaXcobrar
class CtaXcobrarAdmin(admin.ModelAdmin):
    list_display = ( "venta"),
    search_fields = ("venta", "id","estado","monto_x_cobrar","saldo")
admin.site.register(CuentaXcobrar,CtaXcobrarAdmin)
#cobro
#pago
class CobroAdmin(admin.ModelAdmin):
    list_display = ( "monto_cobrado"),
    search_fields = ("monto_cobrado", "id")
admin.site.register(Cobro,CobroAdmin)