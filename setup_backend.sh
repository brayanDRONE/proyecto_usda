#!/bin/bash

echo "========================================"
echo "Sistema de Inspecciones SAG-USDA"
echo "Inicio Rápido - Backend"
echo "========================================"
echo

cd backend

echo "[1/5] Verificando entorno virtual..."
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

echo "[2/5] Activando entorno virtual..."
source venv/bin/activate

echo "[3/5] Instalando dependencias..."
pip install -r requirements.txt

echo "[4/5] Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

echo "[5/5] Creando datos de prueba..."
python manage.py shell < create_test_data.py

echo
echo "========================================"
echo "Backend listo!"
echo "========================================"
echo
echo "Para iniciar el servidor:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo
echo "Panel admin: http://localhost:8000/admin"
echo "API: http://localhost:8000/api/"
echo
