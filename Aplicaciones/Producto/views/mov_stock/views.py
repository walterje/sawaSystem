from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView

from Aplicaciones.Producto.forms import *
from Aplicaciones.Producto.models import *

#Crear baja Stock
class MovStockCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model=MovimientoStock
    form_class = MovStockForm
    template_name='mov_stock/create.html'
    permission_required = 'add_movimiento_stock'
    success_url = reverse_lazy('Compra:cta_x_pagar_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                #prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term']).exclude(es_servicio=True)[0:5]
                #prods = Producto.objects.exclude(tipo_producto = '13' )[0:10]
                prods = Producto.objects.exclude(cant_stock=0)[0:10]
                #prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre_producto
                    data.append(item)
            elif action=='add':
                with transaction.atomic():# si ocurre error en el detalle y no me guarde
                    mov_stock = json.loads(request.POST['mov_stock'])
                    
                    movimiento_stock= MovimientoStock()
                    movimiento_stock.fecha_mov= mov_stock['fecha_mov']
                    movimiento_stock.descripcion=mov_stock['descripcion']
                    
                    #
                    for i in mov_stock['productos']:
                        #det = OrdenCompraDet()
                        movimiento_stock.producto_id = i['id']
                        print(movimiento_stock.producto_id)
                        movimiento_stock.cant_mov = int(i['cantidad'])
                        movimiento_stock.producto.cant_stock -= int(i['cantidad'])
                        movimiento_stock.save()
                        movimiento_stock.producto.save()
                    movimiento_stock.save()

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Creación de Baja Stock'
        context['entity'] = 'Movimiento Stock'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

#Ajuste de stock
class AjusteStockCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model=MovimientoStock
    form_class = MovStockForm
    template_name='ajuste/create.html'
    permission_required = 'add_movimiento_stock'
    success_url = reverse_lazy('Producto:producto_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                #prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term']).exclude(es_servicio=True)[0:5]
                #prods = Producto.objects.exclude(tipo_producto = '13' )[0:10]
                #priducto=1 y Servicio=2
                prods = Producto.objects.exclude(tipo_producto = '2')[0:10]
                #prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre_producto
                    data.append(item)
            elif action=='add':
                with transaction.atomic():# si ocurre error en el detalle y no me guarde
                    mov_stock = json.loads(request.POST['mov_stock_ajuste'])
                    
                    movimiento_stock= MovimientoStock()
                    movimiento_stock.fecha_mov= mov_stock['fecha_mov']
                    movimiento_stock.descripcion=mov_stock['descripcion']
                    
                    #
                    for i in mov_stock['productos']:
                        #det = OrdenCompraDet()
                        movimiento_stock.producto_id = i['id']
                        print(movimiento_stock.producto_id)
                        movimiento_stock.cant_mov = int(i['cantidad'])
                        movimiento_stock.producto.cant_stock += int(i['cantidad'])
                        movimiento_stock.save()
                        movimiento_stock.producto.save()
                    movimiento_stock.save()

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Creación de Ajuste Stock'
        context['entity'] = 'Movimiento Stock'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

