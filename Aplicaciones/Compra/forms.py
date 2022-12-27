
import this
from django.forms import *
from django import forms
from Aplicaciones.Compra.models import *
from Aplicaciones.Caja.models import *
from datetime import datetime
from django.db.models import Q


#Formulario para proveedores
class ProveedorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus']=True
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del proveedor',
                }
            ),
            'ruc': TextInput(
                attrs={
                    'placeholder': 'Ingrese el ruc',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el numero de telefono',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la direccion',
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese el email',
                }
            ),
        }
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

#Formulario para orden Compra
class OrdenCompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].queryset = Proveedor.objects.none()
        
        
    class Meta:
        model = OrdenCompra
        #fields = '__all__'
        exclude = ['estado','company','user']
        widgets = {
            'proveedor': Select(attrs={
                'class': 'form-control select2',
                #'style': 'width: 100%'
            }),
            'fecha_orden': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_orden',
                    'data-target': '#fecha_orden',
                    'data-toggle': 'datetimepicker',
                    'readonly': True,
                }
            ),
           
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
             'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })

        }

#Forulario para compra
class CompraForm(ModelForm):
    #Envia las ordenes con estado pendiente
    ordenCompra=ModelChoiceField(
        queryset=OrdenCompra.objects.filter(estado='0')
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'fecha_compra': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_compra',
                    'data-target': '#fecha_compra',
                    'data-toggle': 'datetimepicker',
                    'readonly': True
                }
            ),
            'nro_factura': DateInput(
                attrs={
                    'style': 'width: 100%'
                    
            }),
            'tipo_compra': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'fecha_plazo': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_plazo',
                    'data-target': '#fecha_plazo',
                    'data-toggle': 'datetimepicker'
                    
            }),
            'ordenCompra': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }), 
            

        }


#para pago
class PagoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cuenta_x_pagar'].queryset = CuentaXpagar.objects.filter(estado='0')
        self.fields['caja'].queryset = Caja.objects.filter(estado='0')

    class Meta:
        model = Pago
        fields = '__all__'
        widgets = {
            'cuenta_x_pagar': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }), 
            'moneda': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
             'caja': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }), 
             'forma_pago': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }), 
            
            'fecha_pago': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_pago',
                    'data-target': '#fecha_pago',
                    'data-toggle': 'datetimepicker',
                    'readonly': True,
                }
            ),
            'monto_pagado': TextInput(attrs={
                'readonly': False,
                'class': 'form-control',
            }),

        }
#Para anular una 

class OC_ConfirForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['proveedor'].queryset = Proveedor.objects.none()
        
        
    class Meta:
        model = OrdenCompra
        exclude = ['fecha_orden','subtotal','iva_0','iva_5','iva_10','total',]
        widgets = {
            'proveedor': DateInput(attrs={
                'readonly': True,
                'class': 'form-control select2',
                'style': 'width: 100%',
              
            }),
            'estado': Select(attrs={
                'readonly': False,
                'class': 'form-control select2',
                'style': 'width: 100%',
              
            }),

        }  
