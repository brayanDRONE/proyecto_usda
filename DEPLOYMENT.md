# 🚀 Guía de Despliegue - Sistema de Inspecciones SAG-USDA

## 📋 Arquitectura de Despliegue

Este proyecto requiere dos servicios independientes:
- **Frontend React + Vite** → Vercel (recomendado)
- **Backend Django** → Railway / Render / PythonAnywhere

---

## 🎨 PARTE 1: Desplegar Frontend en Vercel

### Paso 1: Preparar el proyecto

```bash
# Ya está configurado con vercel.json y variables de entorno
cd frontend
npm install
npm run build  # Verificar que compila correctamente
```

### Paso 2: Desplegar en Vercel

**Opción A: Desde GitHub (Recomendado)**

1. Ve a [vercel.com](https://vercel.com) y crea una cuenta
2. Conecta tu repositorio de GitHub
3. Selecciona el proyecto `proyecto_usda`
4. Configuración:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. **Variables de Entorno** (Settings → Environment Variables):
   ```
   VITE_API_URL = https://tu-backend.railway.app/api
   VITE_PRINT_SERVICE_URL = http://localhost:5000
   ```

6. Click en **Deploy**

**Opción B: CLI de Vercel**

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

---

## 🐍 PARTE 2: Desplegar Backend Django

### Opción A: Railway (Recomendado - Fácil)

1. Ve a [railway.app](https://railway.app) y crea una cuenta
2. Click en **New Project** → **Deploy from GitHub**
3. Selecciona el repositorio `proyecto_usda`
4. Railway detectará Django automáticamente

**Configuración:**

Crea `Procfile` en la raíz del backend:
```
web: cd backend && python manage.py migrate && gunicorn proyecto_usda.wsgi
```

Crea `railway.json` en la raíz:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && python manage.py migrate && gunicorn proyecto_usda.wsgi --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Variables de Entorno en Railway:**
```bash
DJANGO_SETTINGS_MODULE=proyecto_usda.settings
SECRET_KEY=tu-secret-key-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=*.railway.app,tu-frontend.vercel.app
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app
DATABASE_URL=postgresql://...  # Railway lo genera automáticamente
```

**Agregar PostgreSQL:**
- En Railway, click en **+ New** → **Database** → **PostgreSQL**
- Railway conectará automáticamente

**Instalar gunicorn:**
Agrega a `backend/requirements.txt`:
```
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

---

### Opción B: Render

1. Ve a [render.com](https://render.com)
2. **New** → **Web Service**
3. Conecta GitHub y selecciona el repo
4. Configuración:
   ```
   Name: usda-backend
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn proyecto_usda.wsgi:application
   ```

**Variables de Entorno:**
```
PYTHON_VERSION=3.11
SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=.render.com,.vercel.app
DATABASE_URL=postgresql://...
```

**Agregar PostgreSQL:**
- **New** → **PostgreSQL**
- Copia la `Internal Database URL` a la variable `DATABASE_URL`

---

### Opción C: PythonAnywhere (Solo Backend)

1. Crea cuenta en [pythonanywhere.com](https://pythonanywhere.com)
2. Abre Bash console
3. Clona el repo:
   ```bash
   git clone https://github.com/brayanDRONE/proyecto_usda.git
   cd proyecto_usda/backend
   ```

4. Crea virtualenv:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 usda
   pip install -r requirements.txt
   ```

5. Configura Web app:
   - **Web** → **Add new web app**
   - Manual configuration → Python 3.10
   - Virtualenv: `/home/tuusuario/.virtualenvs/usda`
   - WSGI file: apunta a `proyecto_usda/wsgi.py`

6. Variables de entorno en WSGI file

---

## 🔧 PARTE 3: Configuración de Django para Producción

### 1. Actualizar `backend/proyecto_usda/settings.py`

```python
import os
from pathlib import Path
import dj_database_url  # Instalar: pip install dj-database-url

# SECURITY
SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-secret-key-de-desarrollo')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# HOSTS
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CORS
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173'
).split(',')

CORS_ALLOW_CREDENTIALS = True

# DATABASE
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    # SQLite para desarrollo
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Whitenoise para servir archivos estáticos
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 2. Actualizar `requirements.txt`

```bash
cd backend
pip freeze > requirements.txt

# Asegúrate de incluir:
# gunicorn==21.2.0
# psycopg2-binary==2.9.9
# dj-database-url==2.1.0
# whitenoise==6.6.0
```

---

## ✅ PARTE 4: Verificación Final

### 1. Verificar Frontend
```bash
cd frontend
npm run build
npm run preview  # Probar build localmente
```

### 2. Verificar Backend
```bash
cd backend
python manage.py check --deploy
python manage.py collectstatic --no-input
```

### 3. Conectar Frontend con Backend

En Vercel, actualiza la variable de entorno:
```
VITE_API_URL = https://tu-backend.railway.app/api
```

**Redeploy** el frontend en Vercel.

---

## 🔍 URLs Finales

Después del despliegue tendrás:

- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend API**: `https://tu-backend.railway.app/api`
- **Admin Django**: `https://tu-backend.railway.app/admin`

---

## 🐛 Solución de Problemas

### CORS Errors
- Verifica `CORS_ALLOWED_ORIGINS` en Django
- Asegúrate de incluir el dominio de Vercel

### 500 Internal Server Error
- Revisa logs en Railway/Render
- Verifica que `DEBUG=False` en producción
- Ejecuta `python manage.py migrate`

### Static Files no cargan
- Ejecuta `python manage.py collectstatic`
- Verifica configuración de Whitenoise

### Base de datos no conecta
- Verifica variable `DATABASE_URL`
- Asegúrate de que PostgreSQL está corriendo

---

## 📝 Notas Importantes

1. **Servicio de Impresión Zebra**: Solo funciona localmente, no se puede desplegar en la nube
2. **Imágenes grandes**: Las imágenes de fondo están en el repo (1.9 MB total)
3. **Migrations**: Se ejecutan automáticamente en Railway con el `startCommand`

---

## 💰 Costos Estimados

- **Vercel**: Gratis (hasta 100 GB bandwidth)
- **Railway**: $5/mes (incluye PostgreSQL)
- **Render**: Gratis (con limitaciones) o $7/mes
- **PythonAnywhere**: Gratis (con limitaciones) o $5/mes

---

## 🚀 Comandos Rápidos

```bash
# Frontend - Actualizar deployment
cd frontend
git push  # Vercel redeploys automáticamente

# Backend - Actualizar deployment
cd backend
git push  # Railway redeploys automáticamente

# Ver logs
railway logs  # En Railway
# O desde dashboard de Render/PythonAnywhere
```

---

¡Listo! Tu sistema SAG-USDA estará disponible en la web 🎉
