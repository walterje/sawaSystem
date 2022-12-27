from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView


from Aplicaciones.Producto.forms import *
from Aplicaciones.Producto.models import *
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin

# Create your views here.
#Listar
class ProductoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model= Producto
    template_name='producto/list.html'
    permission_required = 'view_producto'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data =[]
                posicion = 1#para listar en orden los numeros del  id
                for i in Producto.objects.all():
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
        context['title']='Listado de Producto'
        context['create_url']=reverse_lazy('Producto:producto_create')
        context['list_url'] = reverse_lazy('Producto:producto_list')
        context['entity']='Producto'
        return context

# Crear
class ProductoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model=Producto
    form_class = ProductoForm
    template_name='producto/create.html'
    permission_required = 'add_producto'
    success_url = reverse_lazy('Producto:producto_list')

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
        return JsonResponse(data)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Creación de Producto'
        context['entity'] = 'Producto'
        context['list_url'] = reverse_lazy('Producto:producto_list')
        context['action'] = 'add'
        return context
# Editar
class ProductoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model=Producto
    form_class = ProductoForm
    template_name='Producto/create.html'
    permission_required = 'change_producto'
    success_url = reverse_lazy('producto_list')

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
        return JsonResponse(data, safe=False)
  
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Editar Producto'
        context['entity']='Producto'
        context['list_url'] = reverse_lazy('Producto:producto_list')
        context['action']='edit'
        return context
# Eliminar
class ProductoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model=Producto
    template_name='Producto/delete.html'
    permission_required = 'delete_producto'
    success_url = reverse_lazy('Producto:producto_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'Este producto ya tiene movimiento no se puede eliminar '
        return JsonResponse(data)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Eliminacion Producto'
        context['entity']='Producto'
        context['list_url'] = reverse_lazy('Producto:producto_list')
        return context

