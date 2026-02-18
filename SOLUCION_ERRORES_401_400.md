# 🚨 SOLUCIÓN URGENTE - Errores 401 y 400 en Producción

## TU SITUACIÓN ACTUAL

**Frontend:** Desplegado en Vercel  
**Backend:** `usda-backend-9di9.onrender.com` en Render  

**Errores:**
- ❌ 401 en `/api/auth/login/` 
- ❌ 400 en `/api/admin/establishments/`

---

## ✅ SOLUCIÓN EN 3 PASOS

### PASO 1: Crear el Superusuario Admin 🔑

El error 401 es porque **no existe el usuario admin** en la base de datos de Render.

**Acción:** 

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Selecciona tu servicio `usda-backend-9di9`
3. Click en **"Shell"** (arriba a la derecha)
4. Ejecuta estos comandos:

```bash
# Aplicar migraciones (por si falta alguna)
python manage.py migrate

# ⭐ CREAR SUPERADMIN
python manage.py create_admin
```

**Resultado esperado:**
```
✅ Superusuario admin creado exitosamente
   Usuario: admin
   Contraseña: admin123
```

---

### PASO 2: Configurar CORS para Vercel 🌐

El backend NO está permitiendo requests desde tu dominio de Vercel.

**Acción:**

1. En Render → tu servicio → **"Environment"**

2. Busca la variable `CORS_ALLOWED_ORIGINS`

3. Necesitas TODOS tus dominios de Vercel:
   - Ve a Vercel → tu proyecto → Settings → Domains
   - Copia TODOS los dominios mostrados

4. **Pega esto en `CORS_ALLOWED_ORIGINS`:**
   ```
   https://TU-PROYECTO.vercel.app,https://TU-PROYECTO-git-main.vercel.app,https://TU-PROYECTO-git-main-TU-USUARIO.vercel.app
   ```

   **Ejemplo real:**
   ```
   https://proyecto-usda.vercel.app,https://proyecto-usda-git-main.vercel.app,https://proyecto-usda-git-main-brayan-drones-projects.vercel.app
   ```

5. **Agrega la misma variable `CSRF_TRUSTED_ORIGINS` con los mismos valores**

6. Click en **"Save Changes"**

7. **Espera 2-3 minutos** (Render auto-redeploya)

---

### PASO 3: Actualizar VITE_API_URL en Vercel 🔧

Verifica que tu frontend apunte al backend correcto.

**Acción:**

1. Vercel → tu proyecto → Settings → **Environment Variables**

2. Verifica que existe:
   ```
   VITE_API_URL = https://usda-backend-9di9.onrender.com
   ```

3. Si falta o está mal, agrégala/corrígela

4. **Redeploy** el frontend:
   - Vercel → Deployments → últimos 3 puntos → Redeploy

---

## 🧪 VERIFICACIÓN

Después de los 3 pasos, abre tu app de Vercel y:

1. **Intenta hacer login con:**
   - Usuario: `admin`
   - Contraseña: `admin123`

2. **Si entra correctamente:**
   - ✅ Error 401 resuelto

3. **Intenta crear un establecimiento:**
   - ✅ Error 400 debería estar resuelto

---

## 🐛 Si sigue sin funcionar

### Ver logs del backend:
1. Render → tu servicio → **"Logs"**
2. Busca mensajes de error cuando intentas crear establecimiento

### Probar la API directamente:

```bash
# 1. Login
curl -X POST https://usda-backend-9di9.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Debería devolver: {"access": "TOKEN...", "refresh": "TOKEN..."}
```

Si ves el token → Login funciona ✅  
Si ves error → El superadmin no se creó correctamente

---

## 📋 Checklist Rápido

Marca cuando completes cada paso:

- [ ] Ejecuté `python manage.py create_admin` en Shell de Render
- [ ] Actualicé `CORS_ALLOWED_ORIGINS` con TODOS los dominios de Vercel
- [ ] Actualicé `CSRF_TRUSTED_ORIGINS` con los mismos dominios
- [ ] Esperé 2-3 minutos para que Render redeploy
- [ ] Verifiqué `VITE_API_URL` en Vercel
- [ ] Probé login con admin/admin123
- [ ] Probé crear un establecimiento

---

## 🎯 Dominios que necesitas configurar

**Copia los dominios exactos desde Vercel:**

1. Ve a: https://vercel.com/tu-usuario/tu-proyecto/settings/domains
2. Copia cada dominio listado
3. Únelos con comas en `CORS_ALLOWED_ORIGINS`

**Ejemplo de cómo se ve:**
```
Production: proyecto-usda.vercel.app
Git Branch: proyecto-usda-git-main.vercel.app  
Git Branch: proyecto-usda-git-main-brayan-drones-projects.vercel.app
```

**Entonces configuras:**
```
CORS_ALLOWED_ORIGINS=https://proyecto-usda.vercel.app,https://proyecto-usda-git-main.vercel.app,https://proyecto-usda-git-main-brayan-drones-projects.vercel.app
```

---

💡 **¿Necesitas ayuda?** Comparte:
- Los logs de Render (Settings → Logs)
- Los dominios exactos de Vercel
- Captura de pantalla de las variables de entorno en Render
