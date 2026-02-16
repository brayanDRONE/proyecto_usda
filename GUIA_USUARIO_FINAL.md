# 📦 Guía para Establecimientos - Sistema SAG-USDA

## ¿Qué necesito?

✅ PC con Windows 10 o superior  
✅ Impresora Zebra conectada (USB o red)  
✅ Internet  

**Eso es todo.** No necesita instalar Python ni saber programar.

---

## 📥 Instalación (Solo 3 pasos)

### 1️⃣ Descargar el instalador

Contacte al administrador del sistema y solicite:
- `ZebraServiceInstaller.zip`

Guarde el archivo en Descargas.

---

### 2️⃣ Extraer e instalar

1. **Haga clic derecho** en `ZebraServiceInstaller.zip`
2. Seleccione **"Extraer todo..."**
3. **Abra la carpeta** extraída
4. **Haga doble clic** en `INSTALAR.bat`
5. Si aparece advertencia de seguridad, click en **"Más información"** → **"Ejecutar de todas formas"**
6. Espere a que termine la instalación
7. Click en **cualquier tecla** para iniciar el servicio

---

### 3️⃣ Verificar instalación

Busque el **icono verde** en la bandeja del sistema (junto al reloj):

```
🟢 [icono verde con "Z"]
```

Si lo ve, **¡listo!** El servicio está funcionando.

**Hacer clic derecho en el icono** para ver opciones:
- 📊 Ver Estado → Muestra impresoras detectadas
- 📋 Ver Registro → Historial de impresiones
- 🧪 Prueba de Impresión → Imprime 3 etiquetas de prueba
- ❌ Salir → Cierra el servicio

---

## 🖥️ Usar el Sistema Web

### Acceder al sistema

1. Abra su navegador (Chrome, Edge, Firefox)
2. Vaya a la dirección que le proporcionó el administrador:
   ```
   https://su-sistema-usda.vercel.app
   ```
   *(El administrador le dará la URL exacta)*

3. Inicie sesión con su usuario y contraseña

---

### Imprimir etiquetas

1. Complete el formulario de muestreo
2. Seleccione las cajas a etiquetar
3. Click en **"Imprimir Etiquetas"**
4. El sistema detectará automáticamente su impresora
5. **¡Las etiquetas se imprimirán automáticamente!**

---

## ❓ Solución de Problemas

### ❌ "No veo el icono verde"

**Solución:**
1. Presione `Windows + R`
2. Escriba: `shell:startup`
3. Presione Enter
4. Haga doble clic en `ServicioImpresionZebra`

---

### ❌ "Error: No se detectó impresora"

**Solución:**
1. Verifique que la impresora Zebra esté **encendida**
2. Verifique que esté **conectada** (USB o red)
3. Abra **Panel de Control** → **Dispositivos e impresoras**
4. La impresora debe aparecer (ej: "ZDesigner ZD230...")
5. Si no aparece, reinstale el driver de la impresora

---

### ❌ "El sistema web dice 'Error al conectar con impresora'"

**Solución:**
1. **Haga clic derecho** en el icono verde
2. Seleccione **"Ver Estado"**
3. Verifique que diga: `Estado: 🟢 Activo`
4. Si dice "Detenido", cierre y vuelva a abrir el servicio

---

### ❌ "Las etiquetas salen en blanco"

**Solución:**
1. Verifique que la **cinta** de la impresora tenga tinta
2. Verifique que el **papel** esté cargado correctamente
3. Haga clic derecho en icono → **"Prueba de Impresión"**
4. Si la prueba funciona pero el sistema no, contacte al administrador

---

## 🔄 Actualizaciones

Cuando haya una nueva versión del servicio:

1. **Haga clic derecho** en el icono verde → **Salir**
2. Descargue el nuevo `ZebraServiceInstaller.zip`
3. Extraiga y ejecute `INSTALAR.bat` nuevamente
4. ¡Listo!

---

## 🆘 Contacto de Soporte

**Problemas técnicos:**
- Administrador del sistema: [CORREO/TELÉFONO]

**Problemas con impresora Zebra:**
- Soporte Zebra: https://www.zebra.com/support
- Teléfono: 1-800-ZEBRA (localice número de su país)

---

## ℹ️ Información Técnica (Para IT)

- **Ejecutable:** Standalone, sin dependencias externas
- **Puerto usado:** 5000 (HTTP local)
- **Ubicación instalación:** `C:\Program Files\ZebraServiceUSDA\`
- **Inicio automático:** Acceso directo en `shell:startup`
- **Sin conexión externa:** El servicio solo escucha localhost
- **Compatible con:** Windows 10/11, Server 2016+

---

## ✅ Checklist de Verificación

Antes de usar el sistema, verifique:

- [ ] Icono verde visible en bandeja del sistema
- [ ] Clic derecho → "Ver Estado" muestra impresora Zebra
- [ ] "Prueba de Impresión" imprime 3 etiquetas correctamente
- [ ] Puede acceder al sistema web desde el navegador
- [ ] Al imprimir desde el sistema web, las etiquetas se imprimen

**Si todos los puntos están ✅, está listo para usar el sistema.**

---

## 📝 Preguntas Frecuentes

### ❓ ¿El servicio consume muchos recursos?

No. Usa menos de 50 MB de RAM y 0% CPU cuando está inactivo.

### ❓ ¿Necesito tener el servicio siempre activo?

Sí. El servicio debe estar corriendo para poder imprimir desde el sistema web.

### ❓ ¿Puedo cerrar el servicio?

Sí, clic derecho → Salir. Pero no podrá imprimir hasta que lo vuelva a iniciar.

### ❓ ¿El servicio se inicia automáticamente al encender el PC?

Sí, después de ejecutar `INSTALAR.bat`, se inicia automáticamente.

### ❓ ¿Puedo usar cualquier impresora?

El sistema funciona mejor con impresoras **Zebra compatibles con ZPL** (ej: ZD230, ZD420, ZD620). Otras marcas pueden no funcionar.

### ❓ ¿Necesito estar conectado a Internet?

Sí, para acceder al sistema web. El servicio de impresión NO requiere Internet.

---

**¿Listo para empezar? ¡Siga los 3 pasos de instalación! 🚀**
