"""Script para verificar usuarios y sus credenciales"""
from django.contrib.auth.models import User
from inspections.models import UserProfile

print("=" * 60)
print("USUARIOS EN EL SISTEMA")
print("=" * 60)

users = User.objects.all()
for user in users:
    print(f"\n👤 Usuario: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Activo: {'✅' if user.is_active else '❌'}")
    print(f"   Staff: {'✅' if user.is_staff else '❌'}")
    print(f"   Superuser: {'✅' if user.is_superuser else '❌'}")
    
    # Verificar perfil
    if hasattr(user, 'profile'):
        profile = user.profile
        print(f"   Rol: {profile.get_role_display()}")
        if profile.establishment:
            print(f"   Establecimiento: {profile.establishment.planta_fruticola}")
    else:
        print(f"   ⚠️  SIN PERFIL")
    
    # Verificar si es admin de establecimiento
    if hasattr(user, 'establishment_admin'):
        print(f"   Admin de: {user.establishment_admin.planta_fruticola}")

print("\n" + "=" * 60)
print("Para resetear contraseña de un usuario:")
print("=" * 60)
print("from django.contrib.auth.models import User")
print("user = User.objects.get(username='NOMBRE_USUARIO')")
print("user.set_password('NUEVA_CONTRASEÑA')")
print("user.save()")
print("=" * 60)
