from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView
from Aplicaciones.Reporte.forms import *
from Aplicaciones.Venta.models import Venta

from django.db.models.functions import Coalesce
from django.db.models import Sum

class ReporteVentaView(LoginRequiredMixin, TemplateView):
    template_name = 'venta/reporte.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data =[]
                start_date = request.POST.get('start_date','')
                end_date = request.POST.get('end_date','')#si no encuentra valor con post le asignamos vacio
                search = Venta.objects.all()#obtengo todos los datos de mi orden de Compra 
                if len(start_date) and len(end_date):#si  el rango tiene valor
                    search = search.filter(fecha_venta__range=[start_date, end_date])
                for i in search:
                    data.append([
                        i.id,
                        i.fecha_venta.strftime('%Y-%m-%d'),
                        i.cliente.nombre + ' ' + i.cliente.apellido,
                        #format(i.subtotal, '.2f'),
                        format(i.total, '.0f'),
                    ])
                #subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')

                data.append([
                    '-',
                    '-',
                    '-',
                    #format(subtotal, '.2f'),
                    format(total, '.0f'),
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Venta'
        context['entity'] = 'Reporte'
        context['list_url'] = reverse_lazy('Reporte:venta_reporte')
        context['form'] = ReporteForm()
        return context