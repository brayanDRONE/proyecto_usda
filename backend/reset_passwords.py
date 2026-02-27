"""Resetear contraseñas de usuarios"""
from django.contrib.auth.models import User

print("=" * 60)
print("RESETEANDO CONTRASEÑAS")
print("=" * 60)

# Resetear Geofrut
try:
    user = User.objects.get(username='Geofrut')
    user.set_password('geofrut2024')
    user.save()
    print("✅ Contraseña de Geofrut actualizada a: geofrut2024")
except User.DoesNotExist:
    print("❌ Usuario Geofrut no existe")

# Resetear Tuniche
try:
    user = User.objects.get(username='Tuniche')
    user.set_password('tuniche2024')
    user.save()
    print("✅ Contraseña de Tuniche actualizada a: tuniche2024")
except User.DoesNotExist:
    print("❌ Usuario Tuniche no existe")

# Verificar admin
try:
    user = User.objects.get(username='admin')
    if not user.check_password('admin123'):
        user.set_password('admin123')
        user.save()
        print("✅ Contraseña de admin actualizada a: admin123")
    else:
        print("ℹ️  Contraseña de admin ya es correcta: admin123")
except User.DoesNotExist:
    print("❌ Usuario admin no existe")

print("\n" + "=" * 60)
print("CREDENCIALES ACTUALIZADAS:")
print("=" * 60)
print("Usuario: admin       | Contraseña: admin123")
print("Usuario: Geofrut     | Contraseña: geofrut2024")
print("Usuario: Tuniche     | Contraseña: tuniche2024")
print("=" * 60)
