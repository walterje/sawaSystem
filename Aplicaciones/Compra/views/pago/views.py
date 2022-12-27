from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from Aplicaciones.Compra.models import *
from Aplicaciones.Compra.forms import *
from django.urls import reverse_lazy
from django.contrib import messages
import json
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.http import JsonResponse
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
# Create your views here.
#Cta_X_Pagar List
class Cta_X_Pagar_ListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = CuentaXpagar
    template_name='pago/cta_x_pagar_list.html'
    permission_required = 'view_pago'
    context_object_name="object_list"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data =[]
                posicion = 1
                estado0='Pagado'
                estado1='Deuda'
                tc0='Contado'
                tc1='Crédito'
                for i in CuentaXpagar.objects.all():
                    item = i.toJSON()
                    if item['estado']== '1':
                        item['estado']=estado1
                    elif item['estado']== '0':
                        item['estado']=estado0
                    if (item['compra']['tipo_compra'])== '0':
                        (item['compra']['tipo_compra'])= tc0
                    elif (item['compra']['tipo_compra'])== '1':
                        (item['compra']['tipo_compra'])= tc1
                    item['posicion'] = posicion
                    data.append(item)
                    posicion += 1
            elif action=='search_pag_comp':
                data=[]
                for i in Pago.objects.filter(cuenta_x_pagar_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Listado de Cuenta Por Pagar'
        context['create_url']=reverse_lazy('Compra:pago_create')
        context['list_url']=reverse_lazy('Compra:proveedor_list')
        context['entity']='Cuenta por Pagar'
        return context
    
#Crear pago
class PagoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model=Pago
    form_class = PagoForm
    #template_name='pago/create_pago.html'
    template_name='pago/pago.html'
    permission_required = 'add_pago'
    success_url = reverse_lazy('Compra:cta_x_pagar_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_cta_x_pagar':
                data = []
                cta_pag = CuentaXpagar.objects.filter(id__icontains=request.POST['term']).exclude(estado='0')
                for i in cta_pag:
                    item = i.toJSON()
                    item['value'] = i.id
                    data.append(item)
            elif action == 'search_caja':
                data = []
                term = request.POST['term']
                #caj = Caja.objects.filter(id__icontains=request.POST['term']).exclude(estado='0')
                caj = Caja.objects.filter(
                    Q(nombre__icontains=term) | Q(id__icontains=term))[0:10]
                
                for i in caj:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)

            elif action=='add':
               
                with transaction.atomic():
                    pag_cta= json.loads(request.POST['pag_cta'])
                    print('Pago cuenta')
                    caja= Caja.objects.filter(id=pag_cta['caja'])
                    for i in caja:
                        if (i.saldo_actual < pag_cta['montopag']):
                            data['error'] = 'La caja tiene saldo insuficiente para pagar'
                         
                        else:
                            pago =Pago()
                            print('---pago---')
                            pago.cuenta_x_pagar_id=pag_cta['cta_x_pagar']
                            print(pago.cuenta_x_pagar_id)
                            
                            pago.fecha_pago= pag_cta['fecha_pago']
                            print(pago.fecha_pago)
                            pago.caja_id = pag_cta['caja']
                            print(pago.caja_id)
                            pago.monto_pagado= int(pag_cta['montopag'])
                            print(pago.monto_pagado)
                            pago.efectivo = int(pag_cta['efectivo'])
                            print(pago.efectivo)
                            pago.vuelto = int(pag_cta['vuelto'])
                            print(pago.vuelto)
                            usuario=User.objects.get(pk=self.request.user.id)
                            pago.user_id = usuario.id
                            pago.save()
                            print('Cuenta_por_pagar')
                            cta_x_pag = CuentaXpagar.objects.filter(id=pag_cta['cta_x_pagar'])
                            for x in cta_x_pag:
                                print('tipo_compra')
                                print(x.compra.tipo_compra )
                                x.saldo -= int(pag_cta['montopag'])
                                print('x')
                                print(x.saldo)
                                x.save()
                                if(x.saldo==0):
                                    x.estado='0'
                                    x.save()
                            print('movimientos')
                            mov_caja=MovimientoCaja()
                            mov_caja.caja_id=pago.caja.id
                            print(mov_caja.caja_id)
                            mov_caja.fecha_movimiento=pago.fecha_pago
                            print(mov_caja.fecha_movimiento)
                            mov_caja.descripcion='Compra'
                            print(mov_caja.descripcion)
                            mov_caja.tipo_movimiento='1'
                            print(mov_caja.tipo_movimiento)
                            mov_caja.monto_ingreso=0
                            print(mov_caja.monto_ingreso)
                            mov_caja.monto_egreso=pago.monto_pagado
                            print(mov_caja.monto_egreso)
                            mov_caja.save()
                            for a in caja:
                                a.total_egreso+=(int(mov_caja.monto_egreso))
                                a.saldo_actual-=(int(pag_cta['montopag']))
                                print(i.total_egreso)
                                a.save()
                        
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Creación de Pago'
        context['entity'] = 'Pago'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        
        return context

