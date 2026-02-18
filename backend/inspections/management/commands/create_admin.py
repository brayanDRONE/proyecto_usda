"""
Comando de gestión para crear el superusuario admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inspections.models import UserProfile


class Command(BaseCommand):
    help = 'Crea el superusuario admin si no existe'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('ℹ️  El usuario admin ya existe'))
            admin_user = User.objects.get(username='admin')
            
            # Verificar perfil
            if not UserProfile.objects.filter(user=admin_user).exists():
                UserProfile.objects.create(user=admin_user, role='SUPERADMIN')
                self.stdout.write(self.style.SUCCESS('✅ Perfil SUPERADMIN creado'))
            else:
                self.stdout.write(self.style.SUCCESS('✅ Usuario admin y perfil ya configurados'))
        else:
            # Crear superusuario
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@usda.cl',
                password='admin123'
            )
            
            # Crear perfil
            UserProfile.objects.create(
                user=admin_user,
                role='SUPERADMIN'
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Superusuario admin creado exitosamente'))
            self.stdout.write(self.style.SUCCESS('   Usuario: admin'))
            self.stdout.write(self.style.SUCCESS('   Contraseña: admin123'))
