# 🏭 Guía para Generar Instalador - Para Administradores

Esta guía es para el **administrador del sistema** que distribuirá el servicio de impresión a los establecimientos.

---

## 📋 Prerrequisitos

- Windows 10 o superior
- Python 3.8 o superior instalado
- Permisos de administrador

---

## 🚀 Generar el Instalador (Proceso Único)

### Opción 1: Script Automático (Recomendado)

Ejecute el script que genera todo automáticamente:

```powershell
cd C:\proyecto_usda
.\generar_ejecutable.ps1
```

**Qué hace el script:**
1. Verifica que Python esté instalado
2. Instala PyInstaller y dependencias
3. Compila `zebra_print_service_gui.py` a `.exe`
4. Crea carpeta `ZebraServiceInstaller` con:
   - `ServicioImpresionZebra.exe` (ejecutable standalone)
   - `INSTALAR.bat` (instalador automático)
   - `LEEME.txt` (instrucciones para usuarios)

**Tiempo estimado:** 3-5 minutos

---

### Opción 2: Proceso Manual

Si el script automático falla, siga estos pasos:

#### 1. Instalar PyInstaller

```powershell
pip install pyinstaller pillow pystray pywin32
```

#### 2. Compilar el ejecutable

```powershell
cd C:\proyecto_usda
pyinstaller --onefile --noconsole --name ServicioImpresionZebra zebra_print_service_gui.py
```

**Parámetros explicados:**
- `--onefile`: Genera un único archivo .exe (no carpeta)
- `--noconsole`: Sin ventana de consola (solo icono en bandeja)
- `--name`: Nombre del ejecutable final

#### 3. El ejecutable estará en

```
C:\proyecto_usda\dist\ServicioImpresionZebra.exe
```

---

## 📦 Crear Paquete de Distribución

### 1. Crear estructura de carpetas

```powershell
mkdir ZebraServiceInstaller
copy dist\ServicioImpresionZebra.exe ZebraServiceInstaller\
```

### 2. Crear `INSTALAR.bat`

En la carpeta `ZebraServiceInstaller`, cree un archivo `INSTALAR.bat` con este contenido:

```batch
@echo off
echo ================================================
echo   INSTALADOR - SERVICIO IMPRESION ZEBRA
echo ================================================
echo.

REM Copiar ejecutable a Archivos de Programa
set INSTALL_DIR=%ProgramFiles%\ZebraServiceUSDA
echo Instalando en: %INSTALL_DIR%
echo.

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
copy /Y ServicioImpresionZebra.exe "%INSTALL_DIR%\"

REM Crear acceso directo en Inicio
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
echo Configurando inicio automático...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%STARTUP_DIR%\ServicioImpresionZebra.lnk'); $s.TargetPath = '%INSTALL_DIR%\ServicioImpresionZebra.exe'; $s.Save()"

echo.
echo ================================================
echo   INSTALACION COMPLETADA
echo ================================================
echo.
echo El servicio se iniciará automaticamente al encender el PC.
echo.
echo Presione cualquier tecla para iniciar el servicio ahora...
pause > nul

start "" "%INSTALL_DIR%\ServicioImpresionZebra.exe"

echo.
echo Servicio iniciado. Busque el icono verde en la bandeja del sistema.
echo.
pause
```

### 3. Crear `LEEME.txt`

```
================================================
  SERVICIO DE IMPRESIÓN ZEBRA - SAG-USDA
================================================

INSTALACIÓN:
1. Ejecute "INSTALAR.bat"
2. Aparecerá un icono verde en la bandeja del sistema
3. ¡Listo! Ya puede usar el sistema web

REQUISITOS:
- Windows 10 o superior
- Impresora Zebra conectada

AYUDA:
Clic derecho en icono verde → Ver opciones
```

### 4. Comprimir en ZIP

```powershell
Compress-Archive -Path ZebraServiceInstaller -DestinationPath ZebraServiceInstaller.zip
```

---

## 📤 Distribuir a Establecimientos

### 1. Subir a servidor/nube

Opciones:
- Google Drive / OneDrive / Dropbox
- Servidor FTP de la empresa
- Email (si el ZIP es pequeño, <25MB)

### 2. Compartir enlace

Envíe a cada establecimiento:
- **Enlace de descarga** del `ZebraServiceInstaller.zip`
- **Guía de usuario**: `GUIA_USUARIO_FINAL.md`

### 3. Template de email

```
Asunto: [SAG-USDA] Instalación del Servicio de Impresión

Estimado/a [NOMBRE],

Para poder utilizar el sistema SAG-USDA con impresora de etiquetas, 
siga estos sencillos pasos:

1. Descargue el instalador: [ENLACE]
2. Extraiga el archivo ZIP
3. Ejecute "INSTALAR.bat"
4. Busque el icono verde en la bandeja del sistema

Adjunto encontrará la guía completa en PDF.

Cualquier duda, no dude en contactarnos.

Saludos,
[FIRMA]
```

---

## 🧪 Probar el Instalador (Antes de Distribuir)

### Prueba en máquina limpia

**Recomendado:** Pruebe en una PC sin Python instalado para verificar que el .exe es realmente standalone.

### 1. Probar ejecución directa

```powershell
cd ZebraServiceInstaller
.\ServicioImpresionZebra.exe
```

**Verificar:**
- ✅ Aparece icono verde en bandeja
- ✅ Clic derecho → "Ver Estado" funciona
- ✅ Si tiene impresora Zebra, "Prueba de Impresión" funciona

### 2. Probar instalador automático

```powershell
.\INSTALAR.bat
```

**Verificar:**
- ✅ Se copia a `C:\Program Files\ZebraServiceUSDA\`
- ✅ Aparece acceso directo en Inicio automático
- ✅ El servicio se inicia correctamente

### 3. Probar inicio automático

1. Reinicie el PC
2. Verifique que el icono verde aparece automáticamente

---

## 🔄 Actualizar Versión

Cuando haga cambios en el código:

### 1. Actualizar código

Modifique `zebra_print_service_gui.py`:
- Actualice la constante `VERSION = "1.1"` al inicio del archivo

### 2. Recompilar

```powershell
.\generar_ejecutable.ps1
```

### 3. Redistribuir

- Genere nuevo ZIP
- Notifique a los establecimientos de la actualización

---

## 📊 Monitoreo de Instalaciones

### Llevar registro

Cree un documento para trackear:
| Establecimiento | Usuario | Email | Fecha Instalación | Versión | Estado |
|-----------------|---------|-------|-------------------|---------|--------|
| Planta Norte    | Juan    | ...   | 2026-02-15        | 1.0     | ✅     |
| Exportadora Sur | María   | ...   | 2026-02-16        | 1.0     | ⏳     |

### Verificación remota

Pida a cada establecimiento:
1. Clic derecho en icono → "Ver Estado"
2. Captura de pantalla
3. Enviar por email

---

## 🛠️ Troubleshooting de Compilación

### Error: "pyinstaller: command not found"

```powershell
pip install --upgrade pyinstaller
```

### Error: "ImportError: No module named 'pystray'"

```powershell
pip install pillow pystray
```

### El .exe es muy grande (>100 MB)

Es normal. Incluye Python completo + librerías.

Para reducir tamaño:
```powershell
pyinstaller --onefile --noconsole --exclude-module matplotlib --exclude-module numpy zebra_print_service_gui.py
```

### El antivirus bloquea el .exe

Algunos antivirus marcan .exe generados con PyInstaller como falsos positivos.

**Soluciones:**
1. Agregar excepción en el antivirus
2. Firmar digitalmente el .exe (requiere certificado de código)
3. Usar `--debug noarchive` al compilar

---

## 📝 Checklist Pre-Distribución

Antes de distribuir el instalador:

- [ ] Compilado y probado en PC sin Python
- [ ] Icono verde aparece en bandeja del sistema
- [ ] "Ver Estado" muestra información correcta
- [ ] "Prueba de Impresión" funciona con impresora Zebra
- [ ] `INSTALAR.bat` copia archivos correctamente
- [ ] Inicio automático funciona tras reiniciar
- [ ] ZIP comprimido correctamente
- [ ] Guía de usuario (`GUIA_USUARIO_FINAL.md`) incluida
- [ ] Subido a servidor/nube para descarga
- [ ] Email template preparado

---

## 💡 Mejoras Futuras (Opcionales)

### Agregar icono personalizado

1. Cree o descargue un archivo `.ico`
2. Al compilar:
   ```powershell
   pyinstaller --icon=zebra_icon.ico ...
   ```

### Crear instalador MSI profesional

Use herramientas como:
- **Inno Setup**: https://jrsoftware.org/isinfo.php
- **WiX Toolset**: https://wixtoolset.org/

### Firma digital

Para evitar advertencias de seguridad:
1. Obtenga certificado de firma de código
2. Firme el .exe con `signtool` de Windows SDK

---

## 🆘 Soporte

Si tiene problemas generando el instalador:

1. Verifique versión de Python: `python --version` (debe ser 3.8+)
2. Actualice pip: `python -m pip install --upgrade pip`
3. Reinstale PyInstaller: `pip uninstall pyinstaller; pip install pyinstaller`

---

**¡Listo para distribuir el servicio a todos los establecimientos! 🚀**
