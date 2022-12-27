from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView
from Aplicaciones.Reporte.forms import *
from Aplicaciones.Compra.models import OrdenCompra

from django.db.models.functions import Coalesce
from django.db.models import Sum

class ReporteOrdenCView(LoginRequiredMixin, TemplateView):
    template_name = 'ordenC/reporte.html'

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
                search = OrdenCompra.objects.all()#obtengo todos los datos de mi orden de Compra 
                if len(start_date) and len(end_date):#si  el rango tiene valor
                    search = search.filter(fecha_orden__range=[start_date, end_date])
                for i in search:
                    data.append([
                        i.id,
                        i.fecha_orden.strftime('%Y-%m-%d'),
                        i.proveedor.nombre,
                        i.estado,
                        '{:,}'.format((i.subtotal)).replace(',','.'),
                        '{:,}'.format((i.subtotal)).replace(',','.'),
                        #format(i.subtotal),
                        format(i.total),
                    ])
                subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'), 4)).get('r')
                

                data.append([
                    '---',
                    '---',
                    '---',
                    '---',
                    '{:,}'.format((subtotal)).replace(',','.'),
                   # format(subtotal, '.2f'),
                    format('{:,}'.format((total)).replace(',','.'),),
                    print(format('{:,}'.format((total)).replace(',','.'),))
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Orden Compra'
        context['entity'] = 'Reporte'
        context['list_url'] = reverse_lazy('Reporte:ordenC_reporte')
        context['form'] = ReporteForm()
        return context