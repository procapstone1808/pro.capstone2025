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




class SpPropiedad(models.Model):
    propiedad_id = models.AutoField(
        db_column='PROPIEDAD_ID',
        primary_key=True,
    )
    rol_sii = models.CharField(
        max_length=20,
        db_column='ROL_SII',
    )
    direccion = models.CharField(
        max_length=200,
        db_column='DIRECCION',
    )
    comuna = models.CharField(
        max_length=80,
        db_column='COMUNA',
    )
    region = models.CharField(
        max_length=80,
        db_column='REGION',
    )

    # TIPO: CASA / DEPTO / SITIO
    TIPO_CHOICES = [
        ('CASA', 'Casa'),
        ('DEPTO', 'Departamento'),
        ('SITIO', 'Sitio'),
    ]
    tipo = models.CharField(
        max_length=20,
        db_column='TIPO',
        choices=TIPO_CHOICES,
    )

    sup_construida_m2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column='SUP_CONSTRUIDA_M2',
        blank=True, null=True,
    )
    sup_terreno_m2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column='SUP_TERRENO_M2',
        blank=True, null=True,
    )
    dormitorios = models.IntegerField(
        db_column='DORMITORIOS',
        blank=True, null=True,
    )
    banos = models.IntegerField(
        db_column='BANOS',
        blank=True, null=True,
    )
    estacionamientos = models.IntegerField(
        db_column='ESTACIONAMIENTOS',
        blank=True, null=True,
    )

    # ESTADO: DISPONIBLE / VENDIDA / ARRENDADA  (por si después lo quieres en el form)
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('VENDIDA', 'Vendida'),
        ('ARRENDADA', 'Arrendada'),
        ('INACTIVA', 'Inactiva (oculta)'),
    ]
    estado = models.CharField(
        max_length=20,
        db_column='ESTADO',
        default='DISPONIBLE',
        choices=ESTADO_CHOICES,
        blank=True, null=True,
    )

    precio_ref_clp = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        db_column='PRECIO_REF_CLP',
        blank=True, null=True,
    )

    # IMAGEN
    imagen = models.ImageField(
        upload_to='propiedades/',
        db_column='IMAGEN',
        blank=True, null=True,
    )

    usuario = models.ForeignKey(
        'SpUsuario',                 
        db_column='USUARIO_ID',
        on_delete=models.DO_NOTHING, # no queremos borrar propiedades si se borra el usuario
        null=True,
        blank=True,
        related_name='propiedades',
    )

    class Meta:
        managed = False
        db_table = 'SP_PROPIEDAD'

    def __str__(self):
        return f"{self.rol_sii} - {self.direccion}"









