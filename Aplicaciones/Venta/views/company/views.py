from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import UpdateView
from Aplicaciones.Venta.models import *
from Aplicaciones.Venta.forms import *


class CompanyUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin,UpdateView):
    model = Company
    form_class = CompanyForm
    template_name='cliente/create.html'
    permission_required = 'change_company'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        company = Company.objects.all()
        if company.exists():
            return company[0]
        return Company()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                instance = self.get_object()
                if instance.pk is not None:
                    form = CompanyForm(request.POST, request.FILES, instance=instance)
                    data = form.save()
                else:
                    form = CompanyForm(request.POST, request.FILES)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de mi compañia'
        context['entity'] = 'Compañia'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
