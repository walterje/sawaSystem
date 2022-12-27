from django.urls import path
from Aplicaciones.Caja.views.caja.views import *
from Aplicaciones.Caja.views.moneda.views import *
from Aplicaciones.Caja.views.forma_pag_cob.views import *
from Aplicaciones.Caja.views.movimiento_caja.views import *

app_name = 'Caja'
urlpatterns = [
    #caja modal
    path('caja/', CajaView.as_view(), name='caja'),
    #moneda
    path('moneda/create/', MonedaCreateView.as_view(), name='moneda_create'),
    path('moneda/list/', MonedaListView.as_view(), name='moneda_list'),
    path('moneda/edit/<int:pk>/', MonedaUpdateView.as_view(), name='moneda_edit'),
    path('moneda/delete/<int:pk>/', MonedaDeleteView.as_view(), name='moneda_delete'),
    #forma pag_cob
    path('forma_pag_cob/create/', FormaPagCobCreateView.as_view(), name='forma_pag_cob_create'),
    path('forma_pag_cob/list/', FormaPagCobListView.as_view(), name='forma_pag_cob_list'),
    path('forma_pag_cob/edit/<int:pk>/', FormaPagCobUpdateView.as_view(), name='forma_pag_cob_edit'),
    path('forma_pag_cob/delete/<int:pk>/', FormaPagCobDeleteView.as_view(), name='forma_pag_cob_delete'),
    
    #mov_caja
    path('movimientoCaja/list/', MovimientoCajaListView.as_view(), name='movimiento_caja_list'),
    path('movimientoCaja/create_egresos_varios/', MovimientoIngresoVariosCreateView.as_view(), name='movimiento_caja_create_egresos_varios'),
    path('movimientoCaja/create_ingresos_varios/', MovimientoIngresoVariosCreateView.as_view(), name='movimiento_caja_create_ingresos_varios'),

]