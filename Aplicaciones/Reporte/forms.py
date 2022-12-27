from django.forms import *
from datetime import datetime

class ReporteForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

class ReporteProductoForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        'readonly': True,
    }))

 