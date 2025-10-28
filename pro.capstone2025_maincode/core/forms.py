import re
from django import forms
from .models import SpUsuario

class RegistroForm(forms.ModelForm):
    class Meta:
        model = SpUsuario
        # Campos que el usuario SI llena en el registro:
        fields = ['rut', 'nombre', 'email', 'telefono', 'rol', 'pass_field']

        labels = {
            'rut': 'RUT',
            'nombre': 'Nombre',
            'email': 'Email',
            'telefono': 'Teléfono',
            'rol': 'Rol',
            'pass_field': 'Contraseña',
        }
        widgets = {
            'pass_field': forms.PasswordInput(),
        }

# Validar Login
class LoginForm(forms.Form):
    rut = forms.CharField(
        max_length=12, label='RUT',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678-9',
            'autocomplete': 'username'
        })
    )
    email = forms.EmailField(
        max_length=120, label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@dominio.cl',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu contraseña',
            'autocomplete': 'current-password'
        })
    )


# Validaciones simples
def clean_rut(self):
    rut = self.cleaned_data['rut'].strip()
    # Solo validación de formato (no calcula DV)
    if not re.match(r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$', rut):
        raise forms.ValidationError("Formato de RUT inválido. Ej: 12.345.678-9")
    return rut
        

def clean(self):
    data = super().clean()
    p1 = data.get('password') or ''
    p2 = data.get('password2') or ''
    if p1 != p2:
        self.add_error('password2', "Las contraseñas no coinciden.")
    if p1 and len(p1) < 8:
        self.add_error('password', "La contraseña debe tener al menos 8 caracteres.")
    return data

def clean_password(self):
    p = self.cleaned_data['password']
    if len(p) < 8:
        raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
    return p