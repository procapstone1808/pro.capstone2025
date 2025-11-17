import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Propiedad

count = Propiedad.objects.count()
print(f"Total propiedades en BD: {count}")
for p in Propiedad.objects.all():
    print(f"  - {p.nombre} (id={p.pk}, ubicacion={p.ubicacion})")
