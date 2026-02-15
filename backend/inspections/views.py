"""
Vistas para la API REST.
"""
import json
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Establishment, Inspection, SamplingResult, EstablishmentTheme
from .serializers import (
    EstablishmentSerializer,
    InspectionSerializer,
    SamplingResultSerializer,
    GenerarMuestreoSerializer
)
from .serializers_admin import EstablishmentThemeSerializer
from .utils import calcular_muestreo


class EstablishmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar establecimientos.
    Solo lectura desde el frontend.
    """
    queryset = Establishment.objects.filter(is_active=True)
    serializer_class = EstablishmentSerializer


class InspectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar inspecciones.
    """
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    
    def perform_create(self, serializer):
        """Valida suscripción antes de crear inspección."""
        establishment = serializer.validated_data.get('establishment')
        if not establishment.has_active_subscription():
            raise serializers.ValidationError({
                'establishment': 'El establecimiento no tiene una suscripción activa.'
            })
        serializer.save()


class SamplingResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar resultados de muestreo.
    Solo lectura.
    """
    queryset = SamplingResult.objects.all()
    serializer_class = SamplingResultSerializer


class MuestreoViewSet(viewsets.ViewSet):
    """
    ViewSet personalizado para generar muestreos.
    """
    
    @action(detail=False, methods=['post'], url_path='generar')
    def generar_muestreo(self, request):
        """
        Endpoint: POST /api/muestreo/generar/
        
        Crea una inspección y genera el muestreo automáticamente.
        
        Request Body:
        {
            "exportador": "string",
            "establishment": int,
            "inspector_sag": "string",
            "contraparte_sag": "string",
            "especie": "string",
            "numero_lote": "string",
            "tamano_lote": int,
            "tipo_muestreo": "NORMAL|POR_ETAPA",
            "tipo_despacho": "string",
            "cantidad_pallets": int,
            "porcentaje_muestreo": float (opcional, default: 2.0)
        }
        
        Response:
        {
            "success": true,
            "message": "Muestreo generado exitosamente",
            "data": {
                "inspection": {...},
                "sampling_result": {
                    "tamano_lote": int,
                    "porcentaje_muestreo": float,
                    "tamano_muestra": int,
                    "cajas_seleccionadas": [int, int, ...]
                }
            }
        }
        """
        # Validar datos de entrada
        serializer = GenerarMuestreoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Datos inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Verificar que el establecimiento tenga suscripción activa
        establishment = get_object_or_404(Establishment, id=data['establishment'])
        if not establishment.has_active_subscription():
            return Response({
                'success': False,
                'message': 'Suscripción vencida o inactiva',
                'error': 'SUBSCRIPTION_EXPIRED',
                'details': 'El establecimiento no tiene una suscripción activa. Contacte al administrador.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            # Crear la inspección
            inspection = Inspection.objects.create(
                exportador=data['exportador'],
                establishment=establishment,
                inspector_sag=data['inspector_sag'],
                contraparte_sag=data['contraparte_sag'],
                especie=data['especie'],
                numero_lote=data['numero_lote'],
                tamano_lote=data['tamano_lote'],
                tipo_muestreo=data['tipo_muestreo'],
                tipo_despacho=data['tipo_despacho'],
                cantidad_pallets=data['cantidad_pallets']
            )
            
            # Calcular muestreo usando la especie
            resultado_muestreo = calcular_muestreo(
                tamano_lote=data['tamano_lote'],
                especie=data['especie']
            )
            
            # Guardar resultado del muestreo
            sampling_result = SamplingResult.objects.create(
                inspection=inspection,
                tipo_tabla=resultado_muestreo['tipo_tabla'],
                nombre_tabla=resultado_muestreo['nombre_tabla'],
                tamano_muestra=resultado_muestreo['tamano_muestra'],
                cajas_seleccionadas=json.dumps(resultado_muestreo['cajas_seleccionadas'])
            )
            
            # Preparar respuesta
            return Response({
                'success': True,
                'message': 'Muestreo generado exitosamente',
                'data': {
                    'inspection': InspectionSerializer(inspection).data,
                    'sampling_result': {
                        'id': sampling_result.id,
                        'tamano_lote': resultado_muestreo['tamano_lote'],
                        'tipo_tabla': resultado_muestreo['tipo_tabla'],
                        'nombre_tabla': resultado_muestreo['nombre_tabla'],
                        'tamano_muestra': resultado_muestreo['tamano_muestra'],
                        'cajas_seleccionadas': resultado_muestreo['cajas_seleccionadas']
                    }
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Error al generar el muestreo',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet público para que los establecimientos obtengan su tema.
    Solo lectura.
    """
    queryset = EstablishmentTheme.objects.all()
    serializer_class = EstablishmentThemeSerializer
    
    @action(detail=False, methods=['get'], url_path='my-theme')
    def my_theme(self, request):
        """
        Endpoint: GET /api/themes/my-theme/
        
        Retorna el tema del establecimiento del usuario autenticado.
        """
        if not request.user.is_authenticated:
            return Response({
                'error': 'Usuario no autenticado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Obtener establecimiento del usuario
        establishment = None
        if hasattr(request.user, 'establishment_admin'):
            establishment = request.user.establishment_admin
        
        if not establishment:
            return Response({
                'error': 'Usuario no tiene un establecimiento asociado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener o crear tema
        theme, created = EstablishmentTheme.objects.get_or_create(
            establishment=establishment
        )
        
        serializer = self.get_serializer(theme)
        return Response(serializer.data)
