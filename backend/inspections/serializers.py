"""
Serializers para la API REST.
"""
from rest_framework import serializers
from .models import Establishment, Inspection, SamplingResult


class EstablishmentSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Establishment.
    """
    has_active_subscription = serializers.SerializerMethodField()
    
    class Meta:
        model = Establishment
        fields = [
            'id', 'planta_fruticola', 'exportadora', 'is_active', 'subscription_status',
            'subscription_expiry', 'has_active_subscription'
        ]
        read_only_fields = ['id']
    
    def get_has_active_subscription(self, obj):
        return obj.has_active_subscription()


class InspectionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Inspection.
    """
    establishment_name = serializers.CharField(source='establishment.planta_fruticola', read_only=True)
    
    class Meta:
        model = Inspection
        fields = [
            'id', 'exportador', 'establishment', 'establishment_name',
            'inspector_sag', 'contraparte_sag', 'fecha', 'hora',
            'especie', 'numero_lote', 'tamano_lote', 'tipo_muestreo',
            'tipo_despacho', 'cantidad_pallets', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'fecha', 'hora']
    
    def validate_tamano_lote(self, value):
        if value <= 0:
            raise serializers.ValidationError("El tamaño del lote debe ser mayor a 0")
        return value
    
    def validate_cantidad_pallets(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad de pallets debe ser mayor a 0")
        return value


class SamplingResultSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SamplingResult.
    """
    cajas_list = serializers.SerializerMethodField()
    inspection_data = InspectionSerializer(source='inspection', read_only=True)
    
    class Meta:
        model = SamplingResult
        fields = [
            'id', 'inspection', 'inspection_data', 'porcentaje_muestreo',
            'tipo_tabla', 'nombre_tabla',
            'tamano_muestra', 'cajas_seleccionadas', 'cajas_list',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_cajas_list(self, obj):
        return obj.get_cajas_list()


class GenerarMuestreoSerializer(serializers.Serializer):
    """
    Serializer para el endpoint de generación de muestreo.
    """
    # Datos de la inspección
    exportador = serializers.CharField(max_length=255)
    establishment = serializers.IntegerField()
    inspector_sag = serializers.CharField(max_length=255)
    contraparte_sag = serializers.CharField(max_length=255)
    especie = serializers.CharField(max_length=100)
    numero_lote = serializers.CharField(max_length=100)
    tamano_lote = serializers.IntegerField(min_value=1)
    tipo_muestreo = serializers.ChoiceField(choices=['NORMAL', 'POR_ETAPA'])
    tipo_despacho = serializers.CharField(max_length=100)
    cantidad_pallets = serializers.IntegerField(min_value=1)
    
    # Parámetro opcional para porcentaje (default: 2%)
    porcentaje_muestreo = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=2.00,
        required=False
    )
    
    def validate_establishment(self, value):
        """Valida que el establecimiento exista y tenga suscripción activa."""
        try:
            establishment = Establishment.objects.get(id=value)
            if not establishment.has_active_subscription():
                raise serializers.ValidationError(
                    "El establecimiento no tiene una suscripción activa. "
                    "Contacte al administrador."
                )
            return value
        except Establishment.DoesNotExist:
            raise serializers.ValidationError("Establecimiento no encontrado")
