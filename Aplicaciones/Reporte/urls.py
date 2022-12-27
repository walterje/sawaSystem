from django.urls import path
from Aplicaciones.Reporte.views.ordenC.views import *
from Aplicaciones.Reporte.views.compra.views import *
from Aplicaciones.Reporte.views.venta.views import *
from Aplicaciones.Reporte.views.caja.views import *
from Aplicaciones.Reporte.views.mov_caja.views import *
from Aplicaciones.Reporte.views.inventario.views import *
app_name = 'Reporte'
urlpatterns = [
    # reporte orden
    #path('ordenC/reporte/', ReporteOrdenCView.as_view(), name='ordenC_reporte'),
    path('compra/reporte/', ReporteCompraView.as_view(), name='compra_reporte'),
    path('venta/reporte/', ReporteVentaView.as_view(), name='venta_reporte'),
    #path('caja/reporte/', ReporteCajaView.as_view(), name='caja_reporte'),
    path('movimiento_caja/reporte/', ReporteMovCajaView.as_view(), name='movimiento_caja_reporte'),
    path('inventario/reporte/', ReporteInventarioView.as_view(), name='inventario_reporte'),
    
]