from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,TemplateView
from Aplicaciones.Caja.forms import *
from Aplicaciones.Caja.models import *
from django.db import transaction

#Modals crear caja
class CajaView(LoginRequiredMixin, ValidatePermissionRequiredMixin,TemplateView):
    template_name = 'caja/list.html'
    permission_required = 'view_caja'
    #permission_required = 'view_caja', 'change_caja', 'delete_caja', 'add_caja'


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
                estado0='Abierto'
                estado1='Cerrado'
                for i in Caja.objects.all(): 
                    item=i.toJSON()
                    item['posicion'] = posicion
                    data.append(item)
                    if item['estado']== '0':
                         item['estado']=estado0
                    elif item['estado']== '1':
                        item['estado']=estado1
                    posicion += 1
            elif action == 'add':
                caj = Caja()
                caj.nombre = request.POST['nombre']
                caj.moneda_id = request.POST['moneda']
                caj.save()
            elif action == 'edit':
                caj = Caja.objects.get(pk=request.POST['id'])
                caj.nombre = request.POST['nombre']
                caj.save()
            elif action == 'delete':
                cli = Caja.objects.get(pk=request.POST['id'])
                cli.delete()
            elif action == 'aper':
                #total_ingreso=0
                caj = Caja.objects.get(pk=request.POST['id'])
                caj.nombre = request.POST['nombre']
                caj.monto_inicio = int(request.POST['monto_inicio'])
                caj.saldo_actual=int(caj.saldo_actual) + int(caj.monto_inicio)
                caj.monto_cierre = 0
                #total_ingreso +=int(caj.monto_inicio)
                #caj.total_ingreso = total_ingreso
                caj.estado='0'
                caj.save()

                mov_caja= MovimientoCaja()
                mov_caja.monto_movimiento=caj.monto_inicio
                mov_caja.descripcion='Apertura'
                mov_caja.tipo_movimiento='0'
                mov_caja.monto_inicio=caj.monto_inicio
                mov_caja.caja_id=caj.id
                mov_caja.save()
            elif action == 'cierre':
                total_egreso=0
                caj = Caja.objects.get(pk=request.POST['id'])
                caj.nombre = request.POST['nombre']
                caj.monto_cierre = request.POST['monto_cierre']
                if (caj.monto_cierre == 0):
                    data['error'] = 'Ingrese el monto'
                caj.saldo_actual=int(caj.saldo_actual) - int(caj.monto_cierre)
                caj.monto_inicio = 0
                #total_egreso +=int(caj.monto_cierre)
                #caj.total_egreso = total_egreso
                caj.estado='1'
                caj.save()

                mov_caja= MovimientoCaja()
                mov_caja.monto_movimiento=caj.monto_cierre
                mov_caja.descripcion='Cierre Caja'
                mov_caja.tipo_movimiento='1'
                #mov_caja.monto_egreso=mov_caja.monto_movimiento
                mov_caja.monto_ingreso=0
                mov_caja.monto_cierre=caj.monto_cierre
                mov_caja.caja_id=caj.id
                mov_caja.save()

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = data['error'] = 'Ha ocurrido un error'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Caja'
        context['list_url'] = reverse_lazy('Caja:caja')
        context['entity'] = 'Cajas'
        context['form'] = CajaForm()
        context['form_aperCaja'] = AperturaCajaForm()
        context['form_cierreCaja'] = CierreCajaForm()
        return context


