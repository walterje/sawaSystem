from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from Aplicaciones.Producto.forms import *
from Aplicaciones.Producto.models import *

# Create your views here.
#Listar
class TipoProductoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model=TipoProducto
    template_name='tipoProducto/list.html'
    permission_required = 'view_tipo_producto'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data =[]
                posicion = 1#para listar en orden los numeros del  id
                for i in TipoProducto.objects.all():
                    item = i.toJSON()
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
        context['title']='Listado de Tipo Producto'
        context['create_url']=reverse_lazy('Producto:tipo_producto_create')
        context['list_url'] = reverse_lazy('Producto:tipo_producto_list')
        context['entity']='TipoProducto'
        return context
# Crear
class TipoProductoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model=TipoProducto
    form_class = TipoProductoForm
    template_name='tipoProducto/create.html'
    success_url = reverse_lazy('Producto:tipo_producto_list')
    permission_required = 'add_tipo_producto'
    url_redirect = success_url

    #@method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Creación de TipoProducto'
        context['entity'] = 'TipoProducto'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
# Editar
class TipoProductoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model=TipoProducto
    form_class = TipoProductoForm
    template_name='tipoProducto/create.html'
    success_url = reverse_lazy('Producto:tipo_producto_list')
    permission_required = 'change_tipo_producto'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
  
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Editar TipoProducto'
        context['entity']='TipoProducto'
        context['list_url'] = self.success_url
        context['action']='edit'
        return context
# Eliminar
class TipoProductoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model=TipoProducto
    template_name='tipoProducto/delete.html'
    success_url = reverse_lazy('Producto:tipo_producto_list')
    permission_required = 'delete_tipo_producto'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error']='No se puede eliminar ya tiene productos que pertenece a este tipo'
            #data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Eliminacion TipoProducto'
        context['entity']='TipoProducto'
        context['list_url'] = self.success_url
        return context
