from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.conf import settings
from weasyprint import HTML, CSS
import os
from django.contrib import messages
from Aplicaciones.Venta.forms import VentaForm
from Aplicaciones.Venta.models import *
from Aplicaciones.Producto.models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.db import transaction
from nlt import numlet as nl
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from datetime import datetime, timedelta
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View

#Listar
class VentaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model=Venta
    template_name='venta/list.html'
    permission_required = 'view_venta'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                posicion = 1
                estado0='Contado'
                estado1='Credito'
                for i in Venta.objects.all():
                    item=i.toJSON()
                    item['posicion'] = posicion
                    data.append(item)
                    posicion += 1
                    if item['tipo_venta']== '0':
                        item['tipo_venta']=estado0
                    elif item['tipo_venta']== '1':
                        item['tipo_venta']=estado1
                    
            elif action=='search_details_prod':
                data=[]
                for i in VentasDet.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Listado de Ventas'
        context['create_url']=reverse_lazy('Venta:venta_create')
        context['list_url']=reverse_lazy('Venta:venta_list')
        context['entity']='Venta'
        return context

#Crear
class VentaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,SuccessMessageMixin ,CreateView):
    model= Venta
    form_class = VentaForm
    template_name='venta/create.html'
    success_url = reverse_lazy('Venta:venta_list')
    permission_required = 'add_venta'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_orden_v':
                data=[]
                ordenV= OrdenVenta.objects.filter(estado='0')
                for i in ordenV:
                    item = i.toJSON()
                    item['value'] = i.id
                    data.append(item)
                    #item['value'] = i.cliente.get_nombre_completo()
            elif action == 'add':
                with transaction.atomic():#si ocurre error no guarda nada
                    vent = json.loads(request.POST['vent'])
                    print('Venta')
                    venta = Venta()
                    venta.fecha_venta = vent['fecha_venta']
                    print(venta.fecha_venta)
                    venta.tipo_venta = vent['tipo_venta']
                    print(venta.tipo_venta)
                    venta.fecha_plazo = vent['fecha_plazo']
                    print(venta.fecha_plazo)
                    venta.subtotal = int(vent['subtotal'])
                    print(venta.subtotal)
                    venta.iva_0 = int(vent['iva_0'])
                    print(venta.iva_0)
                    venta.iva_5 = int(vent['iva_5'])
                    print(venta.iva_5)
                    venta.iva_10 = int(vent['iva_10'])
                    print(venta.iva_10)
                    venta.total = int(vent['total'])
                    print(venta.total)
                    venta.ordenVenta_id=vent['ordenVenta']
                    print(venta.ordenVenta_id)
                    venta.cliente_id = vent['cliente']
                    print(venta.cliente_id)
                    usuario=User.objects.get(pk=self.request.user.id)
                    venta.user_id = usuario.id
                    venta.save()
                    print('Ov')
                    venta.ordenVenta.estado='1'
                    print(venta.ordenVenta.estado)
                    venta.ordenVenta.save()
                    print('Cta x cobrar')
                    ctaxpag=CuentaXcobrar()
                    ctaxpag.venta_id = venta.id
                    print(ctaxpag.venta_id )
                    ctaxpag.estado='1'
                    print(ctaxpag.estado)
                    ctaxpag.monto_x_cobrar= int(venta.total)
                    print(ctaxpag.monto_x_cobrar )
                    ctaxpag.saldo= int(venta.total)
                    print(ctaxpag.saldo)
                    ctaxpag.save()
                    print('detalle')
                    for i in vent['productos']:
                        a=i['producto']
                        b=a['tipo_producto']
                        print('productos-----------')
                        print(a)
                        print(b['id']==1)
                        det = VentasDet()
                        det.venta_id = venta.id
                        det.producto_id = a['id']
                        det.precio_venta = int(i['precio_venta'])
                        det.cantidad = int(i['cantidad'])
                        det.subtotal = int(i['subtotal'])
                        det.save()
                        print('movimientos')
                        mov_stock= MovimientoStock()
                        mov_stock.producto_id=a['id']
                        if(mov_stock.producto.tipo_producto.id == 1):
                           
                            print(mov_stock.producto_id)
                            mov_stock.cant_mov=int(i['cantidad'])
                            print(mov_stock.cant_mov)
                            print('tipo_producto')
                            print(mov_stock.producto.tipo_producto.id)
                            mov_stock.fecha_mov=vent['fecha_venta']
                            print(mov_stock.fecha_mov)
                            mov_stock.descripcion='Venta'
                            print(mov_stock.descripcion)
                            mov_stock.tipo_movimiento='1'
                            print(mov_stock.tipo_movimiento)
                            print(mov_stock)
                            mov_stock.save()
                        else:
                            print('Es servicio')
                        print('actualizacion stock')
                        
                        if(b['id']==1):
                            det.producto.cant_stock -= det.cantidad
                            det.producto.save()
                        elif(b['id']==13):
                            det.producto.cant_stock = 0
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = 'Producto sin stock'
        return JsonResponse(data,safe=False)
   
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Registrar Venta'
        context['entity'] = 'Venta'
        context['list_url']= self.success_url
        context['action'] = 'add'
        return context


##Generar pdf con weasyprint de la  Venta
class VentaPDFView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('venta/factura_venta.html')
            context = {
                'venta': Venta.objects.get(pk=self.kwargs['pk']),
                'comp': {'factura':'001-001-00000'},
                'icon': f'{settings.MEDIA_URL}lg.jpg',
                'total': nl.Numero(Venta.objects.get(pk=self.kwargs['pk']).total).a_letras,  
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('Venta:venta_list'))

#