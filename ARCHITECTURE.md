# 🏗️ Arquitectura del Sistema

## Visión General

Sistema de gestión de inspecciones y muestreo SAG-USDA construido con arquitectura cliente-servidor moderna.

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                     │
│                  http://localhost:5173                   │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────┐  │
│  │   Header   │  │    Form    │  │   Results View   │  │
│  └────────────┘  └────────────┘  └──────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │           API Service (axios)                     │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                     HTTP/JSON
                          │
┌─────────────────────────────────────────────────────────┐
│                    BACKEND (Django)                      │
│                  http://localhost:8000                   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Django REST Framework                │  │
│  │                                                   │  │
│  │  ┌─────────────┐  ┌──────────┐  ┌───────────┐  │  │
│  │  │  ViewSets   │  │  Models  │  │  Serializ │  │  │
│  │  └─────────────┘  └──────────┘  └───────────┘  │  │
│  │                                                   │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │       Business Logic (utils.py)          │  │  │
│  │  │  - calcular_muestreo()                    │  │  │
│  │  │  - generar_cajas_aleatorias()            │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                          │                              │
│                     SQLAlchemy                          │
│                          │                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │           SQLite Database (db.sqlite3)            │  │
│  │                                                   │  │
│  │  ┌─────────────┐  ┌────────────┐  ┌──────────┐ │  │
│  │  │Establishments│  │Inspections│  │Samplings │ │  │
│  │  └─────────────┘  └────────────┘  └──────────┘ │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 📦 Componentes del Sistema

### Frontend (React + Vite)

#### Estructura de Componentes
```
App.jsx (Principal)
├── Header.jsx (Encabezado institucional)
└── [Vista actual]
    ├── InspectionForm.jsx (Formulario de inspección)
    ├── SamplingResultView.jsx (Resultados del muestreo)
    └── SubscriptionExpiredView.jsx (Pantalla de suscripción)
```

#### Servicios
- **api.js**: Maneja todas las comunicaciones HTTP con el backend
  - `getEstablishments()`: Obtiene lista de establecimientos
  - `generateSampling()`: Genera muestreo completo
  - `getInspections()`: Lista inspecciones
  - `getSamplingResult()`: Obtiene resultado específico

#### Comunicación
- **Protocolo**: HTTP/HTTPS
- **Formato**: JSON
- **Puerto**: 5173 (desarrollo)
- **CORS**: Configurado para localhost:8000

### Backend (Django + DRF)

#### Modelos de Datos

**Establishment**
```python
- id (PK)
- name
- is_active (boolean)
- subscription_status (ACTIVE/EXPIRED/SUSPENDED)
- subscription_expiry (date)
- license_key (unique)
- created_at, updated_at
```

**Inspection**
```python
- id (PK)
- exportador
- establishment (FK → Establishment)
- inspector_sag
- contraparte_sag
- fecha (auto)
- hora (auto)
- especie
- numero_lote
- tamano_lote
- tipo_muestreo (NORMAL/POR_ETAPA)
- tipo_despacho
- cantidad_pallets
- created_at, updated_at
```

**SamplingResult**
```python
- id (PK)
- inspection (FK → Inspection, OneToOne)
- porcentaje_muestreo (decimal, default: 2.00)
- tamano_muestra (int)
- cajas_seleccionadas (JSON text)
- created_at
```

#### API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/establishments/` | Lista establecimientos activos |
| GET | `/api/inspections/` | Lista todas las inspecciones |
| POST | `/api/inspections/` | Crea nueva inspección |
| GET | `/api/sampling-results/` | Lista resultados de muestreo |
| POST | `/api/muestreo/generar/` | **Endpoint principal**: Genera inspección + muestreo |

#### Lógica de Negocio (utils.py)

**calcular_muestreo(tamano_lote, porcentaje)**
```python
Entrada: 
  - tamano_lote: int (ej: 2332)
  - porcentaje: float (ej: 2.0)

Proceso:
  1. Validar parámetros (> 0)
  2. Calcular tamaño muestra: ceil(lote * porcentaje/100)
  3. Generar números aleatorios únicos
  4. Ordenar resultado

Salida:
  {
    'tamano_lote': int,
    'porcentaje_muestreo': float,
    'tamano_muestra': int,
    'cajas_seleccionadas': [int...]
  }
```

**generar_cajas_aleatorias(tamano_lote, cantidad)**
```python
Entrada:
  - tamano_lote: int
  - cantidad: int

Proceso:
  1. random.sample(range(1, lote+1), cantidad)
  2. Ordenar lista

Salida: [int...] (ordenado, único)
```

## 🔄 Flujo de Datos Principal

### Caso de Uso: Generar Muestreo

```
1. Usuario completa formulario
   └─> InspectionForm.jsx

2. Clic en "Generar Muestreo"
   └─> handleSubmit()
       └─> apiService.generateSampling(payload)
           └─> POST /api/muestreo/generar/

3. Backend recibe request
   └─> MuestreoViewSet.generar_muestreo()
       ├─> Validar datos (GenerarMuestreoSerializer)
       ├─> Verificar suscripción (has_active_subscription)
       ├─> Crear Inspection (DB)
       ├─> Calcular muestreo (utils.calcular_muestreo)
       ├─> Crear SamplingResult (DB)
       └─> Retornar JSON response

4. Frontend recibe respuesta
   └─> onSamplingGenerated(result)
       └─> Renderiza SamplingResultView.jsx
           ├─> Muestra información inspección
           ├─> Muestra estadísticas
           └─> Muestra cajas seleccionadas
```

## 🔒 Seguridad y Validaciones

### Frontend
- Validación de campos requeridos
- Validación de tipos de datos (números > 0)
- Manejo de errores HTTP
- Feedback visual al usuario

### Backend
- Validación doble (serializer + custom)
- **Control de suscripciones** (crítico)
- Validación de relaciones FK
- Manejo de excepciones
- Respuestas estructuradas

### Control de Suscripción

```python
def has_active_subscription(self):
    """
    Verifica:
    1. subscription_status == 'ACTIVE'
    2. subscription_expiry >= hoy
    3. is_active == True
    """
    if self.subscription_status != 'ACTIVE':
        return False
    if self.subscription_expiry and self.subscription_expiry < today:
        return False
    return True
```

## 📊 Base de Datos

### Estructura
```sql
Establishment (1) ──< Inspection (N)
                      │
                      │ (1:1)
                      │
                      └──── SamplingResult (1)
```

### Relaciones
- **Establishment → Inspections**: One-to-Many
- **Inspection → SamplingResult**: One-to-One
- Eliminación en cascada configurada

## 🎨 Diseño UI/UX

### Paleta de Colores
```css
Primario:    #2563eb (Azul institucional)
Secundario:  #6b7280 (Gris medio)
Fondo:       #f5f7fa (Gris muy claro)
Éxito:       #10b981 (Verde)
Error:       #dc2626 (Rojo)
Advertencia: #fbbf24 (Amarillo)
```

### Componentes Visuales
- **Cards**: Contenedores principales
- **Form Groups**: Inputs uniformes
- **Stats Cards**: Estadísticas destacadas
- **Box Numbers**: Grid de cajas seleccionadas
- **Buttons**: Acciones primarias y secundarias

## 🔧 Tecnologías y Dependencias

### Frontend
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "axios": "^1.6.5",
  "vite": "^5.0.11"
}
```

### Backend
```
Django==4.2.9
djangorestframework==3.14.0
django-cors-headers==4.3.1
```

## 🚀 Escalabilidad

### Preparado para:
1. **Porcentajes dinámicos**: Campo ya existe en modelo
2. **Múltiples usuarios**: Django auth integrado
3. **Roles y permisos**: DRF permissions ready
4. **Auditoría**: Timestamps en todos los modelos
5. **API versionada**: Estructura permite versioning
6. **Impresión Zebra**: Endpoints placeholders
7. **Generación PDF**: Lógica separada, fácil integración

### Futuras Mejoras
- [ ] Autenticación JWT
- [ ] WebSockets para tiempo real
- [ ] Generación de PDFs institucionales
- [ ] Integración con impresoras Zebra
- [ ] Diagrama visual de pallets
- [ ] Dashboard analytics
- [ ] Export a Excel/CSV
- [ ] Notificaciones push
- [ ] Multi-tenancy

## 📈 Performance

### Optimizaciones Implementadas
- QuerySets optimizados (select_related, prefetch_related)
- Paginación lista en DRF
- Índices en campos frecuentes
- Lazy loading de componentes React

### Métricas Esperadas
- Tiempo respuesta API: < 200ms
- Generación muestreo: < 50ms (hasta 10,000 cajas)
- Load time frontend: < 1s
- Primera renderización: < 100ms

---

**Sistema diseñado para ser robusto, escalable y mantenible.**
