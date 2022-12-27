from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from Aplicaciones.Venta.models import CuentaXcobrar
from Aplicaciones.Venta.models import *
from Aplicaciones.Venta.forms import *
from django.urls import reverse_lazy
from django.contrib import messages
import json
import os
from nlt import numlet as nl
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.template.loader import get_template
from weasyprint import HTML, CSS
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View
# Create your views here.
#Cta_X_Cobrar List
class Cta_X_Cobrar_ListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = CuentaXcobrar
    template_name='cobro/cuenta_x_cobrar_list.html'
    permission_required = 'view_cobro'
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
                estado0='Cobrado'
                estado1='Deuda'
                tv0='Contado'
                tv1='Crédito'
               
                for i in CuentaXcobrar.objects.all():
                    item = i.toJSON()
                    if item['estado']== '1':
                        item['estado']=estado1
                    elif item['estado']== '0':
                        item['estado']=estado0
                    if (item['venta']['tipo_venta'])== '0':
                        (item['venta']['tipo_venta'])= tv0
                    elif (item['venta']['tipo_venta'])== '1':
                        (item['venta']['tipo_venta'])= tv1
                    item['posicion'] = posicion
                    data.append(item)
                    posicion += 1
            elif action=='search_cob_ven':
                data=[]
                for i in Cobro.objects.filter(cuenta_x_cobrar_id=request.POST['id']):
                    item=i.toJSON()
                    cobrador = item['user']
                    print(cobrador['first_name'])
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Listado de Cuenta Por Cobrar'
        context['create_url']=reverse_lazy('Venta:cobro_create')
        context['list_url']=reverse_lazy('Venta:cta_x_cobrar_list')
        context['entity']='Cuenta por Cobrar'
        return context
    
#Cobro

class CobroCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model=Cobro
    form_class = CobroForm
    template_name='cobro/cobro.html'
    permission_required = 'add_cobro'
    success_url = reverse_lazy('Venta:cta_x_cobrar_list')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_cta_x_cobrar':
                data = []
                cta_cob = CuentaXcobrar.objects.filter(id__icontains=request.POST['term']).exclude(estado='0')
                print(cta_cob)
                for i in cta_cob:
                    item = i.toJSON()
                    item['value'] = i.id
                    data.append(item)
            elif action=='add':
                with transaction.atomic():# si ocurre error en el detalle y no me guarde
                    cob_cta= json.loads(request.POST['cob_cta'])
                    print('Cobro cuenta')
                    cobro =Cobro()
                    cobro.cuenta_x_cobrar_id=cob_cta['cta_x_cobrar']
                    print(cobro.cuenta_x_cobrar_id)
                    cobro.fecha_cobro= cob_cta['fecha_cobro']
                    print(cobro.fecha_cobro)
                    cobro.caja_id = cob_cta['caja']
                    print(cobro.caja_id)
                    cobro.monto_cobrado= int(cob_cta['montocob'])
                    print(cobro.monto_cobrado)
                    cobro.efectivo = int(cob_cta['efectivo'])
                    print(cobro.efectivo)
                    cobro.vuelto = int(cob_cta['vuelto'])
                    print(cobro.vuelto)
                    usuario=User.objects.get(pk=self.request.user.id)
                    cobro.user_id = usuario.id
                    cobro.save()

                    print('Cuenta_por_pagar')
                    

                    cta_x_cob = CuentaXcobrar.objects.filter(id=cob_cta['cta_x_cobrar'])
                    for i in cta_x_cob:
                        i.saldo-=int(cob_cta['montocob'])
                        i.save()
                        if(i.saldo==0):
                            i.estado='0'
                            i.save()

                    print('movimientos')
                    mov_caja=MovimientoCaja()
                    mov_caja.caja_id=cobro.caja.id
                    print(mov_caja.caja_id)
                    mov_caja.fecha_movimiento=cobro.fecha_cobro
                    print(mov_caja.fecha_movimiento)
                    mov_caja.monto_movimiento=cobro.monto_cobrado
                    print(mov_caja.monto_movimiento)
                    mov_caja.descripcion='Venta'
                    print(mov_caja.descripcion)
                    mov_caja.tipo_movimiento='0'
                    print(mov_caja.tipo_movimiento)
                    mov_caja.monto_egreso=0
                    print(mov_caja.monto_ingreso)
                    mov_caja.monto_ingreso=cobro.monto_cobrado
                    print(mov_caja.monto_ingreso)
                    mov_caja.save()

                  
                    caja= Caja.objects.filter(id=cob_cta['caja'])
                    print('caja')
                    for i in caja:
                        print(i)
                        i.total_ingreso += (int(mov_caja.monto_ingreso))
                        print(i.total_ingreso)
                        i.saldo_actual += (int(cob_cta['montocob']))
                        print(i.saldo_actual)
                        i.save()
      
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Creación de Cobro'
        context['entity'] = 'Cobro'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


#Recibo
class CobroPdfView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('cobro/recibo_pdf.html')
            print(self.kwargs['pk'])
            context = {
                'cobro': Cobro.objects.get(pk=self.kwargs['pk']),
                'monto_cobrado': nl.Numero(Cobro.objects.get(pk=self.kwargs['pk']).monto_cobrado).a_letras,
                'company': (Company.objects.get(pk=self.kwargs['pk']))
            }
            print(context)
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('Venta:cta_x_cobrar_list'))