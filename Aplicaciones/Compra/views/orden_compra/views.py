from django.contrib.auth.mixins import LoginRequiredMixin
from cgi import print_form
import json
from tempfile import template
from django.db import transaction
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View
from Aplicaciones.Compra.forms import *
from django.conf import settings
from Aplicaciones.Compra.models import *
from Aplicaciones.User.models import *
import os
from nlt import numlet as nl
from django.template import Context
from django.template.loader import get_template
#pdf weasyprint
from weasyprint import HTML, CSS
from django.template.loader import render_to_string

# Create your views here.
#Listar la orden de Compra
class OrdenCompraListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model=OrdenCompra
    template_name='ordenCompra/list.html'
    permission_required = 'view_ordencompra'
    
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
                for i in OrdenCompra.objects.all():
                    item=i.toJSON()
                    item['posicion'] = posicion
                    data.append(item)
                    if item['estado']== '0':
                        item['estado']=estado0
                    elif item['estado']== '1':
                        item['estado']=estado1
                    elif item['estado']== '2':
                        item['estado']=estado2
                    posicion += 1
                print(request.user.username)
                                  
            elif action=='search_details_prod':
                data=[]
                for i in OrdenCompraDet.objects.filter(nro_orden_c_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'confir':
                oc= OrdenCompra.objects.get(pk=request.POST['id'])
                oc.proveedor.nombre=request.POST['proveedor']
                print(oc.proveedor.nombre)
                oc.estado = request.POST['estado']
                print(oc.estado )
                oc.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Listado de Orden'
        context['create_url']=reverse_lazy('Compra:orden_compra_create')
        context['list_url']=reverse_lazy('Compra:orden_compra_list')
        context['entity']='OrdenCompra'
        context['form_OC_confir']=OC_ConfirForm()
        return context

#Crear la orden de Compra
class OrdenCompraCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model= OrdenCompra
    form_class = OrdenCompraForm
    template_name='ordenCompra/create.html'
    success_url = reverse_lazy('Compra:orden_compra_list')
    success_message = 'Creado exitosamente'
    permission_required = 'add_ordencompra'
    url_redirect = success_url

    @method_decorator(csrf_exempt)#para desactivar el mecanismo de defensa del post
    def dispatch(self, request, *args,**kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                #prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term']).exclude(es_servicio=True)[0:5]
                #prods = Producto.objects.exclude(tipo_producto = '13' )[0:10]
                #prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term']).exclude(tipo_producto ='13')[0:10]
                prods = Producto.objects.filter(nombre_producto__icontains=request.POST['term']).exclude(tipo_producto ='2')[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre_producto
                    data.append(item)
            elif action=='add':
                with transaction.atomic():# si ocurre error en el detalle y no me guarde
                    orden_c = json.loads(request.POST['orden_c'])
                    print(orden_c)

                    orden_compra = OrdenCompra()
                    orden_compra.fecha_orden= orden_c['fecha_orden']
                    orden_compra.proveedor_id = orden_c['proveedor']
                    orden_compra.subtotal = int(orden_c['subtotal'])
                    orden_compra.iva_0 = int(orden_c['iva_0'])
                    orden_compra.iva_5 = int(orden_c['iva_5'])
                    orden_compra.iva_10 = int(orden_c['iva_10'])
                    orden_compra.total = int(orden_c['total'])
                    usuario=User.objects.get(pk=self.request.user.id)
                    orden_compra.user_id = usuario.id
                    orden_compra.save()
                    for i in orden_c['productos']:
                        det = OrdenCompraDet()
                        print('---------')
                        print(orden_compra.id)
                        det.nro_orden_c_id = orden_compra.id
                        det.producto_id = i['id']
                        det.precio = int(i['precio_compra'])
                        det.cantidad = int(i['cantidad'])
                        det.subtotal =int(i['subtotal'])
                        
                        det.save()
            elif action == 'search_prov':
                data = []
                term = request.POST['term']
                prov = Proveedor.objects.filter(
                    Q(nombre__icontains=term) | Q(ruc__icontains=term))[0:10]
                for i in prov:
                    item = i.toJSON()
                    item['text'] = i.get_proveedor()
                    data.append(item)
            elif action == 'create_prov':
                with transaction.atomic():
                    formProv = ProveedorForm(request.POST)
                    data = formProv.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)#para que se pueda seializar el save=False


    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Creación de una orden de Compra'
        context['entity'] = 'OrdenCompra'
        context['list_url']= self.success_url
        context['action'] = 'add'
        context['formProv'] = ProveedorForm()
        return context

#Editar la orden de Compra
class OrdenCompraUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model=OrdenCompra
    form_class = OrdenCompraForm
    template_name='OrdenCompra/create.html'
    permission_required = 'change_orden_compra'
    success_url = reverse_lazy('Compra:orden_compra_list')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_form(self, form_class=None):
        instance = self.get_object()
        form = OrdenCompraForm(instance=instance)
        form.fields['proveedor'].queryset = Proveedor.objects.filter(id=instance.proveedor.id)
        return form
    #Sobreescribimos el método post para editar mi orden de compra
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
                    orden_c = json.loads(request.POST['orden_c'])
                    
                    ordenCompra = self.get_object()
                    ordenCompra.fecha_orden = orden_c['fecha_orden']
                    ordenCompra.proveedor_id=orden_c['proveedor']
                    ordenCompra.estado=orden_c['estado']
                    ordenCompra.subtotal=int(orden_c['subtotal'])
                    ordenCompra.iva_0=int(orden_c['iva_0'])
                    ordenCompra.iva_5=int(orden_c['iva_5'])
                    ordenCompra.iva_10=int(orden_c['iva_10'])
                    ordenCompra.total=int(orden_c['total'])
                    usuario=User.objects.get(pk=self.request.user.id)
                    ordenCompra.user_id = usuario.id
                    ordenCompra.save()
                    ordenCompra.ordencompradet_set.all().delete()#para borrar mis detalles y se me actualize
                    for i in orden_c['productos']:
                        det = OrdenCompraDet()
                        det.nro_orden_c_id = ordenCompra.id
                        det.producto_id = i['id']
                        det.precio = int(i['precio_compra'])
                        det.cantidad = int(i['cantidad'])
                        det.subtotal = int(i['subtotal'])
                        det.save()
            elif action == 'search_prov':
                data = []
                term = request.POST['term']
                prov = Proveedor.objects.filter(
                    Q(nombre__icontains=term) | Q(ruc__icontains=term))[0:10]
                for i in prov:
                    item = i.toJSON()
                    item['text'] = i.get_proveedor()
                    data.append(item)
            elif action == 'create_prov':
                with transaction.atomic():
                    formProv = ProveedorForm(request.POST)
                    data = formProv.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    #para editar mi detalle de la ordn de compra
    def get_detalle_orden_compra(self):
        data=[]
        try:
            for i in OrdenCompraDet.objects.filter(nro_orden_c_id=self.get_object().id):
                item=i.producto.toJSON()
                item['cantidad']=i.cantidad
                data.append(item)
        except:
            pass
        return data
        
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Editar Orden'
        context['entity']='OrdenCompra'
        context['list_url']= self.success_url
        context['action']='edit'
        context['det']=json.dumps(self.get_detalle_orden_compra())
        #context['list_url'] = reverse_lazy('pedido_proveedor_list')
        return context

#eliminar la orden de Compra
class OrdenCompraDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model = OrdenCompra
    template_name = 'ordenCompra/delete.html'
    permission_required = 'delete_orden_compra'
    success_url = reverse_lazy('Compra:orden_compra_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            oc= OrdenCompra.objects.get(pk=request.POST['id'])
            print(oc)
            print(self.get_object())
            self.object.delete()
        except Exception as e:
            data['error'] = 'No se eliminara la orden compra, solo se anulara'
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Orden'
        context['entity'] = 'OrdenCompra'
        context['list_url'] = self.success_url
        return context
 
#Generar pdf con weasyprint de la orden de Compra
class OrdenCPdfView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('ordenCompra/ordenC.html')
            context = {
                'ordenCompra': OrdenCompra.objects.get(pk=self.kwargs['pk']),
                'total': nl.Numero(OrdenCompra.objects.get(pk=self.kwargs['pk']).total).a_letras,
                 'title': 'Orden de Compra'
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.4.1-dist/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('Compra:orden_compra_list'))

