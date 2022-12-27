from django.contrib.auth.mixins import LoginRequiredMixin
import json
from Aplicaciones.Compra.forms import CompraForm
from Aplicaciones.Compra.models import *
from Aplicaciones.Producto.models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.template.loader import get_template
from django.db import transaction
from django.conf import settings
from Aplicaciones.Compra.models import *
import os
from nlt import numlet as nl
#pdf weasyprint
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View

#Listar
class CompraListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model=Compra
    template_name='compra/list.html'
    permission_required = 'view_compra'
    
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
                tipo_compra0='Contado'
                tipo_compra1='Credito'
                for i in Compra.objects.all():
                    item=i.toJSON()
                    item['posicion'] = posicion
                    data.append(item)
                    if item['tipo_compra']== '0':
                        item['tipo_compra']=tipo_compra0
                    elif item['tipo_compra']=='1':
                        item['tipo_compra']=tipo_compra1
                    posicion += 1
            elif action=='search_details_prod':
                data=[]
                for i in ComprasDet.objects.filter(compra_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Listado de Compras'
        context['create_url']=reverse_lazy('Compra:compra_create')
        context['list_url']=reverse_lazy('Compra:compra_list')
        context['entity']='Compra'
        return context
#Crear
class CompraCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,SuccessMessageMixin ,CreateView):
    model= Compra
    form_class = CompraForm
    template_name='compra/create.html'
    success_url = reverse_lazy('Compra:compra_list')
    permission_required = 'add_compra'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_orden_c':
                data=[]
                ordenC= OrdenCompra.objects.filter(estado='0')
                for i in ordenC:
                    item = i.toJSON()
                    item['value'] = i.id
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():#si ocurre error no guarda nada
                    comp = json.loads(request.POST['comp'])
                    
                    compra = Compra()
                    print('Compra')
                    compra.fecha_compra = comp['fecha_compra']
                    print(compra.fecha_compra)
                    compra.nro_factura= comp['nro_factura']
                    print(compra.nro_factura)
                    compra.tipo_compra = comp['tipo_compra']
                    print(compra.tipo_compra)
                    compra.fecha_plazo = comp['fecha_plazo']
                    print(compra.fecha_plazo)
                    compra.subtotal = int(comp['subtotal'])
                    print( compra.subtotal)
                    compra.iva_0 = int(comp['iva_0'])
                    print(compra.iva_0)
                    compra.iva_5 = int(comp['iva_5'])
                    print(compra.iva_5)
                    compra.iva_10 = int(comp['iva_10'])
                    print(compra.iva_10)
                    compra.total = int(comp['total'])
                    print(compra.total)
                    print('orden compra')
                    compra.ordenCompra_id=comp['ordenCompra']
                    print( compra.ordenCompra_id)
                    compra.proveedor_id = comp['proveedor']
                    print(compra.proveedor_id)
                    usuario=User.objects.get(pk=self.request.user.id)
                    compra.user_id = usuario.id
                    compra.save()

                    print('ordencompraestado')
                    compra.ordenCompra.estado='1'
                    compra.ordenCompra.save()

                    print('cta')
                    ctaxpag=CuentaXpagar()
                    print('cta')
                    ctaxpag.compra_id = compra.id
                    print(ctaxpag.compra_id)
                    ctaxpag.estado='1'
                    print(ctaxpag.estado)
                    ctaxpag.monto_x_pagar= int(compra.total)
                    print(ctaxpag.monto_x_pagar)
                    ctaxpag.saldo= int(compra.total)
                    print(ctaxpag.saldo)
                    ctaxpag.save()
                    
                    for i in comp['productos']:
                        a=i['producto']
                        det = ComprasDet()
                        print('detalle')
                        det.compra_id = compra.id
                        print( det.compra_id )
                        det.producto_id = a['id']
                        print( det.producto_id )
                        det.precio = int(i['precio'])
                        print(det.precio)
                        det.cantidad = int(i['cantidad'])
                        print(det.cantidad )
                        det.subtotal = int(i['subtotal'])
                        print( det.subtotal)
                        det.save()
                        
                        det.producto.cant_stock += det.cantidad
                        det.producto.save()



                        mov_stock= MovimientoStock()
                        print('movimiento')
                        mov_stock.producto_id=a['id']
                        print(mov_stock.producto_id)
                        mov_stock.cant_mov=int(i['cantidad'])
                        print(mov_stock.cant_mov)
                        mov_stock.fecha_mov=comp['fecha_compra']
                        print(mov_stock.fecha_mov)
                        mov_stock.descripcion='Compra'
                        print(mov_stock.descripcion)
                        mov_stock.tipo_movimiento='0'
                        print(mov_stock.tipo_movimiento)
                        print(mov_stock)
                        mov_stock.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = 'verifique sus datos '
        return JsonResponse(data,safe=False)
   
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Registrar Compra'
        context['entity'] = 'Compra'
        context['list_url']= self.success_url
        context['action'] = 'add'
        return context

#Editar la compra
class CompraUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model=Compra
    form_class = CompraForm
    template_name='compra/create.html'
    permission_required = 'update_compra'
    success_url = reverse_lazy('Compra:compra_list')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Sobreescribimos el método post para editar mi orden de compra
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_orden_c':
                data=[]
                ordenC= OrdenCompra.objects.filter(estado='0')[0:10]
                for i in ordenC:
                    item = i.toJSON()
                    item['value'] = i.id
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():#si ocurre error no guarda nada
                    comp = json.loads(request.POST['comp'])
                    
                    compra = Compra()
                    compra.fecha_compra = comp['fecha_compra']
                    compra.tipo_compra = comp['tipo_compra']
                    compra.fecha_plazo = comp['fecha_plazo']
                    compra.subtotal = int(comp['subtotal'])
                    compra.iva_0 = int(comp['iva_0'])
                    compra.iva_5 = int(comp['iva_5'])
                    compra.iva_10 = int(comp['iva_10'])
                    compra.total = int(comp['total'])
                    compra.ordenCompra_id=comp['ordenCompra']
                    compra.proveedor_id = comp['proveedor']
                    compra.save()

                    compra.ordenCompra.estado='1'
                    compra.ordenCompra.save()

                    ctaxpag=CuentaXpagar()
                    ctaxpag.compra_id = compra.id
                    ctaxpag.estado='1'
                    ctaxpag.monto_x_pagar= int(compra.total)
                    ctaxpag.saldo= int(compra.total)
                    ctaxpag.save()
                    
                    for i in comp['productos']:
                        a=i['producto']
                        det = ComprasDet()
                        det.compra_id = compra.id
                        det.producto_id = a['id']
                        det.precio = int(i['precio'])
                        det.cantidad = int(i['cantidad'])
                        det.subtotal = int(i['subtotal'])
                        det.save()
                        det.producto.cant_stock += det.cantidad
                        det.producto.save()


            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    #para editar mi detalle de compra
    def get_detalle_compra(self):
        try:
            data=[]
            for i in ComprasDet.objects.filter(compra_id=self.get_object().id):
                item=i.producto.toJSON()
                print('---------')
                print(item)
                item['producto.nombre_producto']=i.producto.nombre_producto
                print(item['producto.nombre_producto'])
                item['producto']=i.cantidad
                item['precio']=i.precio
                item['cantidad']=i.cantidad
                item['subtotal']=i.subtotal
                data.append(item)          
        except:
            pass
        return data
        
        
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Editar Compra'
        context['entity']='Compra'
        context['list_url']= self.success_url
        context['action']='edit'
        context['det']=json.dumps(self.get_detalle_compra())
        print(context['det'])
        #context['list_url'] = reverse_lazy('pedido_proveedor_list')
        return context

#Eliminar
#html
class CompraView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('compra/compra.html') 
            context = {
                'compra': Compra.objects.get(pk=self.kwargs['pk']),
                'title': 'Compra'
            }
            html = template.render(context)

            return HttpResponse(html)
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse_lazy('Compra:compra_list')) 
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Compra'
        context['entity'] = 'Compra'
        context['list_url']= self.success_url
        return context

#factura
#Generar pdf con weasyprint de la Compra
class CompraPdfView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('compra/factura_c.html')
            context = {
                'compra': Compra.objects.get(pk=self.kwargs['pk']),
                'total': nl.Numero(Compra.objects.get(pk=self.kwargs['pk']).total).a_letras,
                #'cta': CuentaXpagar.objects.get(compra__id=self.kwargs['pk']),
            }
            print(context)
            html = template.render(context)
            compra=Compra.objects.get(pk=self.kwargs['pk'])
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('Compra:compra_list'))