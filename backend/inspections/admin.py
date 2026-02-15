from django.contrib import admin
from .models import Establishment, Inspection, SamplingResult, EstablishmentTheme, UserProfile


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ['planta_fruticola', 'rut', 'admin_user', 'subscription_status', 'subscription_expiry', 'is_active']
    list_filter = ['subscription_status', 'is_active', 'created_at']
    search_fields = ['planta_fruticola', 'exportadora', 'rut', 'license_key', 'email']
    readonly_fields = ['license_key', 'created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('exportadora', 'planta_fruticola', 'rut', 'address', 'phone', 'email', 'encargado_sag')
        }),
        ('Usuario Administrador', {
            'fields': ('admin_user',)
        }),
        ('Suscripción', {
            'fields': ('subscription_status', 'subscription_start', 'subscription_expiry', 'license_key', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ['numero_lote', 'exportador', 'establishment', 'fecha', 'especie', 'tamano_lote']
    list_filter = ['tipo_muestreo', 'especie', 'fecha', 'tipo_despacho']
    search_fields = ['numero_lote', 'exportador', 'inspector_sag']
    date_hierarchy = 'fecha'
    readonly_fields = ['fecha', 'hora', 'created_at', 'updated_at']


@admin.register(SamplingResult)
class SamplingResultAdmin(admin.ModelAdmin):
    list_display = ['inspection', 'nombre_tabla', 'tamano_muestra', 'created_at']
    list_filter = ['created_at', 'tipo_tabla', 'nombre_tabla']
    search_fields = ['inspection__numero_lote', 'inspection__especie']
    readonly_fields = ['created_at']


@admin.register(EstablishmentTheme)
class EstablishmentThemeAdmin(admin.ModelAdmin):
    list_display = ['establishment', 'primary_color', 'show_logo', 'dark_mode']
    search_fields = ['establishment__planta_fruticola', 'establishment__exportadora']
    
    fieldsets = (
        ('Establecimiento', {
            'fields': ('establishment',)
        }),
        ('Colores', {
            'fields': ('primary_color', 'secondary_color', 'accent_color')
        }),
        ('Logos e Imágenes', {
            'fields': ('logo', 'logo_dark', 'favicon', 'show_logo')
        }),
        ('Textos Personalizados', {
            'fields': ('company_name', 'welcome_message', 'footer_text')
        }),
        ('Configuración', {
            'fields': ('dark_mode',)
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
