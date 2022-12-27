from django.urls import path
from Aplicaciones.Producto.views.tipoProducto.views import *
from Aplicaciones.Producto.views.producto.views import *
from Aplicaciones.Producto.views.mov_stock.views import *
from Aplicaciones.Producto.views.disponibilidad.views import *
app_name = 'Producto'
urlpatterns = [
    # tipo producto
    path('tipo_producto/list/', TipoProductoListView.as_view(), name='tipo_producto_list'),
    path('tipo_producto/create/', TipoProductoCreateView.as_view(), name='tipo_producto_create'),
    path('tipo_producto/edit/<int:pk>/', TipoProductoUpdateView.as_view(), name='tipo_producto_edit'),
    path('tipo_producto/delete/<int:pk>/', TipoProductoDeleteView.as_view(), name='tipo_producto_delete'),
    #Producto
    path('producto/list/', ProductoListView.as_view(), name='producto_list'),
    path('producto/create/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/edit/<int:pk>/', ProductoUpdateView.as_view(), name='producto_edit'),
    path('producto/delete/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
    #mov stock
    path('mov_stock/create/', MovStockCreateView.as_view(), name='mov_stock_create'),
    #ajuste
    path('ajuste/create/', AjusteStockCreateView.as_view(), name='ajuste_stock_create'),
    #disponibilidad
    #path('disponibilidad/producto/', ProductoDisponibleView.as_view(), name='mov_stock_create'),


]