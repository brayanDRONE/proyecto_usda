@echo off
echo ========================================
echo Sistema de Inspecciones SAG-USDA
echo Inicio Rapido - Frontend
echo ========================================
echo.

cd frontend

echo [1/2] Instalando dependencias...
call npm install

echo.
echo ========================================
echo Frontend listo!
echo ========================================
echo.
echo Para iniciar el servidor:
echo   cd frontend
echo   npm run dev
echo.
echo Aplicacion: http://localhost:5173
echo.
pause
