"""
Script para crear superadministrador y actualizar datos de prueba.
Ejecutar con: python manage.py shell < create_superadmin.py
"""

from django.contrib.auth.models import User
from inspections.models import UserProfile, Establishment, EstablishmentTheme
from datetime import timedelta
from django.utils import timezone

print("=" * 60)
print("Configurando Sistema de Administración")
print("=" * 60)
print()

# Crear superadministrador
print("[1/4] Creando superadministrador...")
superadmin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@sistema-sag.cl',
        'first_name': 'Super',
        'last_name': 'Administrador',
        'is_staff': True,
        'is_superuser': True
    }
)

if created:
    superadmin.set_password('admin123')  # Cambiar en producción
    superadmin.save()
    print("✓ Superadministrador creado")
    print(f"  Usuario: admin")
    print(f"  Password: admin123")
else:
    print("- Superadministrador ya existe")

# Crear perfil de superadministrador
if not hasattr(superadmin, 'profile'):
    UserProfile.objects.create(
        user=superadmin,
        role='SUPERADMIN'
    )
    print("✓ Perfil de superadministrador creado")
else:
    print("- Perfil ya existe")

print()

# Actualizar establecimientos existentes
print("[2/4] Actualizando establecimientos...")
establishments = Establishment.objects.all()

for est in establishments:
    # Crear usuario administrador si no existe
    if not est.admin_user:
        username = f"admin_{est.name.lower().replace(' ', '_')[:20]}"
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f"{username}@example.com",
                'first_name': est.name.split()[0],
                'last_name': 'Admin'
            }
        )
        
        if user_created:
            user.set_password('password123')  # Cambiar en producción
            user.save()
            
            # Crear perfil
            UserProfile.objects.create(
                user=user,
                role='ESTABLISHMENT_ADMIN'
            )
        
        est.admin_user = user
        est.created_by = superadmin
        
        # Asegurar que tiene subscription_start
        if not est.subscription_start:
            est.subscription_start = timezone.now().date()
        
        est.save()
        print(f"✓ Usuario creado para: {est.name} (usuario: {username})")
    else:
        print(f"- {est.name} ya tiene usuario")

print()

# Crear temas por defecto
print("[3/4] Creando temas por defecto...")
for est in establishments:
    theme, theme_created = EstablishmentTheme.objects.get_or_create(
        establishment=est,
        defaults={
            'company_name': est.name,
            'welcome_message': f'Bienvenido al sistema de inspecciones de {est.name}'
        }
    )
    
    if theme_created:
        print(f"✓ Tema creado para: {est.name}")
    else:
        print(f"- {est.name} ya tiene tema")

print()

# Resumen
print("[4/4] Resumen del sistema:")
print("=" * 60)
print(f"Total de usuarios: {User.objects.count()}")
print(f"Superadministradores: {UserProfile.objects.filter(role='SUPERADMIN').count()}")
print(f"Admin de establecimientos: {UserProfile.objects.filter(role='ESTABLISHMENT_ADMIN').count()}")
print(f"Total de establecimientos: {Establishment.objects.count()}")
print(f"  - Activos: {Establishment.objects.filter(subscription_status='ACTIVE').count()}")
print(f"  - Expirados: {Establishment.objects.filter(subscription_status='EXPIRED').count()}")
print()
print("=" * 60)
print("✓ Sistema configurado correctamente")
print("=" * 60)
print()
print("CREDENCIALES DE ACCESO:")
print("-" * 60)
print("SUPERADMINISTRADOR:")
print("  Usuario: admin")
print("  Password: admin123")
print()
print("ESTABLECIMIENTOS:")
for est in Establishment.objects.filter(admin_user__isnull=False):
    print(f"  {est.name}:")
    print(f"    Usuario: {est.admin_user.username}")
    print(f"    Password: password123")
print()
print("⚠️  IMPORTANTE: Cambiar contraseñas en producción")
print("=" * 60)
