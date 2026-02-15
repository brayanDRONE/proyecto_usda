"""
Script para verificar las especies almacenadas en la base de datos.
"""
import sys
import os
import django

# Agregar el directorio backend al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inspections.models import Inspection
from inspections.utils import obtener_tipo_tabla_muestreo

# Mostrar las últimas 5 inspecciones
inspecciones = Inspection.objects.all().order_by('-created_at')[:5]

print("=" * 80)
print("ÚLTIMAS INSPECCIONES Y SUS ESPECIES")
print("=" * 80)

for insp in inspecciones:
    print(f"\nID: {insp.id}")
    print(f"Lote: {insp.numero_lote}")
    print(f"Especie: '{insp.especie}'")
    print(f"Tipo tabla detectado: {obtener_tipo_tabla_muestreo(insp.especie)}")
    
    if hasattr(insp, 'sampling_result'):
        print(f"Tabla aplicada: {insp.sampling_result.nombre_tabla}")
        print(f"Tamaño muestra: {insp.sampling_result.tamano_muestra}")
    else:
        print("Sin resultado de muestreo")
    print("-" * 80)

print("\n" + "=" * 80)
print("PRUEBA DE DETECCIÓN CON 'durazno' (minúscula)")
print("=" * 80)
print(f"Tipo tabla para 'durazno': {obtener_tipo_tabla_muestreo('durazno')}")
print(f"Tipo tabla para 'Durazno': {obtener_tipo_tabla_muestreo('Durazno')}")
print(f"Tipo tabla para 'DURAZNO': {obtener_tipo_tabla_muestreo('DURAZNO')}")
print(f"Tipo tabla para 'duraznos': {obtener_tipo_tabla_muestreo('duraznos')}")
print(f"Tipo tabla para 'Duraznos': {obtener_tipo_tabla_muestreo('Duraznos')}")
print(f"\nTipo tabla para 'cerezas': {obtener_tipo_tabla_muestreo('cerezas')}")
print(f"Tipo tabla para 'Cerezas': {obtener_tipo_tabla_muestreo('Cerezas')}")
print(f"Tipo tabla para 'Cereza': {obtener_tipo_tabla_muestreo('Cereza')}")

