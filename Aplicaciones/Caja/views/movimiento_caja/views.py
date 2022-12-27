from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from Aplicaciones.Caja.forms import *
from Aplicaciones.Caja.models import *

# Create your views here.
#Listar
class MovimientoCajaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model=MovimientoCaja
    template_name='movimiento_caja/list.html'
    permission_required = 'view_movimientocaja'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data =[]
                posicion = 1#para listar en orden los numeros del  id
                estado0='Entrada'
                estado1='Salida'
                for i in MovimientoCaja.objects.all():
                    item = i.toJSON()
                    if item['tipo_movimiento']=='1':
                        print('True')
                        item['tipo_movimiento']=estado1
                    elif item['tipo_movimiento']=='0':
                        item['tipo_movimiento']=estado0
                    item['posicion'] = posicion
                    data.append(item)
                    posicion += 1
                
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Movimiento Caja'
        context['create_url']=reverse_lazy('Caja:caja')
        context['list_url'] = reverse_lazy('Caja:movimiento_caja_list')
        context['entity']='MovimientoMoneda'
        return context


#Crear ingresos Varios
class MovimientoIngresoVariosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model=MovimientoCaja
    form_class = MovimientosVariosForm

    template_name='movimiento_caja/ingresos_varios.html'
    success_url = reverse_lazy('Caja:movimiento_caja_list')
    permission_required = 'add_movimiento_caja'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_caja':
                data = []
                caja = Caja.objects.exclude(estado = '1' )[0:10]
                for i in caja:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():# si ocurre error en el detalle y no me guarde
                    ing_varios = json.loads(request.POST['mov_caja'])
                    print(ing_varios)
                    print('mov')
                    mov_caja= MovimientoCaja()
                    mov_caja.fecha_movimiento= ing_varios['fecha_movimiento']
                    print(mov_caja.fecha_movimiento)
                    mov_caja.descripcion=ing_varios['descripcion']
                    print(mov_caja.descripcion)
                    mov_caja.tipo_movimiento='0'
                    print(mov_caja.tipo_movimiento)
                    
                    print('caja')
                    for i in ing_varios['caja']:
                        #det = OrdenCompraDet()
                        mov_caja.caja_id = i['id']
                        print(mov_caja.caja_id)
                        print(i)
                        print(i['monto'])
                        print(i['saldo_actual'])
                        mov_caja.monto_ingreso = int(i['monto'])
                        print(mov_caja.monto_ingreso)
                        mov_caja.caja.saldo_actual+= int(i['monto'])
                        print(mov_caja.caja.saldo_actual)
                        #mov_caja.save()
                        #mov_caja.caja.save()
                    #mov_caja.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Ingresos varios'
        context['entity'] = 'Movimiento Caja'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

#Egresos varios
class MovimientoEgresoVariosCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model=MovimientoCaja
    form_class = MovimientosVariosForm
    template_name='movimiento_caja/egresos_varios.html'
    success_url = reverse_lazy('Caja:movimiento_caja_list')
    permission_required = 'add_movimiento_caja'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_caja':
                data = []
                caja = Caja.objects.exclude(estado = '1' )[0:10]
                for i in caja:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():# si ocurre error en el detalle y no me guarde
                    eg_varios = json.loads(request.POST['mov_caja'])
                    print(eg_varios)
                    print('mov')
                    mov_caja= MovimientoCaja()
                    mov_caja.fecha_movimiento= eg_varios['fecha_movimiento']
                    print(mov_caja.fecha_movimiento)
                    mov_caja.descripcion=eg_varios['descripcion']
                    print(mov_caja.descripcion)
                    mov_caja.tipo_movimiento='1'
                    print(mov_caja.tipo_movimiento)
                    
                    print('caja')
                    for i in eg_varios['caja']:
                        mov_caja.caja_id = i['id']
                        print(mov_caja.caja_id)
                        print(i)
                        print(i['monto'])
                        print(i['saldo_actual'])
                        mov_caja.monto_egreso = int(i['monto'])
                        print(mov_caja.monto_egreso)
                        mov_caja.caja.saldo_actual-= int(i['monto'])
                        print(mov_caja.caja.saldo_actual)
                        #mov_caja.save()
                        #mov_caja.caja.save()
                    #mov_caja.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Egresos varios'
        context['entity'] = 'Movimiento Caja'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
