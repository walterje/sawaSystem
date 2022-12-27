from django import forms
from Aplicaciones.User.models import User


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese su usuario',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            raise forms.ValidationError('El usuario no existe')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese una nueva contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repite la contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned

