from django.urls import path
#from Aplicaciones.Compra.views.dashboard.views import DashboardView
from Aplicaciones.Compra.views.proveedor.views import *
from Aplicaciones.Compra.views.orden_compra.views import *
from Aplicaciones.Compra.views.compra.views import *
from Aplicaciones.Compra.views.pago.views import *
app_name = 'Compra'

urlpatterns = [
    #proveedor
    path('proveedor/list/',ProveedorListView.as_view(),name='proveedor_list'),
    path('proveedor/create/',ProveedorCreateView.as_view(),name='proveedor_create'),
    path('proveedor/edit/<int:pk>/',ProveedorUpdateView.as_view(),name='proveedor_edit'),
    path('proveedor/delete/<int:pk>/',ProveedorDeleteView.as_view(),name='proveedor_delete'),
    #OrdenCompra
    path('ordenCompra/create/',OrdenCompraCreateView.as_view(),name='orden_compra_create'),
    path('ordenCompra/list/', OrdenCompraListView.as_view(), name='orden_compra_list'),
    path('ordenCompra/edit/<int:pk>/',OrdenCompraUpdateView.as_view(),name='orden_compra_edit'),
    path('ordenCompra/delete/<int:pk>/', OrdenCompraDeleteView.as_view(), name='orden_compra_delete'),
    #pdf con weasyprint
    path('ordenCompra/pdf/<int:pk>/', OrdenCPdfView.as_view(), name='ordenCompra_pdf'),
    path('compra/pdf/<int:pk>/', CompraPdfView.as_view(), name='compra_pdf'),
    #Compra
    path('create/',CompraCreateView.as_view(),name='compra_create'),
    path('list/',CompraListView.as_view(),name='compra_list'),
    path('edit/<int:pk>/',CompraUpdateView.as_view(),name='compra_edit'),
    #Cta_X_pagar
    path('cta_x_pagar/list/',Cta_X_Pagar_ListView.as_view(),name='cta_x_pagar_list'),
    #Pago
    path('pago/create/',PagoCreateView.as_view(),name='pago_create'),
    #html
    path('compra/<int:pk>/',CompraView.as_view(), name='compra'),


]
