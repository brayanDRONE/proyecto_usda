"""
Script de prueba para verificar el servicio de impresión Zebra
"""
import requests
import json

ZEBRA_SERVICE_URL = "http://localhost:5000"

def test_health_check():
    """Verifica que el servicio esté activo."""
    print("🔍 Verificando servicio de impresión...")
    try:
        response = requests.get(f"{ZEBRA_SERVICE_URL}/health", timeout=3)
        if response.status_code == 200:
            data = response.json()
            print("✅ Servicio activo")
            print(f"   Impresoras disponibles: {', '.join(data['printers'])}")
            print(f"   Zebra disponible: {'Sí' if data['zebra_available'] else 'No'}")
            return True
        else:
            print(f"❌ Servicio respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servicio")
        print("   Asegúrese de que zebra_print_service.py esté ejecutándose")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_print_labels():
    """Prueba de impresión con datos de ejemplo."""
    print("\n🖨️  Enviando datos de prueba para impresión...")
    
    test_data = {
        "lote": "TEST-2026",
        "numeros": [1, 2, 3, 4, 5, 6],
        "printer": "ZDesigner ZD230-203dpi ZPL"
    }
    
    try:
        response = requests.post(
            f"{ZEBRA_SERVICE_URL}/print",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        result = response.json()
        
        if result.get("success"):
            print(f"✅ {result['message']}")
            return True
        else:
            print(f"❌ Error de impresión: {result.get('error', 'Desconocido')}")
            return False
            
    except Exception as e:
        print(f"❌ Error al enviar datos: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 PRUEBA DEL SERVICIO DE IMPRESIÓN ZEBRA")
    print("=" * 60)
    print()
    
    # Test 1: Health check
    if not test_health_check():
        print("\n⚠️  El servicio no está disponible. Inicie zebra_print_service.py")
        return
    
    # Test 2: Pregunta si desea imprimir prueba
    print()
    response = input("¿Desea imprimir etiquetas de prueba? (s/n): ").strip().lower()
    
    if response == 's':
        test_print_labels()
    else:
        print("⏭️  Prueba de impresión omitida")
    
    print()
    print("=" * 60)
    print("✅ Pruebas completadas")
    print("=" * 60)

if __name__ == "__main__":
    main()
