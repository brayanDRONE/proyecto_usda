# 🚀 Guía de Inicio Rápido

## Configuración Inicial (5 minutos)

### Opción A: Usando Scripts Automáticos (Recomendado)

#### Windows:
```bash
# 1. Ejecutar setup backend
setup_backend.bat

# 2. En otra terminal, ejecutar setup frontend
setup_frontend.bat
```

#### Linux/Mac:
```bash
# 1. Dar permisos de ejecución
chmod +x setup_backend.sh setup_frontend.sh

# 2. Ejecutar setup backend
./setup_backend.sh

# 3. En otra terminal, ejecutar setup frontend
./setup_frontend.sh
```

### Opción B: Configuración Manual

#### 1. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell < create_test_data.py
python manage.py runserver
```

#### 2. Frontend (nueva terminal)
```bash
cd frontend
npm install
npm run dev
```

## 🎯 Primer Uso

### 1. Acceder al Sistema
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin

### 2. Crear Establecimientos (si no usaste el script)

Acceder al panel admin y crear un establecimiento:
- Nombre: "Mi Establecimiento"
- Estado: ✓ Activo
- Estado de suscripción: ACTIVE
- Fecha de expiración: (30 días en el futuro)
- Clave de licencia: "TEST-2026-001"

### 3. Crear Primera Inspección

En el frontend (http://localhost:5173):

1. Completar formulario:
   - **Exportador**: "Exportadora Ejemplo"
   - **Establecimiento**: Seleccionar de la lista
   - **Inspector SAG**: "Juan Pérez"
   - **Contraparte SAG**: "María González"
   - **Especie**: "Uva de Mesa"
   - **Número de Lote**: "LOT-2026-001"
   - **Tamaño del Lote**: 2332
   - **Tipo de Muestreo**: Normal
   - **Tipo de Despacho**: Marítimo
   - **Cantidad de Pallets**: 48

2. Clic en "Generar Muestreo"

3. Ver resultados:
   - Tamaño de muestra: 47 cajas
   - Cajas seleccionadas (ordenadas)

## 📊 Verificar Funcionamiento

### Backend funcionando correctamente:
```bash
curl http://localhost:8000/api/establishments/
```
Debe retornar JSON con lista de establecimientos.

### Frontend funcionando correctamente:
- Abrir http://localhost:5173
- Debe verse la interfaz del sistema

## 🔧 Comandos Útiles

### Backend
```bash
# Ver todas las inspecciones en DB
python manage.py shell
>>> from inspections.models import Inspection
>>> Inspection.objects.all()

# Ejecutar tests
python manage.py test

# Crear superusuario adicional
python manage.py createsuperuser
```

### Frontend
```bash
# Build de producción
npm run build

# Preview del build
npm run preview
```

## 🐛 Solución Rápida de Problemas

### ❌ "ModuleNotFoundError: No module named 'rest_framework'"
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### ❌ "Port 8000 already in use"
```bash
# Usar otro puerto
python manage.py runserver 8001
# Actualizar API_BASE_URL en frontend/src/services/api.js
```

### ❌ "CORS error en el frontend"
- Verificar que backend esté corriendo en localhost:8000
- Verificar que frontend esté corriendo en localhost:5173

### ❌ "Error: no such table: inspections_establishment"
```bash
python manage.py migrate
```

## 📖 Próximos Pasos

1. ✅ Explorar la interfaz
2. ✅ Crear múltiples inspecciones
3. ✅ Probar con diferentes tamaños de lote
4. ✅ Revisar resultados en el admin panel
5. ✅ Probar funcionalidad de suscripción expirada

## 🌟 Características a Probar

- [x] Formulario de inspección con validaciones
- [x] Cálculo automático de muestreo (2%)
- [x] Generación de números aleatorios únicos
- [x] Visualización profesional de resultados
- [x] Control de suscripciones
- [x] Pantalla de suscripción expirada
- [ ] Impresión de etiquetas (próximamente)
- [ ] Diagrama de pallets (próximamente)

## 📞 ¿Necesitas Ayuda?

- Revisar [README.md](README.md) completo
- Consultar documentación de Django: https://docs.djangoproject.com/
- Consultar documentación de React: https://react.dev/

---

**¡Listo para empezar!** 🎉
