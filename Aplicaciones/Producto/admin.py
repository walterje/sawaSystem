from django.contrib import admin
from Aplicaciones.Producto.models import *

# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
    list_display = ( "nombre_producto"),
    search_fields = ("nombre_producto", "id")
admin.site.register(Producto,ProductoAdmin)

class MovStockAdmin(admin.ModelAdmin):
    list_display = ( "descripcion"),
    search_fields = ("descripcion","id")
admin.site.register(MovimientoStock,MovStockAdmin)