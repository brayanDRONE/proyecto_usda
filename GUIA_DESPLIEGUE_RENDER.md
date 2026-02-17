# Guía de Despliegue en Render

## Paso 1: Crear cuenta en Render
1. Ve a https://render.com
2. Haz clic en "Get Started" o "Sign Up"
3. Puedes registrarte con tu cuenta de GitHub (recomendado)

## Paso 2: Conectar el repositorio
1. En el dashboard de Render, haz clic en "New +"
2. Selecciona "Blueprint" (Blueprint Instance)
3. Conecta tu cuenta de GitHub si no lo has hecho
4. Busca y selecciona el repositorio `proyecto_usda`
5. Haz clic en "Connect"

## Paso 3: Configurar variables de entorno
Render leerá el archivo `render.yaml` automáticamente, pero necesitas configurar estas variables manualmente:

1. Ve a tu servicio "usda-backend"
2. En el menú lateral, haz clic en "Environment"
3. Agrega estas variables:

```
ALLOWED_HOSTS=tu-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

**Nota:** Render generará automáticamente:
- `SECRET_KEY` (valor aleatorio seguro)
- `DATABASE_URL` (desde la base de datos PostgreSQL creada)

## Paso 4: Deploy
1. Render iniciará el despliegue automáticamente
2. El proceso toma 3-5 minutos
3. Verás los logs en tiempo real

## Paso 5: Crear superusuario
Una vez desplegado:

1. En el dashboard de Render, ve a tu servicio "usda-backend"
2. En el menú superior, haz clic en "Shell"
3. Ejecuta:
```bash
python manage.py createsuperuser
```
4. Ingresa:
   - Username: `admin`
   - Email: `admin@usda.cl`
   - Password: `admin123` (o la que prefieras)

## Paso 6: Acceder al admin
1. Tu URL será algo como: `https://usda-backend-xxxx.onrender.com`
2. Ve a: `https://usda-backend-xxxx.onrender.com/admin`
3. Inicia sesión con las credenciales creadas

## Ventajas de Render sobre Railway
- ✅ Configuración más simple (render.yaml)
- ✅ UI más intuitiva
- ✅ PostgreSQL incluido en plan free
- ✅ 750 horas gratis al mes
- ✅ Deploy automático desde GitHub
- ✅ Shell incluido para comandos Django

## Notas importantes
- El plan free de Render "duerme" después de 15 minutos de inactividad
- La primera petición después de dormir toma ~30 segundos
- Para producción real, considera el plan "Starter" ($7/mes)

## Frontend (siguiente paso)
Una vez funcione el backend, desplegaremos el frontend en:
- **Vercel** (recomendado) - Gratis, optimizado para Vite/React
- O también en Render (Web Service estático)
