from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView
from datetime import datetime
from django.db.models import FloatField
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Aplicaciones.Compra.models import *
from Aplicaciones.Producto.models import Producto
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'home/index.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

        
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_compra_year_month':
                data ={
                    'name': 'Compra',
                    'showInLegend': False,
                    'colorByPoint' : True,
                    'data': self.get_compra_year_month()
                }
            elif action == 'get_compra_productos_year_month':
                data = {
                    'name': 'Cantidad',
                    'colorByPoint': True,
                    'data': self.get_compra_productos_year_month(),
                }
            elif action == 'get_venta_year_month':
                data ={
                    'name': 'Venta',
                    'showInLegend': False,
                    'colorByPoint' : True,
                    'data': self.get_venta_year_month()
                }
                
            elif action == 'get_producto':
                data = {
                    'name': 'Producto',
                    'colorByPoint': True,
                    'data': self.get_producto(),
                }

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


#compra por año
    def get_compra_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Compra.objects.filter(fecha_compra__year=year, fecha_compra__month=m).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                #total_compra = '{:,}'.format(int((total))).replace(',','.')
                data.append((total))
                
        except:
            pass
        return data
#venta por año
    def get_venta_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Venta.objects.filter(fecha_venta__year=year, fecha_venta__month=m).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                #data.append('{:,}'.format(int((total))).replace(',','.'))
                data.append(int(total))
        except:
            pass
        return data
    #producto por mes
    def get_compra_productos_year_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
      
        try:
            for p in Producto.objects.all():
                # = ComprasDet.objects.filter(compra__fecha_compra__year=year, compra__fecha_compra__month=month, producto_id=p.id).aggregate(
                 #   r=Coalesce(Sum('subtotal'), 0)).get('r')
                total= p.cant_stock
                if p.cant_stock > 0:
                    data.append({
                        'name': p.nombre_producto,
                        'y': int(total)
                    })
        except:
            pass
        return data
#datos varios 
    def get_datos (self):
        data = []
        try:
            cliente=Cliente.objects.all()
            proveedor= Proveedor.objects.all()
            producto= Producto.objects.filter(tipo_producto__id=1 )
            servicio=Producto.objects.exclude(tipo_producto__id=1 )
            data.append({
                'cli': cliente.count(),
                'prov': proveedor.count(),
                'prod': producto.count(),
                'serv': servicio.count()
                 })
        except:
            pass
        return data

# 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['grafico_compra_year_month'] = self.get_compra_year_month()
        context['grafico_venta_year_month'] = self.get_venta_year_month()
        context['get_datos'] = self.get_datos()
        return context

def page_not_found404(request, exception):
    return render(request, 'home/404.html')