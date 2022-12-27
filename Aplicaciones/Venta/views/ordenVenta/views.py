from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from Aplicaciones.Venta.models import *
from django.urls import reverse_lazy
from django.contrib import messages
import json
import os
from nlt import numlet as nl
from django.db.models import Q
from django.conf import settings
from tempfile import template
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.http import JsonResponse
from django.template.loader import get_template
from weasyprint import HTML, CSS
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View
from Aplicaciones.Venta.forms import *
#Listar orden Venta
class OrdenVentaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model=OrdenVenta
    template_name='ordenVenta/list.html'
    permission_required = 'view_ordenventa'
    
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
                estado0='Pendiente'
                estado1='Confirmado'
                estado2='Anulado'
                for i in OrdenVenta.objects.all():
                    item=i.toJSON()
                    item['posicion'] = posicion
                    data.append(item)
                    posicion += 1
                    if item['estado']== '0':
                        item['estado']=estado0
                    elif item['estado']== '1':
                        item['estado']=estado1
                    elif item['estado']== '2':
                        item['estado']=estado2
            elif action=='search_details_prod':
                data=[]

                for i in OrdenVentaDet.objects.filter(nro_orden_v_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Listado de Orden de Venta'
        context['create_url']=reverse_lazy('Venta:orden_venta_create')
        context['list_url']=reverse_lazy('Venta:orden_venta_list')
        context['entity']='OrdenVenta'
        return context

#Crear orden Venta
class OrdenVentaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model=OrdenVenta
    form_class = OrdenVentaForm
    template_name='ordenVenta/create.html'
    success_url = reverse_lazy('Venta:orden_venta_list')
    permission_required = 'add_ordenventa'
    url_redirect = success_url
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
   
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                #prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term']).exclude(cant_stock=0)[0:5]
                #prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term'])[0:5]
                prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term'])[0:5]
                print(prods)
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre_producto
                    data.append(item)

            elif action=='add':
                with transaction.atomic():# si ocurre error en el detalle y no me guarde
                    orden_v = json.loads(request.POST['orden_v'])

                    orden_venta = OrdenVenta()
                    orden_venta.fecha_orden_v= orden_v['fecha_orden_v']
                    orden_venta.cliente_id = orden_v['cliente']
                    orden_venta.subtotal = int(orden_v['subtotal'])
                    orden_venta.iva_0 = int(orden_v['iva_0'])
                    orden_venta.iva_5 = int(orden_v['iva_5'])
                    orden_venta.iva_10 = int(orden_v['iva_10'])
                    orden_venta.total = int(orden_v['total'])
                    usuario=User.objects.get(pk=self.request.user.id)
                    orden_venta.user_id = usuario.id
                    orden_venta.save()
                    for i in orden_v['productos']:
                        det = OrdenVentaDet()
                        det.nro_orden_v_id = orden_venta.id
                        print()
                        det.producto_id = i['id']
                        det.precio_venta = int(i['precio_venta'])
                        det.cantidad = int(i['cantidad'])
                        det.subtotal =int(i['subtotal'])
                        det.save()
            elif action == 'search_clientes':
                data = []
                term = request.POST['term']
                cliente = Cliente.objects.filter(
                    Q(nombre__icontains=term) | Q(apellido__icontains=term) | Q(ci__icontains=term))[0:10]
                for i in cliente:
                    item = i.toJSON()
                    item['text'] = i.get_nombre_completo()
                    data.append(item)
            elif action == 'create_cliente':
                print(request.POST)
                with transaction.atomic():
                    formCliente = ClienteForm(request.POST)
                    print(formCliente)
                    data = formCliente.save()
            else:      
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Registro de una orden de Venta'
        context['entity'] = 'OrdenVenta'
        context['list_url']= self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['formCliente'] = ClienteForm()
        return context


#Editar orden Venta
class OrdenVentaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model=OrdenVenta
    form_class = OrdenVentaForm
    template_name='OrdenVenta/create.html'
    permission_required = 'change_orden_venta'
    success_url = reverse_lazy('Venta:orden_venta_list')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        #para editar el orden y que me cargue el cliente
    def get_form(self, form_class=None):
        instance = self.get_object()
        form = OrdenVentaForm(instance=instance)
        form.fields['cliente'].queryset = Cliente.objects.filter(id=instance.cliente.id)
        return form
    #Sobreescribimos el método post para editar mi orden de venta
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term'])[0:5]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre_producto
                    data.append(item)
            elif action=='edit':
                with transaction.atomic():
                    orden_v = json.loads(request.POST['orden_v'])
                    ordenVenta = self.get_object()
                    ordenVenta.fecha_orden_v = orden_v['fecha_orden_v']
                    ordenVenta.cliente_id=orden_v['cliente']
                    ordenVenta.estado=orden_v['estado']
                    ordenVenta.subtotal=int(orden_v['subtotal'])
                    ordenVenta.iva_0=int(orden_v['iva_0'])
                    ordenVenta.iva_5=int(orden_v['iva_5'])
                    ordenVenta.iva_10=int(orden_v['iva_10'])
                    ordenVenta.total=int(orden_v['total'])
                    usuario=User.objects.get(pk=self.request.user.id)
                    ordenVenta.user_id = usuario.id
                    ordenVenta.save()
                    ordenVenta.ordenventadet_set.all().delete()#para borrar mis detalles y se me actualize
                    for i in orden_v['productos']:
                        det = OrdenVentaDet()
                        det.nro_orden_v_id = ordenVenta.id
                        det.producto_id = i['id']
                        det.precio_venta = int(i['precio_venta'])
                        det.cantidad = int(i['cantidad'])
                        det.subtotal = int(i['subtotal'])
                        det.save()
            elif action == 'search_clientes':
                data = []
                term = request.POST['term']
                clientes = Cliente.objects.filter(
                    Q(nombre__icontains=term) | Q(apellido__icontains=term) | Q(ci__icontains=term))[0:10]
                for i in clientes:
                    item = i.toJSON()
                    item['text'] = i.get_nombre_completo()
                    data.append(item)
            elif action == 'create_cliente':
                with transaction.atomic():
                   
                    formCliente = ClienteForm(request.POST)
                    data = formCliente.save()
    
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    #para editar mi detalle de la ordn de venta
    def get_detalle_orden_venta(self):
        data=[]
        try:
            for i in OrdenVentaDet.objects.filter(nro_orden_v_id=self.get_object().id):
                item=i.producto.toJSON()
                item['cantidad']=i.cantidad
                data.append(item)
        except:
            pass
        return data
        
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Editar Orden Venta'
        context['entity']='OrdenVenta'
        context['list_url']= self.success_url
        context['action']='edit'
        context['det']=json.dumps(self.get_detalle_orden_venta())
        context['formCliente'] = ClienteForm()
        #context['list_url'] = reverse_lazy('pedido_proveedor_list')
        return context


#Generar pdf con weasyprint de la orden de Venta
class OrdenVentaPDFView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('ordenVenta/ordenVentaPDF.html')
            context = {
                'ordenVenta': OrdenVenta.objects.get(pk=self.kwargs['pk']),
                'total': nl.Numero(OrdenVenta.objects.get(pk=self.kwargs['pk']).total).a_letras,
                'title': 'Orden de Venta'
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('Venta:orden_venta_list'))

