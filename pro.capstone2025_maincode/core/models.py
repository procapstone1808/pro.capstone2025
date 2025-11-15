from django.db import models
from django.urls import reverse


class SpUsuario(models.Model):
    usuario_id = models.AutoField(
        db_column='USUARIO_ID',
        primary_key=True,
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


class Propiedad(models.Model):
    ESTADOS = (
        ("published", "Publicado"),
        ("draft", "Borrador"),
    )

    nombre = models.CharField(max_length=120, db_column='NOMBRE')
    ubicacion = models.CharField(max_length=200, db_column='UBICACION')
    descripcion = models.TextField(blank=True, db_column='DESCRIPCION')
    imagen = models.ImageField(upload_to='propiedades/', blank=True, null=True)
    activo = models.CharField(max_length=10, choices=ESTADOS, default="published")
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'PROPIEDAD'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("propiedad_detail", args=[self.pk])


