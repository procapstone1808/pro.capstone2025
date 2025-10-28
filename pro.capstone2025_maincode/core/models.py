from django.db import models


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