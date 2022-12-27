from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from Aplicaciones.Venta.models import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from Aplicaciones.Venta.forms import *
#Listar
class ClienteListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Cliente
    template_name='cliente/list.html'
    permission_required = 'view_cliente'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data =[]
                posicion = 1
                for i in Cliente.objects.all():
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
        context['title']='Lista de Cliente'
        context['create_url']=reverse_lazy('Venta:cliente_create')
        context['list_url']=reverse_lazy('Venta:cliente_list')
        context['entity']='Clientes'
        return context
#Crear
class ClienteCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,SuccessMessageMixin ,CreateView):
    model=Cliente
    form_class = ClienteForm
    template_name='cliente/create.html'
    permission_required = 'add_cliente'
    success_url = reverse_lazy('Venta:cliente_list')
    success_message = 'Creado exitosamente'
    permission_required = 'add_cliente', 
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
        context['title']='Registro de Cliente'
        context['entity'] = 'Cliente'
        context['list_url']= self.success_url
        context['action'] = 'add'
        return context

#Editar
class ClienteUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    model= Cliente
    form_class = ClienteForm
    template_name='cliente/create.html'
    permission_required = 'change_cliente'
    success_url = reverse_lazy('Venta:cliente_list')
    success_message = "Cliente actualizada"
    permission_required = 'change_cliente', 
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
        context['title']='Editar Cliente'
        context['entity']='Cliente'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
#Eliminar
class ClienteDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model = Cliente
    template_name='cliente/delete.html'
    permission_required = 'delete_cliente'
    success_url = reverse_lazy('Venta:cliente_list')
    permission_required = 'delete_cliente', 
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'No se puede eliminar tiene cuenta pendiente'
        return JsonResponse(data)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Eliminar Clientes'
        context['entity']='Cliente'
        context['list_url'] = self.success_url
        return context