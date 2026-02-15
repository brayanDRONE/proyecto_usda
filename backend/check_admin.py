from django.contrib.auth.models import User
from inspections.models import UserProfile

try:
    u = User.objects.get(username='admin')
    print(f'✓ Usuario encontrado: {u.username}')
    print(f'  Email: {u.email}')
    print(f'  Staff: {u.is_staff}')
    print(f'  Superuser: {u.is_superuser}')
    
    # Verificar perfil
    try:
        profile = u.profile
        print(f'✓ Perfil encontrado')
        print(f'  Role: {profile.role}')
        print(f'  Is superadmin: {profile.is_superadmin()}')
    except UserProfile.DoesNotExist:
        print('✗ NO TIENE PERFIL - Creando perfil...')
        profile = UserProfile.objects.create(
            user=u,
            role='SUPERADMIN'
        )
        print(f'✓ Perfil creado con rol: {profile.role}')
        
except User.DoesNotExist:
    print('✗ Usuario admin no existe')
