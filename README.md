# Sistema de Inspecciones SAG-USDA

Sistema profesional de gestión de inspecciones y muestreo para establecimientos agrícolas y packing.

---

## 📚 Inicio Rápido - Seleccione su Guía

👉 **Elija la guía según su rol:**

| Rol | Guía | Descripción |
|-----|------|-------------|
| 🧑‍💼 **Usuario Final** (Establecimiento) | [GUIA_USUARIO_FINAL.md](GUIA_USUARIO_FINAL.md) | Instalación simple del servicio de impresión |
| 👨‍💻 **Desarrollador** (Testing local) | [GUIA_INICIO_RAPIDO.md](GUIA_INICIO_RAPIDO.md) | Cómo levantar el sistema localmente |
| 🏭 **Administrador** (Distribuir servicio) | [GUIA_GENERAR_INSTALADOR.md](GUIA_GENERAR_INSTALADOR.md) | Generar ejecutable para distribución |
| 🚀 **DevOps** (Deploy producción) | [DEPLOYMENT.md](DEPLOYMENT.md) | Desplegar a Vercel + Railway |

---

## 🎯 Características

- **Captura de Datos de Inspección**: Formulario completo con validaciones
- **Cálculo Automático de Muestreo**: 2% del lote con redondeo hacia arriba
- **Generación de Cajas Aleatorias**: Selección única y ordenada
- **Exportación a PDF**: Formato oficial SAG-USDA con todos los datos
- **Impresión de Etiquetas Zebra**: Etiquetas 5x5cm con número de lote y cajas (2 por tira)
- **Visualización de Resultados**: Interface moderna y profesional
- **Control de Suscripciones**: Validación de licencias mensuales
- **API REST**: Backend robusto con Django REST Framework

## 🛠️ Tecnologías

### Backend
- Django 4.2
- Django REST Framework
- SQLite (base de datos)

### Frontend
- React 18
- Vite
- CSS Moderno

## 📋 Requisitos Previos

- Python 3.8 o superior
- Node.js 16 o superior
- npm o yarn

## 🚀 Instalación y Configuración

### 1. Backend (Django)

```bash
# Navegar a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (para acceder al admin)
python manage.py createsuperuser

# Iniciar servidor de desarrollo
python manage.py runserver
```

El backend estará disponible en: `http://localhost:8000`

### 2. Frontend (React + Vite)

```bash
# En una nueva terminal, navegar a la carpeta frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## 📊 Configuración Inicial

### Crear Establecimientos de Prueba

1. Acceder al panel de administración: `http://localhost:8000/admin`
2. Iniciar sesión con el superusuario creado
3. Crear uno o más establecimientos con:
   - Nombre del establecimiento
   - Estado: Activo
   - Estado de suscripción: ACTIVE
   - Fecha de expiración: (fecha futura)
   - Clave de licencia: (cualquier texto único)

## 🖨️ Servicio de Impresión Zebra (Opcional)

Para habilitar la impresión de etiquetas Zebra:

### Requisitos
- Windows (requerido para win32print)
- Impresora Zebra ZPL (ej: ZDesigner ZD230-203dpi)
- Python con pywin32: `pip install pywin32`

### Iniciar Servicio

**Opción 1**: Usando el archivo .bat
```bash
# Doble clic en:
start_zebra_service.bat
```

**Opción 2**: Manualmente
```bash
python zebra_print_service.py
```

El servicio se iniciará en `http://localhost:5000` y estará disponible desde la aplicación web.

📖 **Documentación completa**: Ver [ZEBRA_PRINTER_SETUP.md](ZEBRA_PRINTER_SETUP.md)

## 🎨 Estructura del Proyecto

```
proyecto_usda/
├── backend/
│   ├── config/              # Configuración Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── inspections/         # Aplicación principal
│   │   ├── models.py        # Modelos de datos
│   │   ├── serializers.py   # Serializers DRF
│   │   ├── views.py         # Vistas/Endpoints
│   │   ├── urls.py          # URLs de la app
│   │   ├── utils.py         # Lógica de muestreo
│   │   └── admin.py         # Configuración admin
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/      # Componentes React
    │   │   ├── Header.jsx
    │   │   ├── InspectionForm.jsx
    │   │   ├── SamplingResultView.jsx
    │   │   └── SubscriptionExpiredView.jsx
    │   ├── services/        # Servicios API
    │   │   └── api.js
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── vite.config.js
    └── package.json
```

## 📡 API Endpoints

### Establecimientos
- `GET /api/establishments/` - Listar establecimientos activos

### Inspecciones
- `GET /api/inspections/` - Listar inspecciones
- `POST /api/inspections/` - Crear inspección

### Muestreo
- `POST /api/muestreo/generar/` - Generar muestreo completo

**Body de ejemplo:**
```json
{
  "exportador": "Exportadora ABC",
  "establishment": 1,
  "inspector_sag": "Juan Pérez",
  "contraparte_sag": "María González",
  "especie": "Uva de Mesa",
  "numero_lote": "LOT-2026-001",
  "tamano_lote": 2332,
  "tipo_muestreo": "NORMAL",
  "tipo_despacho": "Marítimo",
  "cantidad_pallets": 48
}
```

## 🔒 Control de Suscripciones

El sistema valida automáticamente:
- Estado de suscripción (ACTIVE, EXPIRED, SUSPENDED)
- Fecha de expiración
- Estado activo del establecimiento

Si la suscripción no es válida:
- Se bloquea la generación de muestreos
- Se muestra pantalla informativa
- Se requiere contacto con administrador

## 🎯 Flujo de Uso

1. **Inicio**: Usuario accede al sistema
2. **Formulario**: Completa datos de inspección
3. **Validación**: Sistema verifica suscripción del establecimiento
4. **Cálculo**: Se genera muestreo automático (2% del lote)
5. **Resultados**: Se muestran cajas seleccionadas
6. **Acciones futuras**: Imprimir etiquetas, ver diagrama

## 🔄 Lógica de Muestreo

```python
# Ejemplo: Lote de 2332 cajas
Muestra = ceil(2332 * 0.02) = 47 cajas

# Generación de números aleatorios únicos
Rango: 1 → 2332
Cantidad: 47
Ordenamiento: Ascendente
```

## 🚀 Escalabilidad Futura

El sistema está preparado para:
- ✅ Porcentajes de muestreo dinámicos
- ✅ Diagrama visual de distribución de pallets
- ✅ Impresión automática en impresoras Zebra
- ✅ Generación de PDF institucional
- ✅ Sistema de auditoría e historial
- ✅ Múltiples usuarios y roles

## 🎨 Diseño UI/UX

- **Estilo**: Profesional e institucional
- **Layout**: Dashboard moderno con cards
- **Colores**: Azul institucional, grises sobrios
- **Tipografía**: Inter/Roboto, clara y legible
- **Responsive**: Adaptable a diferentes pantallas

## 📝 Comandos Útiles

### Backend
```bash
# Crear nueva migración
python manage.py makemigrations

# Ver SQL de migración
python manage.py sqlmigrate inspections 0001

# Abrir shell Django
python manage.py shell

# Crear datos de prueba
python manage.py shell < create_test_data.py
```

### Frontend
```bash
# Build para producción
npm run build

# Preview del build
npm run preview
```

## � Flujo de Trabajo Completo

### Iniciar el Sistema

1. **Backend Django** (terminal 1):
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Frontend React** (terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Servicio Zebra** (terminal 3, opcional):
   ```bash
   python zebra_print_service.py
   # O doble clic en: start_zebra_service.bat
   ```

### Generar Muestreo e Imprimir

1. Acceder a la aplicación: `http://localhost:5173`
2. Completar formulario de inspección:
   - Seleccionar establecimiento
   - Ingresar datos del lote
   - Especificar tipo de despacho
3. Hacer clic en "Generar Muestreo"
4. En la pantalla de resultados:
   - **Imprimir PDF**: Descarga reporte oficial SAG-USDA
   - **Etiquetas Zebra**: Imprime etiquetas automáticamente (requiere servicio activo)
   - **Nueva Inspección**: Generar otro muestreo

## �🐛 Solución de Problemas

### Error de CORS
- Verificar que el frontend esté en `localhost:5173`
- Revisar configuración en `backend/config/settings.py`

### Error de base de datos
```bash
# Eliminar base de datos y recrear
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Puerto ocupado
- Backend: Cambiar puerto con `python manage.py runserver 8001`
- Frontend: Cambiar en `vite.config.js`

### Error: "No se pudo conectar al servicio de impresión"
- Verificar que `zebra_print_service.py` esté ejecutándose
- El servicio debe estar en `http://localhost:5000`
- Ver documentación completa en [ZEBRA_PRINTER_SETUP.md](ZEBRA_PRINTER_SETUP.md)

### Impresora Zebra no detectada
```bash
# Verificar impresoras instaladas (PowerShell)
Get-Printer | Select-Object Name
```
- Instalar drivers oficiales de Zebra
- Conectar y encender la impresora antes de iniciar el servicio

---

## 🌐 Arquitectura Multi-Establecimiento (Producción)

Este sistema está diseñado para funcionar como **SaaS multi-tenant**:

```
┌─────────────────────────────────────────┐
│  SISTEMA WEB (Vercel + Railway)         │
│  - Admin central gestiona usuarios      │
│  - Backend API con PostgreSQL           │
└──────────────┬──────────────────────────┘
               │ Internet
    ┌──────────┴─────────┬────────────┬─────────────
    │                    │            │
    ▼                    ▼            ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Establ. 1   │  │ Establ. 2   │  │ Establ. N   │
│ PC + Zebra  │  │ PC + Zebra  │  │ PC + Zebra  │
│ + Servicio  │  │ + Servicio  │  │ + Servicio  │
└─────────────┘  └─────────────┘  └─────────────┘
```

### Para Usuarios Finales

Cada establecimiento necesita:
1. **PC con Windows** + Internet
2. **Impresora Zebra** conectada
3. **Instalador simple**: Ejecutar `INSTALAR.bat` (ver [GUIA_USUARIO_FINAL.md](GUIA_USUARIO_FINAL.md))
4. **Acceso web**: Navegar a su URL asignada

**No requiere conocimientos técnicos** - El instalador configura todo automáticamente.

### Para Administradores

Distribución del servicio de impresión:
1. Generar ejecutable con [GUIA_GENERAR_INSTALADOR.md](GUIA_GENERAR_INSTALADOR.md)
2. Compartir `ZebraServiceInstaller.zip` con cada establecimiento
3. Los usuarios ejecutan `INSTALAR.bat` → Listo

### Para Desarrolladores

- **Local**: Seguir [GUIA_INICIO_RAPIDO.md](GUIA_INICIO_RAPIDO.md)
- **Producción**: Seguir [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📄 Licencia

Sistema desarrollado para uso interno en establecimientos agrícolas.

## 👥 Soporte

Para soporte técnico o consultas, contactar al administrador del sistema.

---

**Sistema de Inspecciones SAG-USDA** - Versión 1.0.0 - 2026
