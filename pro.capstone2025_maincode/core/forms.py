import re
from django import forms

ROLE_CHOICES = [('ADMIN', 'ADMIN'), ('CORREDOR', 'CORREDOR')]

# Validar Registro
class RegistroForm(forms.Form):
    rut = forms.CharField(
        max_length=12, label='RUT',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678-9',
            'autocomplete': 'off'
        })
    )
    nombre = forms.CharField(
        max_length=120, label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'})
    )
    email = forms.EmailField(
        max_length=120, label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@dominio.cl'})
    )
    telefono = forms.CharField(
        max_length=20, label='Teléfono', required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite la contraseña'})
    )
    rol = forms.ChoiceField(
        label='Rol', choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
        
    )

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