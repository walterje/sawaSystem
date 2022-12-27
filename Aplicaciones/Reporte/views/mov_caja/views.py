from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView
from Aplicaciones.Reporte.forms import *
from Aplicaciones.Caja.models import *

from django.db.models.functions import Coalesce
from django.db.models import Sum

class ReporteMovCajaView(LoginRequiredMixin, TemplateView):
    template_name = 'mov_caja/reporte.html'

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
                search = MovimientoCaja.objects.all()#obtengo todos los datos de mi orden de Compra 
                if len(start_date) and len(end_date):#si  el rango tiene valor
                    search = search.filter(fecha_movimiento__range=[start_date, end_date])
                for i in search:
                    data.append([
                        i.id,
                        i.fecha_movimiento.strftime('%Y-%m-%d'),
                        i.caja.nombre,
                        i.descripcion,
                        format(i.monto_inicio, '.0f'),
                        format(i.monto_cierre, '.0f'),
                        format(i.monto_ingreso, '.0f'),
                        format(i.monto_egreso, '.0f'),
                    ])
                monto_ingreso = search.aggregate(r=Coalesce(Sum('monto_ingreso'), 0)).get('r')
                monto_egreso = search.aggregate(r=Coalesce(Sum('monto_egreso'), 0)).get('r')

                data.append([
                    '-',
                    '-',
                    '-',
                    '-',
                    '-',
                    '-',
                    format(monto_ingreso, '.0f'),
                    format(monto_egreso, '.0f'),
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Movimiento Caja'
        context['entity'] = 'Reporte'
        context['list_url'] = reverse_lazy('Reporte:movimiento_caja_reporte')
        context['form'] = ReporteForm()
        return context