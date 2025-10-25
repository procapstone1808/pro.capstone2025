from django.db import models


class SpUsuario(models.Model):
    ROL_CHOICES = [('ADMIN','ADMIN'), ('CORREDOR','CORREDOR')]

    usuario_id = models.BigAutoField(primary_key=True, db_column='USUARIO_ID')
    rut        = models.CharField(max_length=12, db_column='RUT', unique=True)
    nombre     = models.CharField(max_length=120, db_column='NOMBRE')
    email      = models.EmailField(max_length=120, db_column='EMAIL', unique=True)
    telefono   = models.CharField(max_length=20, db_column='TELEFONO', blank=True, null=True)
    rol        = models.CharField(max_length=20, db_column='ROL', choices=ROL_CHOICES)
    password   = models.CharField(max_length=30, db_column='PASS')          # plano (simple)
    is_active  = models.CharField(max_length=1, db_column='IS_ACTIVE', default='Y')  # 'Y'/'N'

    class Meta:
        db_table = 'SP_USUARIO'
        managed  = False

    def __str__(self):
        return f'{self.nombre} ({self.rut})'