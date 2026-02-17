from django.db import migrations
from django.contrib.auth.models import User


def create_superuser(apps, schema_editor):
    """Crea un superusuario por defecto si no existe"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@usda.cl',
            password='admin123'
        )
        print("✅ Superusuario 'admin' creado exitosamente")
    else:
        print("ℹ️ Superusuario 'admin' ya existe")


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0010_samplingresult_incremento_aplicado_and_more'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
