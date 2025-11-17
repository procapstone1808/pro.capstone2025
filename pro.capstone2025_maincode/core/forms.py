import re
from django import forms
from django.core.exceptions import ValidationError
from .models import SpUsuario, SpPropiedad


class RegistroForm(forms.ModelForm):
    class Meta:
        model = SpUsuario
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
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(choices=[
                    ('ADMIN', 'Administrador'),
                    ('CORREDOR', 'Corredor'),],
                attrs={'class': 'form-control'}),
            'pass_field': forms.PasswordInput(attrs={'class': 'form-control'}),
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
        model = SpPropiedad

        # Todos los campos que quieres pedir (menos propiedad_id)
        fields = [
            'rol_sii',
            'direccion',
            'comuna',
            'region',
            'tipo',
            'sup_construida_m2',
            'sup_terreno_m2',
            'dormitorios',
            'banos',
            'estacionamientos',
            'estado',
            'precio_ref_clp',
            'imagen',
        ]

        labels = {
            'rol_sii': 'Rol SII',
            'direccion': 'Dirección / Nombre propiedad',
            'comuna': 'Comuna',
            'region': 'Región',
            'tipo': 'Tipo de propiedad',
            'sup_construida_m2': 'Sup. construida (m²)',
            'sup_terreno_m2': 'Sup. terreno (m²)',
            'dormitorios': 'Dormitorios',
            'banos': 'Baños',
            'estacionamientos': 'Estacionamientos',
            'estado': 'Estado',
            'precio_ref_clp': 'Precio referencia (CLP)',
            'imagen': 'Imagen',
        }

        widgets = {
            'rol_sii': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345-6'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre o dirección de la propiedad'
            }),
            'comuna': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa comuna'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Región'
            }),

            # SELECT para Casa / Depto / Sitio (usa choices del modelo)
            'tipo': forms.Select(attrs={
                'class': 'form-control',
            }),

            'sup_construida_m2': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'sup_terreno_m2': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'dormitorios': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            'banos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            'estacionamientos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),

            # SELECT para estado (usa choices del modelo: DISPONIBLE / VENDIDA / ARRENDADA)
            'estado': forms.Select(attrs={
                'class': 'form-control',
            }),

            'precio_ref_clp': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000',
                'min': '0',
            }),

            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }


    def clean_rol_sii(self):
        """Validar que no exista otra propiedad con el mismo ROL SII."""
        rol = self.cleaned_data.get('rol_sii')

        if not rol:
            return rol

        rol = rol.strip()

        qs = SpPropiedad.objects.filter(rol_sii=rol)

        # Si estamos editando, excluir la misma instancia
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("Ya existe una propiedad registrada con este Rol SII.")

        return rol










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





