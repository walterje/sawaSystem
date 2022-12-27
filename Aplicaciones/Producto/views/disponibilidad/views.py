from django.contrib.auth.mixins import LoginRequiredMixin
from cgi import print_form
import json
from tempfile import template
from django.db import transaction
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from Aplicaciones.User.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View
from Aplicaciones.Compra.forms import *
from django.conf import settings
from Aplicaciones.Producto.models import *
import os
from nlt import numlet as nl
from django.template import Context
from django.template.loader import get_template
#pdf weasyprint
from weasyprint import HTML, CSS
from django.template.loader import render_to_string

"""
class ProductoDisponibleView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            template = get_template('disponibilidad/producto_disponible.html') 
            data = []
            for p in Producto.objects.all():
                if p.cant_stock > 0:
                    data.append({
                        'producto': p.nombre_producto,
                        'stock_min': p.stock_minimo,
                        'cant_stock': p.cant_stock
                    })
                    print(data)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['title']='Disponibilidad de Productos'
        context['entity'] = 'Producto'
        context['list_url']= self.success_url
        print(context)
        return context
        
"""