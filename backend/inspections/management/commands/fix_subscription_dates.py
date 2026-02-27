"""
Management command para corregir suscripciones sin fecha de vencimiento.
Asigna 30 días desde hoy a todo establecimiento ACTIVO que no tenga fecha.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from inspections.models import Establishment


class Command(BaseCommand):
    help = 'Asigna fecha de vencimiento a establecimientos ACTIVOS sin fecha'

    def handle(self, *args, **options):
        today = timezone.now().date()
        default_expiry = today + timedelta(days=30)
        
        # Encontrar establecimientos ACTIVOS sin fecha de expiración
        establishments = Establishment.objects.filter(
            subscription_status='ACTIVE',
            subscription_expiry__isnull=True
        )
        
        count = establishments.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No hay establecimientos sin fecha de expiración.')
            )
            return
        
        # Actualizar todos
        for est in establishments:
            old_expiry = est.subscription_expiry
            est.subscription_expiry = default_expiry
            est.save()
            
            self.stdout.write(
                f'{est.planta_fruticola} ({est.license_key}): '
                f'{old_expiry} → {default_expiry}'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Actualizados {count} establecimientos con fecha de vencimiento: {default_expiry}'
            )
        )
