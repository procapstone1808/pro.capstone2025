import re
from django import forms
from django.core.exceptions import ValidationError
from .models import SpUsuario, Propiedad


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
        max_length=12, 
        label='RUT',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678-9',
            'autocomplete': 'username'
        })
    )
    email = forms.EmailField(
        max_length=120, 
        label='Email',
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


class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['nombre', 'ubicacion', 'descripcion', 'imagen', 'activo']
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "nombre propiedad"
            }),
            "ubicacion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "ingresar ubicacion"
            }),
            "descripcion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "descripcion propiedad"
            }),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),

        }

        error_messages = {
            "nombre": {
                "required": "El nombre de la propiedad es obligatorio.",
                "max_length": "El maximo es de 100 caracteres."
            }
            
        }
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        if len(nombre) < 5:
            raise ValidationError("El nombre debe tener al menos 5 caracteres.")
        if Propiedad.objects.filter(nombre__iexact=nombre).exists():
            raise ValidationError("Ya existe una propiedad con este nombre.")
        return nombre

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion', '')
        if len(ubicacion) < 5:
            raise ValidationError('La ubicacion es demasiado corta')
        return ubicacion

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '')
        if not descripcion or len(descripcion.strip()) < 5:
            raise ValidationError('La descripcion es obligatoria y debe tener al menos 5 caracteres')
        return descripcion

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if not imagen:
            raise ValidationError('Se requiere una imagen para la propiedad.')
        if hasattr(imagen, 'size'):
            if imagen.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError("El tamaño de la imagen no debe exceder los 5MB.")
        return imagen

    def clean(self):
        data = super().clean()
        nombre = data.get('nombre', '')
        ubicacion = data.get('ubicacion', '')
        if nombre and ubicacion and nombre.lower() == ubicacion.lower():
            self.add_error('ubicacion', "La ubicación no puede ser igual al nombre de la propiedad.")
        return data
        

# Formulario para editar propiedades (con validación que no marca duplicado el propio nombre)
class PropiedadEditForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['nombre', 'ubicacion', 'descripcion', 'imagen', 'activo']
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "nombre propiedad"
            }),
            "ubicacion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "ingresar ubicacion"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "descripcion propiedad",
                "rows": 4
            }),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

        error_messages = {
            "nombre": {
                "required": "El nombre de la propiedad es obligatorio.",
                "max_length": "El maximo es de 100 caracteres."
            }
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '')
        if len(nombre) < 5:
            raise ValidationError("El nombre debe tener al menos 5 caracteres.")
        # Al editar, excluir la instancia actual de la búsqueda de duplicados
        qs = Propiedad.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Ya existe una propiedad con este nombre.")
        return nombre

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion', '')
        if len(ubicacion) < 5:
            raise ValidationError('La ubicacion es demasiado corta')
        return ubicacion

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '')
        if descripcion and len(descripcion.strip()) < 5:
            raise ValidationError('La descripcion debe tener al menos 5 caracteres si se proporciona')
        return descripcion

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen and hasattr(imagen, 'size'):
            if imagen.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError("El tamaño de la imagen no debe exceder los 5MB.")
        return imagen

    def clean(self):
        data = super().clean()
        nombre = data.get('nombre', '')
        ubicacion = data.get('ubicacion', '')
        if nombre and ubicacion and nombre.lower() == ubicacion.lower():
            self.add_error('ubicacion', "La ubicación no puede ser igual al nombre de la propiedad.")
        return data





