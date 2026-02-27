"""Verificación final"""
from django.contrib.auth.models import User

usuarios_test = [
    ('admin', 'admin123'),
    ('Geofrut', 'geofrut2024'),
    ('Tuniche', 'tuniche2024'),
]

print("=" * 60)
print("VERIFICACIÓN FINAL DE CREDENCIALES")
print("=" * 60)

for username, password in usuarios_test:
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            print(f"✅ {username:15} / {password:15} - CORRECTA")
        else:
            print(f"❌ {username:15} / {password:15} - INCORRECTA")
    except User.DoesNotExist:
        print(f"⚠️  {username:15} - NO EXISTE")

print("=" * 60)
