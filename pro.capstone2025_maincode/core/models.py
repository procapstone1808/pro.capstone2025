from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse
#from .models import Propiedad
#from .forms import PropiedadForm



class SpUsuario(models.Model):
    usuario_id = models.DecimalField(
        primary_key=True,
        max_digits=11,
        decimal_places=0,
        db_column='USUARIO_ID',
        editable=False,
        auto_created=True,
    )
    rut = models.CharField(max_length=12, db_column='RUT')
    nombre = models.CharField(max_length=120, db_column='NOMBRE')
    email = models.CharField(max_length=120, db_column='EMAIL')
    telefono = models.CharField(max_length=20, db_column='TELEFONO', blank=True, null=True)
    rol = models.CharField(max_length=30, db_column='ROL')
    is_active = models.CharField(max_length=1, db_column='IS_ACTIVE', default='Y')
    pass_field = models.CharField(max_length=30, db_column='PASS')

    class Meta:
        managed = False          
        db_table = 'SP_USUARIO'  

    def __str__(self):
        return f"{self.nombre} ({self.rut})"
    

class PropiedadUpdateView (LoginRequiredMixin, UpdateView):
    #model = Propiedad
    #form_class = PropiedadForm
    template_name = 'core/propiedadform.html'
    success_url = reverse_lazy("core:propiedad_lista")

class Propiedad(models.Model):
    ESTADOS = (("draft", "Borrador"), ("published", "Publicado"))
    nombre = models.CharField(max_length=120)
    ubicacion = models.CharField(max_length=180, blank=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='propiedades/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="draft")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('core:editar-propform', args=[self.pk] )


    