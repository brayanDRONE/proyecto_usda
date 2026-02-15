# 🖨️ Guía de Configuración - Impresora Zebra

## Requisitos Previos

1. **Sistema Operativo**: Windows (requerido para win32print)
2. **Python**: Versión 3.8 o superior
3. **Impresora Zebra**: ZDesigner ZD230-203dpi ZPL u otra impresora Zebra compatible con ZPL

## Instalación

### 1. Instalar Dependencias Python

Abrir PowerShell como Administrador y ejecutar:

```powershell
pip install pywin32
```

### 2. Verificar Impresora

```powershell
# Listar impresoras instaladas
Get-Printer | Select-Object Name
```

Buscar una impresora que contenga "Zebra" o "ZDesigner" en el nombre.

## Uso del Servicio de Impresión

### Iniciar el Servicio

1. Abrir una terminal PowerShell en la carpeta del proyecto
2. Ejecutar:

```powershell
python zebra_print_service.py
```

3. El servicio se iniciará en `http://localhost:5000`

Salida esperada:
```
============================================================
🖨️  SERVICIO DE IMPRESIÓN ZEBRA - SISTEMA USDA
============================================================
✅ Servicio iniciado en http://localhost:5000
   Health check: http://localhost:5000/health
   Endpoint: POST http://localhost:5000/print

✅ Impresoras Zebra detectadas:
   - ZDesigner ZD230-203dpi ZPL

🔄 Presiona Ctrl+C para detener el servicio
============================================================
```

### Usar desde la Aplicación Web

1. **Iniciar el servicio** (`zebra_print_service.py`)
2. **Iniciar el backend** Django (`python manage.py runserver`)
3. **Iniciar el frontend** React (`npm run dev`)
4. Generar un muestreo en la aplicación
5. Hacer clic en el botón **"Etiquetas Zebra"**

El servicio imprimirá automáticamente las etiquetas con:
- Número de lote
- Números de cajas aleatorias (2 etiquetas por tira)
- Formato: 5x5 cm cada etiqueta

## Solución de Problemas

### Error: "No se pudo conectar al servicio de impresión"

**Causa**: El servicio `zebra_print_service.py` no está ejecutándose.

**Solución**:
```powershell
python zebra_print_service.py
```

### Error: "Impresora Zebra no encontrada"

**Causa**: La impresora no está instalada o no es reconocida.

**Solución**:
1. Verificar que la impresora esté conectada y encendida
2. Instalar los drivers oficiales de Zebra
3. Verificar con: `Get-Printer | Select-Object Name`
4. Si aparece con otro nombre, modificar `printer_name` en el servicio

### Error: "Este servicio solo funciona en Windows"

**Causa**: Intentando ejecutar en Linux/Mac.

**Solución**: La impresión directa a Zebra requiere Windows. Alternativas:
- Usar una máquina Windows para impresión
- Implementar un servidor de impresión en Windows accesible desde red

### Las etiquetas se imprimen en blanco

**Causa**: Configuración incorrecta de ZPL o driver.

**Solución**:
1. Imprimir etiqueta de prueba desde el driver de Windows
2. Verificar que la impresora use modo ZPL (no EPL)
3. Calibrar la impresora (consultar manual Zebra)

### Etiquetas desalineadas o cortadas

**Causa**: Tamaño de etiqueta incorrecto en configuración.

**Solución**:
1. Verificar que las etiquetas físicas sean 5cm x 5cm
2. Modificar `LABEL_MM` en `zebra_print_service.py` si usa otro tamaño
3. Ajustar DPI si la impresora no es 203 dpi

## Formato de Etiquetas

Cada tira contiene 2 etiquetas de 5x5 cm:

```
┌─────────────┬─────────────┐
│  MUESTRA    │  MUESTRA    │
│  USDA       │  USDA       │
│             │             │
│    1234     │    5678     │
│             │             │
│ LOTE: 2025  │ LOTE: 2025  │
└─────────────┴─────────────┘
```

## Configuración Avanzada

### Cambiar Puerto del Servicio

Editar `zebra_print_service.py`:

```python
if __name__ == "__main__":
    run_service(port=8080)  # Cambiar puerto
```

También actualizar en `SamplingResultView.jsx`:

```javascript
const response = await fetch('http://localhost:8080/print', {
```

### Usar Impresora con Nombre Diferente

El servicio detecta automáticamente impresoras Zebra. Si tiene nombre específico:

```python
printer_name = "Tu-Impresora-Zebra-Custom"
```

### Ajustar Tamaño de Etiquetas

Para etiquetas de 4x6 cm (por ejemplo):

```python
LABEL_MM = 40  # Ancho en mm
LABEL_H = mm_to_dots(60)  # Alto en mm
```

## API del Servicio

### Health Check

```bash
GET http://localhost:5000/health
```

Respuesta:
```json
{
  "status": "online",
  "printers": ["ZDesigner ZD230-203dpi ZPL"],
  "zebra_available": true
}
```

### Imprimir Etiquetas

```bash
POST http://localhost:5000/print
Content-Type: application/json

{
  "lote": "2025-001",
  "numeros": [1, 45, 123, 456, 789],
  "printer": "ZDesigner ZD230-203dpi ZPL"
}
```

Respuesta exitosa:
```json
{
  "success": true,
  "message": "✅ Se imprimieron 3 tiras (5 etiquetas) en 'ZDesigner ZD230-203dpi ZPL'"
}
```

Respuesta con error:
```json
{
  "success": false,
  "error": "Impresora no encontrada"
}
```

## Automatización (Opcional)

### Iniciar Servicio Automáticamente con Windows

1. Crear acceso directo a `zebra_print_service.py`
2. Mover a: `C:\Users\<Usuario>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

### Ejecutar como Servicio Windows

Usar `NSSM` (Non-Sucking Service Manager):

```powershell
# Descargar NSSM desde https://nssm.cc/
nssm install ZebraPrintService "C:\Python310\python.exe" "C:\proyecto_usda\zebra_print_service.py"
nssm start ZebraPrintService
```

## Soporte

Para problemas adicionales:
1. Verificar logs del servicio en la terminal
2. Revisar el driver de la impresora Zebra
3. Consultar documentación ZPL de Zebra
4. Verificar conectividad con `curl http://localhost:5000/health`
