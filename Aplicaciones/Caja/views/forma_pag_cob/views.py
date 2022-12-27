from django.contrib.auth.mixins import LoginRequiredMixin
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from Aplicaciones.Caja.forms import *
from Aplicaciones.Caja.models import *

# Create your views here.
#Listar
class FormaPagCobListView(LoginRequiredMixin, ValidatePermissionRequiredMixin,ListView):
    model=FormaPago
    template_name='forma_pag_cob/list.html'
    permission_required = 'view_forma_pago'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data =[]
                posicion = 1#para listar en orden los numeros del  id
                for i in FormaPago.objects.all():
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
        context['title']='Listado de Forma Pago'
        context['create_url']=reverse_lazy('Caja:forma_pag_cob_create')
        context['list_url'] = reverse_lazy('Caja:forma_pag_cob_list')
        context['entity']='Forma Pago'
        return context

# Crear
class FormaPagCobCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,CreateView):
    model=FormaPago
    form_class = FormaPagCobForm
    template_name='forma_pag_cob/create.html'
    success_url = reverse_lazy('Caja:forma_pag_cob_list')
    permission_required = 'add_forma_pag'
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
        context['title']='Creación de Forma Pago Cobro'
        context['entity'] = 'Forma Pago'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

# Editar
class FormaPagCobUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model=FormaPago
    form_class = FormaPagCobForm
    template_name='forma_pag_cob/create.html'
    success_url = reverse_lazy('Caja:forma_pag_cob_list')
    permission_required = 'change_forma_pag' 
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
        context['title']='Editar Forma Pago Cobro'
        context['entity']='Forma Pago'
        context['list_url'] = self.success_url
        context['action']='edit'
        return context
# Eliminar
class FormaPagCobDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin,DeleteView):
    model=FormaPago
    template_name='forma_pag_cob/delete.html'
    success_url = reverse_lazy('Caja:forma_pag_cob_list')
    permission_required = 'delete_forma_pago'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = 'No se puede eliminar esta forma de pago'
        return JsonResponse(data)

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Eliminacion Forma Pago Cobro'
        context['entity']='Forma Pago'
        context['list_url'] = self.success_url
        return context
