# 🚀 Guía de Inicio Rápido - Sistema USDA

## Pre-requisitos

✅ Python 3.10+ instalado  
✅ Node.js 18+ instalado  
✅ Impresora Zebra conectada (USB o Red)  
✅ Git instalado  

---

## 📦 Paso 1: Clonar e Instalar (Solo primera vez)

```powershell
# Clonar el repositorio
git clone https://github.com/brayanDRONE/proyecto_usda.git
cd proyecto_usda

# --- BACKEND ---
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos y aplicar migraciones
python manage.py migrate

# Crear superusuario (admin)
python manage.py createsuperuser
# Username: admin
# Email: admin@usda.cl
# Password: (tu contraseña)

# Volver a la raíz
cd ..

# --- FRONTEND ---
cd frontend

# Instalar dependencias
npm install

# Volver a la raíz
cd ..

# --- SERVICIO ZEBRA ---
# Instalar dependencias del servicio de impresión
pip install pywin32 requests
```

---

## 🎯 Paso 2: Levantar los Servicios

Necesitas **3 terminales** abiertas simultáneamente:

### Terminal 1️⃣ - Backend Django

```powershell
cd C:\proyecto_usda\backend
venv\Scripts\activate
python manage.py runserver
```

**Verificar:** Abre `http://localhost:8000/admin` en el navegador
- Deberías ver el login del admin de Django ✅

---

### Terminal 2️⃣ - Frontend React

```powershell
cd C:\proyecto_usda\frontend
npm run dev
```

**Verificar:** Abre `http://localhost:5173` en el navegador
- Deberías ver la pantalla de login con animación 3D ✅

---

### Terminal 3️⃣ - Servicio de Impresión Zebra

```powershell
cd C:\proyecto_usda
python zebra_print_service.py
```

**Output esperado:**
```
🖨️  SERVICIO DE IMPRESIÓN ZEBRA - SISTEMA USDA
============================================
🌐 Servidor corriendo en: http://localhost:5000
👍 Listo para recibir peticiones de impresión

📋 Impresoras disponibles:
   • Microsoft Print to PDF
   • ZDesigner ZD230-203dpi ZPL  ← Tu impresora Zebra
   
✅ Impresoras Zebra detectadas:
   • ZDesigner ZD230-203dpi ZPL

Presiona Ctrl+C para detener el servicio
```

**⚠️ Si no aparece tu impresora Zebra:**
- Verifica que esté encendida y conectada
- Instala los drivers desde: https://www.zebra.com/us/en/support-downloads.html
- Ve a "Dispositivos e impresoras" en Windows para confirmar que aparece

---

## 🧪 Paso 3: Probar el Sistema Completo

### 3.1 Login

1. Abre `http://localhost:5173`
2. Credenciales por defecto:
   - **Usuario:** `admin`
   - **Password:** (la que creaste con `createsuperuser`)

---

### 3.2 Crear Inspección de Prueba

1. Click en **"Nueva Inspección"**
2. Llenar formulario:
   ```
   Número de Lote: TEST-001
   Especie: Cereza
   Cantidad de Pallets: 2
   Cajas por Pallet: 50, 50
   Tipo de Muestreo: Aleatorio
   ```
3. Click **"Calcular Muestreo"**

---

### 3.3 Configurar Diagramas de Pallets (Opcional)

1. En los resultados, click **"Configurar Diagramas"**
2. Para cada pallet:
   - Base (cajas por capa): 5
   - Cantidad de cajas: 50
   - Distribución de caras: 2, 3 (automático)
3. Click **"Guardar Configuración"**
4. Click **"Ver Diagramas"**

---

### 3.4 Probar Impresión de Etiquetas Zebra 🖨️

1. En los resultados del muestreo, busca **"Imprimir Etiquetas"**
2. Verifica el estado:
   - ✅ Verde: "Servicio Zebra disponible" → Todo OK
   - ❌ Rojo: "Servicio no disponible" → Revisar Terminal 3
3. Click **"Imprimir Etiquetas"**
4. **Resultado esperado:**
   - Las etiquetas se imprimen en la Zebra ✅
   - Mensaje: "✅ Etiquetas enviadas a impresora"

---

## 🐛 Solución de Problemas

### Problema 1: "Servicio Zebra no disponible"

**Síntomas:**
- Botón de impresión en rojo
- Mensaje: "No se pudo conectar al servicio"

**Solución:**
```powershell
# Terminal 3 - Verificar que esté corriendo
cd C:\proyecto_usda
python zebra_print_service.py
```

**Probar manualmente:**
```powershell
# Nueva terminal
cd C:\proyecto_usda
python test_zebra_service.py
```

---

### Problema 2: "Impresora Zebra no encontrada"

**Síntomas:**
- Servicio corre pero no detecta impresora
- Output: "⚠️ No se detectaron impresoras Zebra"

**Solución:**

1. **Verificar conexión:**
   ```powershell
   # Listar impresoras del sistema
   python -c "import win32print; print([p[2] for p in win32print.EnumPrinters(6)])"
   ```

2. **Instalar drivers Zebra:**
   - Descarga desde: https://www.zebra.com/us/en/support-downloads.html
   - Busca tu modelo (ej: ZD230)
   - Instala el driver ZPL

3. **Configurar impresora:**
   - Panel de Control → Dispositivos e impresoras
   - Verifica que aparezca como "ZDesigner" o "Zebra"
   - Click derecho → Propiedades → Imprimir página de prueba

---

### Problema 3: Backend no conecta con Frontend

**Síntomas:**
- Login falla
- Error CORS en consola del navegador

**Solución:**

1. **Verificar que backend esté corriendo:**
   ```powershell
   # Debería responder
   curl http://localhost:8000/api/
   ```

2. **Verificar CORS en backend:**
   ```python
   # backend/config/settings.py
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:5173",
       "http://127.0.0.1:5173",
   ]
   ```

---

### Problema 4: Error de migraciones

**Síntomas:**
- Error: "no such table"
- Backend no arranca

**Solución:**
```powershell
cd backend
venv\Scripts\activate
python manage.py migrate
python manage.py createsuperuser  # Si es necesario
```

---

## 📊 Verificación Rápida de Servicios

### Check 1: Backend
```powershell
curl http://localhost:8000/admin/
# Debería devolver HTML del admin
```

### Check 2: Frontend
```powershell
curl http://localhost:5173
# Debería devolver HTML de React
```

### Check 3: Servicio Zebra
```powershell
curl http://localhost:5000/health
# Debería devolver: {"status": "ok", "printers_available": [...]}
```

---

## 🎉 Sistema Funcionando

Cuando todo esté correcto, tendrás:

✅ **Backend Django** en http://localhost:8000  
✅ **Frontend React** en http://localhost:5173  
✅ **Servicio Zebra** en http://localhost:5000  
✅ **Impresora detectada** y lista para usar  

---

## 📝 Notas Importantes

1. **Los 3 servicios deben estar corriendo** para funcionalidad completa
2. **El servicio Zebra es opcional** - Si no lo corres, el botón de impresión estará deshabilitado pero el resto funciona
3. **Base de datos SQLite** - Los datos se guardan en `backend/db.sqlite3`
4. **Para detener servicios:** `Ctrl + C` en cada terminal

---

## 🔄 Comandos Rápidos para Uso Diario

### Levantar todo de una vez (PowerShell)

Crea un archivo `start_all.ps1`:

```powershell
# Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; venv\Scripts\activate; python manage.py runserver"

# Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

# Zebra Service
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python zebra_print_service.py"

Write-Host "✅ Todos los servicios iniciados" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Zebra: http://localhost:5000" -ForegroundColor Cyan
```

**Uso:**
```powershell
cd C:\proyecto_usda
.\start_all.ps1
```

---

## 🆘 Soporte

Si algo no funciona:

1. **Revisa los terminales** - Busca errores en rojo
2. **Verifica requisitos** - Python, Node.js, drivers Zebra
3. **Consulta logs** - Cada terminal muestra información útil
4. **Reinicia servicios** - A veces basta con `Ctrl+C` y volver a correr

---

¡Listo para producción! 🚀
