from django.forms import *
from Aplicaciones.Producto.models import MovimientoStock, TipoProducto, Producto
from datetime import datetime

class TipoProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus']=True

    class Meta:
        model = TipoProducto
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del tipo de producto',
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

class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_producto'].widget.attrs['autofocus']=True

    class Meta:
        model = Producto
        #fields = '__all__'
        exclude = ['cant_stock']
        widgets = {
            'nombre_producto': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del producto',

                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                print(form)
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data  

#Mov stock
class MovStockForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['descripcion'].widget.attrs['autofocus']=True

    class Meta:
        model = MovimientoStock
        exclude = ['tipo_movimiento']
        #fields = '__all__'
        widgets = {
            'descripcion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripcion',
                    'style': 'width: 100%',
                    'class': 'form-control',
                }
            ),
            
            'producto': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%'
            }), 
            'fecha_mov': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha_mov',
                    'data-target': '#fecha_mov',
                    'data-toggle': 'datetimepicker',
                    'readonly': True,
                }
            ),
            
            'cantidad': TextInput(attrs={
                'readonly': False,
                'class': 'form-control',
            }),

        }