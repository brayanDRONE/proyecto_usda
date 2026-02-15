"""
Script para crear datos de prueba en el sistema.
Ejecutar con: python manage.py shell < create_test_data.py
"""

from inspections.models import Establishment
from django.utils import timezone
from datetime import timedelta

# Crear establecimientos de prueba
establishments_data = [
    {
        'name': 'Exportadora Frutas del Valle',
        'is_active': True,
        'subscription_status': 'ACTIVE',
        'subscription_expiry': timezone.now().date() + timedelta(days=30),
        'license_key': 'FDV-2026-ACTIVE-001'
    },
    {
        'name': 'Packing Santa Rosa',
        'is_active': True,
        'subscription_status': 'ACTIVE',
        'subscription_expiry': timezone.now().date() + timedelta(days=60),
        'license_key': 'PSR-2026-ACTIVE-002'
    },
    {
        'name': 'Agrícola Los Andes (EXPIRADO)',
        'is_active': True,
        'subscription_status': 'EXPIRED',
        'subscription_expiry': timezone.now().date() - timedelta(days=10),
        'license_key': 'ALA-2026-EXPIRED-003'
    }
]

print("Creando establecimientos de prueba...")

for data in establishments_data:
    establishment, created = Establishment.objects.get_or_create(
        license_key=data['license_key'],
        defaults=data
    )
    if created:
        print(f"✓ Creado: {establishment.name}")
    else:
        print(f"- Ya existe: {establishment.name}")

print("\n=== Datos de prueba creados exitosamente ===")
print(f"\nTotal de establecimientos: {Establishment.objects.count()}")
print(f"Activos: {Establishment.objects.filter(subscription_status='ACTIVE').count()}")
print(f"Expirados: {Establishment.objects.filter(subscription_status='EXPIRED').count()}")
