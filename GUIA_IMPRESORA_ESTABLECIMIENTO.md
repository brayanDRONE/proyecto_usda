# Guía de Instalación del Servicio de Impresión para Establecimientos

## Introducción

Este documento está diseñado para el personal técnico de cada establecimiento que utilizará el sistema SAG-USDA. **La impresora de etiquetas es un componente obligatorio** para el uso del sistema, ya que permite la impresión de etiquetas de muestreo directamente desde la aplicación web.

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│             Sistema Web (Vercel + Railway)              │
│         https://tu-sistema.vercel.app                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Internet
                     │
    ┌────────────────▼────────────────┐
    │   Establecimiento 1              │
    │   ┌──────────────────────────┐  │
    │   │ PC con Windows           │  │
    │   │ - Navegador Web          │  │
    │   │ - Servicio Impresión     │◄─┼─── localhost:5000
    │   │   (zebra_print_service)  │  │
    │   └───────────┬──────────────┘  │
    │               │                  │
    │   ┌───────────▼──────────────┐  │
    │   │ Impresora Zebra ZD230    │  │
    │   │ (USB o Red)              │  │
    │   └──────────────────────────┘  │
    └──────────────────────────────────┘

    ┌────────────────────────────────┐
    │   Establecimiento 2            │
    │   (misma configuración...)     │
    └────────────────────────────────┘
```

## Requisitos Previos

### Hardware
- **PC con Windows** (Windows 10 o superior recomendado)
- **Impresora Zebra ZD230** (o modelo compatible con ZPL)
- Cable USB o conexión de red para la impresora

### Software
- **Python 3.8 o superior**
- **Navegador web moderno** (Chrome, Edge, Firefox)

### Conexión
- **Internet** para acceder al sistema web
- La PC debe permanecer encendida durante las horas de operación

---

## Paso 1: Instalación del Driver de la Impresora

### 1.1 Descargar el Driver Zebra

1. Visita: https://www.zebra.com/us/en/support-downloads.html
2. Busca tu modelo (ejemplo: "ZD230")
3. Descarga el **Zebra ZPL Driver** para Windows
4. Ejecuta el instalador y sigue las instrucciones

### 1.2 Conectar la Impresora

**Opción A: USB**
1. Conecta la impresora al PC mediante USB
2. Enciende la impresora
3. Windows debería detectarla automáticamente
4. Verifica en `Panel de Control → Dispositivos e Impresoras`

**Opción B: Red (IP estática recomendada)**
1. Conecta la impresora al router/switch mediante Ethernet
2. Accede al panel de configuración de la impresora
3. Configura una IP estática (ejemplo: 192.168.1.100)
4. Agrega la impresora en Windows usando su IP

### 1.3 Verificar Instalación

1. Abre `Panel de Control → Dispositivos e Impresoras`
2. Busca tu impresora (ejemplo: "ZDesigner ZD230-203dpi ZPL")
3. Click derecho → `Propiedades de impresora`
4. Imprime una página de prueba

**✅ Punto de control:** Si la página de prueba imprime bien, continúa al siguiente paso.

---

## Paso 2: Instalación de Python

### 2.1 Descargar Python

1. Visita: https://www.python.org/downloads/
2. Descarga **Python 3.11** (o la versión más reciente)
3. Ejecuta el instalador

### 2.2 Configuración del Instalador

**⚠️ IMPORTANTE:** Durante la instalación:
- ✅ **Marca la casilla "Add Python to PATH"**
- Selecciona "Install Now"

### 2.3 Verificar Instalación

Abre **PowerShell** o **CMD** y ejecuta:

```powershell
python --version
```

Deberías ver algo como: `Python 3.11.0`

**✅ Punto de control:** Si ves la versión de Python, continúa.

---

## Paso 3: Descargar el Servicio de Impresión

### 3.1 Obtener el Archivo

Contacta al administrador del sistema para obtener:
- `zebra_print_service.py` (archivo principal)

O bien, descárgalo del repositorio compartido.

### 3.2 Crear Carpeta de Instalación

Crea una carpeta dedicada, por ejemplo:
```
C:\SAG-USDA-Printer\
```

Coloca el archivo `zebra_print_service.py` en esta carpeta.

---

## Paso 4: Instalar Dependencias de Python

### 4.1 Abrir PowerShell como Administrador

1. Presiona `Win + X`
2. Selecciona "Windows PowerShell (Administrador)"

### 4.2 Navegar a la Carpeta

```powershell
cd C:\SAG-USDA-Printer\
```

### 4.3 Instalar pywin32

```powershell
pip install pywin32
```

Espera a que se complete la instalación.

**✅ Punto de control:** Si ves "Successfully installed pywin32", continúa.

---

## Paso 5: Configurar el Servicio

### 5.1 Identificar el Nombre de tu Impresora

Abre PowerShell y ejecuta:

```powershell
python zebra_print_service.py
```

Verás un mensaje como:
```
Servicio de impresión Zebra iniciado en http://localhost:5000
Impresoras disponibles:
  - ZDesigner ZD230-203dpi ZPL
  - Microsoft Print to PDF
  - ...
```

**Copia el nombre exacto de tu impresora Zebra** (ejemplo: `ZDesigner ZD230-203dpi ZPL`)

### 5.2 Editar Configuración (Opcional)

Si tu impresora tiene un nombre diferente, edita `zebra_print_service.py`:

Busca la línea:
```python
printer = data.get('printer', 'ZDesigner ZD230-203dpi ZPL')
```

Reemplaza con el nombre de tu impresora:
```python
printer = data.get('printer', 'TU-IMPRESORA-AQUI')
```

---

## Paso 6: Probar el Servicio

### 6.1 Iniciar el Servicio

En PowerShell:
```powershell
cd C:\SAG-USDA-Printer\
python zebra_print_service.py
```

Deberías ver:
```
Servicio de impresión Zebra iniciado en http://localhost:5000
```

**⚠️ Deja esta ventana abierta mientras uses el sistema.**

### 6.2 Probar desde el Navegador

Abre un navegador y visita:
```
http://localhost:5000/health
```

Deberías ver una respuesta JSON:
```json
{
  "status": "online",
  "printers_available": ["ZDesigner ZD230-203dpi ZPL", ...],
  "zebra_available": true
}
```

**✅ Punto de control:** Si `zebra_available: true`, el servicio está funcionando.

### 6.3 Probar Impresión de Prueba

En PowerShell (en una ventana NUEVA):
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/print" -Method Post -ContentType "application/json" -Body '{"lote":"TEST001","numeros":[1,2,3],"printer":"ZDesigner ZD230-203dpi ZPL"}'
```

**Actualiza el nombre de impresora si es diferente.**

La impresora debería imprimir 3 etiquetas con "TEST001" y números 1, 2, 3.

**✅ Punto de control:** Si imprime las etiquetas, ¡todo está funcionando!

---

## Paso 7: Configurar Inicio Automático

Para evitar iniciar el servicio manualmente cada vez:

### 7.1 Crear Script de Inicio

Crea un archivo `iniciar_servicio.bat` en `C:\SAG-USDA-Printer\`:

```batch
@echo off
cd /d C:\SAG-USDA-Printer\
python zebra_print_service.py
pause
```

### 7.2 Crear Acceso Directo en Inicio

1. Presiona `Win + R` y escribe: `shell:startup`
2. Presiona Enter (se abre la carpeta de inicio)
3. Arrastra `iniciar_servicio.bat` a esta carpeta (crear acceso directo)

Ahora el servicio se iniciará automáticamente al encender el PC.

### 7.3 Opción Avanzada: Servicio de Windows

Para configurarlo como servicio de Windows (requiere conocimientos avanzados):
1. Usa `NSSM` (Non-Sucking Service Manager)
2. Descarga desde: https://nssm.cc/download
3. Ejecuta: `nssm install ZebraPrintService`
4. Configura:
   - Path: `C:\Python311\python.exe`
   - Startup directory: `C:\SAG-USDA-Printer\`
   - Arguments: `zebra_print_service.py`

---

## Paso 8: Usar el Sistema Web

### 8.1 Acceder al Sistema

1. Abre el navegador
2. Visita: https://tu-sistema.vercel.app (URL proporcionada por el administrador)
3. Inicia sesión con tus credenciales

### 8.2 Verificar Conexión con Impresora

En el módulo de muestreo:
1. Completa un muestreo
2. Click en "Imprimir Etiquetas"
3. El sistema verificará automáticamente la conexión
4. Si la impresora está lista, mostrará ✅
5. Selecciona las cajas a imprimir
6. Click en "Confirmar Impresión"

### 8.3 Solución de Problemas durante el Uso

**"Error al conectar con impresora"**
- ✅ Verifica que el servicio esté corriendo (PowerShell abierto)
- ✅ Verifica que la impresora esté encendida
- ✅ Visita http://localhost:5000/health para confirmar

**"Impresora no disponible"**
- ✅ Verifica el nombre de la impresora en Panel de Control
- ✅ Actualiza el nombre en `zebra_print_service.py`
- ✅ Reinicia el servicio

**"Las etiquetas se imprimen incorrectamente"**
- ✅ Verifica el tamaño del papel configurado (50mm x 25mm recomendado)
- ✅ Calibra la impresora (consulta manual Zebra)
- ✅ Verifica que el modo sea ZPL, no EPL

---

## Configuración de Firewall (Si es necesario)

Si el navegador no puede conectarse a `localhost:5000`:

### Windows Defender Firewall

1. Abre `Panel de Control → Sistema y Seguridad → Firewall de Windows Defender`
2. Click en "Configuración avanzada"
3. Click en "Reglas de entrada"
4. Click en "Nueva regla..."
5. Selecciona "Puerto" → Siguiente
6. TCP, puerto específico: `5000` → Siguiente
7. Permitir la conexión → Siguiente
8. Aplica a todos los perfiles → Siguiente
9. Nombre: "SAG-USDA Printer Service" → Finalizar

---

## Mantenimiento y Soporte

### Tareas Regulares

**Diarias:**
- Verificar que el servicio esté corriendo antes de iniciar jornada
- Verificar que la impresora tenga papel y cinta suficiente

**Semanales:**
- Limpiar cabezal de impresión (consulta manual Zebra)

**Mensuales:**
- Verificar actualizaciones del sistema operativo
- Verificar actualizaciones de Python (opcional)

### Contacto de Soporte

**Problemas técnicos:**
- Administrador del sistema: [EMAIL/TELÉFONO]

**Problemas con impresora:**
- Soporte técnico Zebra: https://www.zebra.com/support

---

## Resumen de Verificación

Antes de poner en producción, verifica:

- [ ] Impresora instalada y funcionando
- [ ] Página de prueba de Windows imprime correctamente
- [ ] Python instalado (versión 3.8+)
- [ ] pywin32 instalado
- [ ] zebra_print_service.py descargado en `C:\SAG-USDA-Printer\`
- [ ] Servicio inicia correctamente
- [ ] http://localhost:5000/health responde
- [ ] Prueba de impresión manual exitosa
- [ ] Inicio automático configurado
- [ ] Sistema web accesible desde navegador
- [ ] Impresión desde sistema web funciona

---

## Apéndice A: Troubleshooting Avanzado

### Error: "Python no se reconoce como comando"

**Causa:** Python no está en PATH.

**Solución:**
1. Busca la carpeta de instalación de Python (ejemplo: `C:\Python311\`)
2. Abre "Variables de entorno del sistema"
3. Edita la variable `Path`
4. Agrega: `C:\Python311\` y `C:\Python311\Scripts\`
5. Reinicia PowerShell

### Error: "ModuleNotFoundError: No module named 'win32print'"

**Causa:** pywin32 no instalado correctamente.

**Solución:**
```powershell
pip uninstall pywin32
pip install pywin32
python -c "import win32print; print('OK')"
```

### Error: "Address already in use"

**Causa:** El puerto 5000 ya está siendo usado.

**Solución:**
```powershell
# Verificar qué proceso usa el puerto
netstat -ano | findstr :5000

# Matar el proceso (reemplaza PID con el número mostrado)
taskkill /PID [PID] /F
```

### La impresora imprime símbolos extraños

**Causa:** Modo de impresión incorrecto (EPL vs ZPL).

**Solución:**
1. Accede al panel de la impresora
2. Verifica que esté en modo ZPL
3. Resetea la impresora a configuración de fábrica
4. Reconfigura

---

## Apéndice B: Comandos Útiles

```powershell
# Verificar versión de Python
python --version

# Listar paquetes instalados
pip list

# Verificar impresoras disponibles (desde Python)
python -c "import win32print; print([x[2] for x in win32print.EnumPrinters(2)])"

# Probar servicio
Invoke-RestMethod http://localhost:5000/health

# Ver logs del servicio en tiempo real
# (ejecutar en la ventana donde corre el servicio)

# Reiniciar el servicio
# Ctrl + C en la ventana de PowerShell
# Luego: python zebra_print_service.py
```

---

## Apéndice C: Especificaciones de Etiquetas

**Tamaño recomendado:** 50mm x 25mm (2" x 1")

**Formato ZPL generado:**
```zpl
^XA
^CF0,30
^FO50,20^FDLote: [LOTE]^FS
^CF0,40
^FO50,60^FDCaja: [NUMERO]^FS
^XZ
```

**Configuración de impresora:**
- Velocidad: 4 ips (pulgadas por segundo)
- Oscuridad: 10-15 (ajustar según cinta)
- Sensor: Gap (espaciado entre etiquetas)

---

## Cambios y Versiones

**Versión 1.0** (Fecha)
- Guía inicial de instalación

---

**¿Preguntas?** Contacta al administrador del sistema.
