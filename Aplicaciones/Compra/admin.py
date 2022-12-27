from django.contrib import admin
from Aplicaciones.Compra.models import *

# Register your models here.
#Proveedor
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ( "nombre"),
    search_fields = ("nombre", "id")
admin.site.register(Proveedor,ProveedorAdmin)
#pago
class PagoAdmin(admin.ModelAdmin):
    list_display = ( "monto_pagado"),
    search_fields = ("monto_pagado", "id")
admin.site.register(Pago,PagoAdmin)

#Orden
class OrdenCompraDetalle(admin.TabularInline):
    model = OrdenCompraDet
    raw_id_fields = ['producto','nro_orden_c']

class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ( "id","fecha_orden","proveedor","estado")
    list_filter = ['id']
    search_fields = ("nro_orden_c","Proveedor")
    inlines = [OrdenCompraDetalle]

admin.site.register(OrdenCompra, OrdenCompraAdmin)
#Recepcion
"""
class RecepcionDetalle(admin.TabularInline):
    model = RecepcionProductoDet
    raw_id_fields = ['producto','recepcion_producto']

class RecepcionAdmin(admin.ModelAdmin):
    list_display = ( "id","proveedor")
    list_filter = ['id']
    search_fields = ("recepcion_producto","id")
    inlines = [RecepcionDetalle]

admin.site.register(RecepcionProducto,RecepcionAdmin)
"""
#Compra
class CompraDetalle(admin.TabularInline):
    model = ComprasDet
    raw_id_fields = ['producto','compra']

class CompraAdmin(admin.ModelAdmin):
    list_display = ( "id","fecha_compra","proveedor","tipo_compra")
    list_filter = ['id']
    search_fields = ("compra","id")
    inlines = [CompraDetalle]

admin.site.register(Compra,CompraAdmin)
#DeudaXpagar
class CtaXpagarAdmin(admin.ModelAdmin):
    list_display = ( "compra"),
    search_fields = ("compra", "id","estado","monto_x_pagar","saldo")
admin.site.register(CuentaXpagar,CtaXpagarAdmin)