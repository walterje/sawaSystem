from django.forms import *
from django import forms
from Aplicaciones.Compra.models import *
from datetime import datetime


#Formulario para rejistar una caja
class CajaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus']=True
    class Meta:
        model = Caja
        exclude = ['monto_inicio','monto_cierre','total_ingreso','total_egreso','estado','saldo_actual']
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre',
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

class MonedaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus']=True

    class Meta:
        model = Moneda
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la descipcion de la moneda',
                }
            ),
            'sigla': TextInput(
                attrs={
                    'placeholder': 'Ingrese la sigla de la moneda',
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
#Forma Pago Cobro
class FormaPagCobForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['autofocus']=True

    class Meta:
        model = FormaPago
        fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la descipcion',
                }
            )
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

#AperturaCaja
class AperturaCajaForm(ModelForm):
     #Envia la caja con estado cerrado para abrir
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model =Caja
        
        #fields = '__all__'
        exclude = ['moneda','monto_cierre','total_ingreso','total_egreso','estado','saldo_actual']
        widgets = {
            'nombre': TextInput( attrs={
                'readonly': False,
                'readonly': True,
        }),
            'monto_inicio': TextInput(attrs={
                'readonly': False,
                'class': 'form-control',
            }),
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

#Cierre Caja
class CierreCajaForm(ModelForm):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model =Caja
        
        #fields = '__all__'
        exclude = ['moneda','monto_inicio','total_ingreso','total_egreso','estado','saldo_actual']
        widgets = {
            'nombre': TextInput( attrs={
                'readonly': False,
                'readonly': True,
        }),
        'saldo_actual': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
        }),
        'monto_cierre': TextInput(attrs={
            'readonly': False,
            'class': 'form-control',
        }),
            
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

#ingresos varios
class MovimientosVariosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['descripcion'].widget.attrs['autofocus']=True

    class Meta:
        model = MovimientoCaja
        exclude = ['monto_inicio','monto_cierre','tipo_movimiento']
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingresela descripcion',
                    'style': 'width: 100%'
                }
            ),
             'caja': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }),
            'fecha_movimiento': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_mov',
                    'data-target': '#fecha_mov',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'monto_ingreso': TextInput(attrs={
                'readonly': False,
                'class': 'form-control',
            }),
            'monto_egreso': TextInput(attrs={
                'readonly': False,
                'class': 'form-control',
            }),
        }
    