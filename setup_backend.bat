@echo off
echo ========================================
echo Sistema de Inspecciones SAG-USDA
echo Inicio Rapido - Backend
echo ========================================
echo.

cd backend

echo [1/5] Verificando entorno virtual...
if not exist "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
)

echo [2/5] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [3/5] Instalando dependencias...
pip install -r requirements.txt

echo [4/5] Aplicando migraciones...
python manage.py makemigrations
python manage.py migrate

echo [5/5] Creando datos de prueba...
python manage.py shell < create_test_data.py

echo.
echo ========================================
echo Backend listo!
echo ========================================
echo.
echo Para iniciar el servidor:
echo   cd backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Panel admin: http://localhost:8000/admin
echo API: http://localhost:8000/api/
echo.
pause
