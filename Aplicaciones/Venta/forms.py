from django.forms import *
from django import forms
from Aplicaciones.Venta.models import *
from datetime import datetime
from Aplicaciones.Caja.models import *

#Formulario para cliente
class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus']=True
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'ci': TextInput(
                attrs={
                    'placeholder': 'Ingrese su numero de cedula',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese su direccion',
                }
            ),
              'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese el el numero de su telefono',
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

#Formulario para orden Venta
class OrdenVentaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.none()
        
    class Meta:
        model = OrdenVenta
        #fields = '__all__'
        exclude=['estado','company','user']
        widgets = {
            'cliente': Select(attrs={
                'class': 'form-control select2',
                #'style': 'width: 100%' #porque el boton de cliente de mi orden se muestra abajo
            }),
            'fecha_orden_v': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_orden_v',
                    'data-target': '#fecha_orden_v',
                    'data-toggle': 'datetimepicker',
                    'readonly': True,
                }
            ),

            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
             'iva_0': TextInput(attrs={
                'class': 'form-control',
            }),
             'iva_5': TextInput(attrs={
                'class': 'form-control',
            }),
             'iva_10': TextInput(attrs={
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })

        }

#Forulario para venta
class VentaForm(ModelForm):
    #Envia las ordenes con estado pendiente
    ordenVenta=ModelChoiceField(
        queryset=OrdenVenta.objects.filter(estado='0')
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
            'fecha_venta': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_venta',
                    'data-target': '#fecha_venta',
                    'data-toggle': 'datetimepicker',
                    'readonly': True,
                }
            ),
            'tipo_venta': Select(attrs={
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
            'ordenVenta': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }), 

        }

    
# cobro
class CobroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['cuenta_x_cobrar'].queryset = CuentaXcobrar.objects.filter(estado='1')
        self.fields['caja'].queryset = Caja.objects.filter(estado='0')

    class Meta:
        model = Cobro
        fields = '__all__'
        widgets = {
            'cuenta_x_cobrar': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }), 
             'caja': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }), 
             'forma_cobro': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }), 
            'fecha_cobro': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_cobro',
                    'data-target': '#fecha_cobro',
                    'data-toggle': 'datetimepicker',
                    'readonly': True,
                }
            ),
            'monto_cobrado': TextInput(attrs={
                'readonly': False,
                'class': 'form-control',
            }),

        }

    
#Compañia
class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'celular': forms.TextInput(attrs={'placeholder': 'Ingrese un numero celular'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono convencional'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un mail'}),
            'timbrado': forms.TextInput(attrs={'placeholder': 'Ingrese el timbrado'}),
            'fecha_desde': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_desde',
                    'data-target': '#fecha_desde',
                    'data-toggle': 'datetimepicker',
                    'readonly': False,
                }
            ),
             'fecha_hasta': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_hasta',
                    'data-target': '#fecha_hasta',
                    'data-toggle': 'datetimepicker',
                    'readonly': False,
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data