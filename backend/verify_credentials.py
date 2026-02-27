"""Script para verificar credenciales"""
from django.contrib.auth.models import User

# Usuarios para verificar
usuarios_test = [
    ('admin', 'admin123'),
    ('Geofrut', 'geofrut2024'),
    ('Tuniche', 'pass'),
]

print("=" * 60)
print("VERIFICACIÓN DE CREDENCIALES")
print("=" * 60)

for username, password in usuarios_test:
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            print(f"✅ {username} / {password} - CORRECTA")
        else:
            print(f"❌ {username} / {password} - INCORRECTA")
    except User.DoesNotExist:
        print(f"⚠️  {username} - NO EXISTE")

print("\n" + "=" * 60)
print("RESETEAR CONTRASEÑAS")
print("=" * 60)

# Preguntar si resetear
print("\n¿Deseas resetear las contraseñas? Ejecuta esto manualmente:")
print("\nfrom django.contrib.auth.models import User")
print("# Admin")
print("user = User.objects.get(username='admin')")
print("user.set_password('admin123')")
print("user.save()")
print("\n# Geofrut")
print("user = User.objects.get(username='Geofrut')")
print("user.set_password('geofrut2024')")
print("user.save()")
print("\n# Tuniche")
print("user = User.objects.get(username='Tuniche')")
print("user.set_password('tuniche2024')")
print("user.save()")
