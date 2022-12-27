from django.urls import path
from Aplicaciones.Venta.views.cliente.views import *
from Aplicaciones.Venta.views.ordenVenta.views import *
from Aplicaciones.Venta.views.venta.views import *
from Aplicaciones.Venta.views.cobro.views import *
from Aplicaciones.Venta.views.company.views import *
app_name = 'Venta'

urlpatterns = [
    #cliente
    path('cliente/list/',ClienteListView.as_view(),name='cliente_list'),
    path('cliente/create/',ClienteCreateView.as_view(),name='cliente_create'),
    path('cliente/edit/<int:pk>/',ClienteUpdateView.as_view(),name='cliente_edit'),
    path('cliente/delete/<int:pk>/',ClienteDeleteView.as_view(),name='cliente_delete'),
    #ordenVenta
    path('ordenVenta/create/',OrdenVentaCreateView.as_view(),name='orden_venta_create'),
    path('ordenVenta/list/', OrdenVentaListView.as_view(), name='orden_venta_list'),
    path('ordenVenta/edit/<int:pk>/',OrdenVentaUpdateView.as_view(),name='orden_venta_edit'),
    #pdf con weasyprint
    path('ordenVenta/pdf/<int:pk>/', OrdenVentaPDFView.as_view(), name='ordenVenta_pdf'),
    #Venta
    path('venta/create',VentaCreateView.as_view(),name='venta_create'),
    path('venta/list/', VentaListView.as_view(), name='venta_list'),
    path('venta/pdf/<int:pk>/', VentaPDFView.as_view(), name='venta_pdf'),
    #Cta_x_Cobrar
    path('cta_x_cobrar/list/',Cta_X_Cobrar_ListView.as_view(),name='cta_x_cobrar_list'),
    #Cobro
    path('cobro/create/',CobroCreateView.as_view(),name='cobro_create'),
    #company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),
    #pdf
    path('cobro/pdf/<int:pk>/', CobroPdfView.as_view(), name='cobro_pdf'),
    
]