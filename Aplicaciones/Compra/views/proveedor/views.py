from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from Aplicaciones.Compra.models import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.http import JsonResponse
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from Aplicaciones.Compra.forms import *
# Create your views here.
#Proveedor List
class ProveedorListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model = Proveedor
    template_name='proveedor/list.html'
    context_object_name="object_list"
    permission_required = 'view_proveedor'
        
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data =[]
                posicion = 1
                for i in Proveedor.objects.all():
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
        context = super().get_context_data(**kwargs)
        context['title']='Listado de Proveedores'
        context['create_url']=reverse_lazy('Compra:proveedor_create')
        context['list_url']=reverse_lazy('Compra:proveedor_list')
        context['entity']='Proveedores'
        return context
#crear
class ProveedorCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,SuccessMessageMixin ,CreateView):
    model=Proveedor
    form_class = ProveedorForm
    template_name='proveedor/create.html'
    success_url = reverse_lazy('Compra:proveedor_list')
    success_message = 'Creado exitosamente'
    permission_required = 'add_proveedor'
    url_redirect = success_url
   
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Creación de Proveedor'
        context['entity'] = 'Proveedor'
        context['list_url']= self.success_url
        context['action'] = 'add'
        return context
        
#Editar
class ProveedorUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    model= Proveedor
    form_class = ProveedorForm
    template_name='proveedor/create.html'
    success_url = reverse_lazy('Compra:proveedor_list')
    success_message = "Proveedor actualizada"
    permission_required = 'change_proveedor'
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
        context['title']='Editar Proveedor'
        context['entity']='Proveedor'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

#Eliminar Proveedor
class ProveedorDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model = Proveedor
    template_name='proveedor/delete.html'
    success_url = reverse_lazy('Compra:proveedor_list')
    permission_required = 'delete_proveedor'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'Este proveedor no se puede eliminar'
        return JsonResponse(data)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Eliminacion de Proveedor'
        context['entity']='Proveedor'
        context['list_url'] = self.success_url
        return context