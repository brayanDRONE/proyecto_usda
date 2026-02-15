@echo off
echo ============================================================
echo   SERVICIO DE IMPRESION ZEBRA - SISTEMA USDA
echo ============================================================
echo.
echo Iniciando servicio de impresion en http://localhost:5000
echo.
echo IMPORTANTE:
echo   - Mantener esta ventana abierta mientras se usa el sistema
echo   - Presionar Ctrl+C para detener el servicio
echo   - La impresora Zebra debe estar conectada y encendida
echo.
echo ============================================================
echo.

python zebra_print_service.py

pause
