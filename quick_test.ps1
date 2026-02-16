# Script de prueba rápida - Sistema USDA
# Ejecutar: .\quick_test.ps1

Write-Host "🧪 PRUEBA RÁPIDA - Sistema USDA" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Backend
Write-Host "1️⃣  Probando Backend Django..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/admin/" -TimeoutSec 3 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host " ✅" -ForegroundColor Green
    }
} catch {
    Write-Host " ❌ No responde" -ForegroundColor Red
    Write-Host "   Solución: cd backend; venv\Scripts\activate; python manage.py runserver" -ForegroundColor Yellow
}

Start-Sleep -Milliseconds 500

# Test 2: Frontend
Write-Host "2️⃣  Probando Frontend React..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 3 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host " ✅" -ForegroundColor Green
    }
} catch {
    Write-Host " ❌ No responde" -ForegroundColor Red
    Write-Host "   Solución: cd frontend; npm run dev" -ForegroundColor Yellow
}

Start-Sleep -Milliseconds 500

# Test 3: Servicio Zebra
Write-Host "3️⃣  Probando Servicio Zebra..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 3 -UseBasicParsing
    $data = $response.Content | ConvertFrom-Json
    Write-Host " ✅" -ForegroundColor Green
    
    Write-Host "   Impresoras detectadas:" -ForegroundColor Cyan
    foreach ($printer in $data.printers_available) {
        if ($printer -match "zebra|zdesigner" -or $printer -match "zebra|zdesigner") {
            Write-Host "     • $printer " -NoNewline -ForegroundColor Green
            Write-Host "← Zebra" -ForegroundColor Yellow
        } else {
            Write-Host "     • $printer" -ForegroundColor Gray
        }
    }
    
    if ($data.zebra_available) {
        Write-Host "   ✅ Impresora Zebra lista para usar" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  No se detectó impresora Zebra" -ForegroundColor Yellow
        Write-Host "   Verifica que esté encendida y conectada" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host " ❌ No responde" -ForegroundColor Red
    Write-Host "   Solución: python zebra_print_service.py" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Resumen
$allOk = $true
try {
    Invoke-WebRequest -Uri "http://localhost:8000/admin/" -TimeoutSec 2 -UseBasicParsing | Out-Null
    Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 2 -UseBasicParsing | Out-Null
    Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 2 -UseBasicParsing | Out-Null
} catch {
    $allOk = $false
}

if ($allOk) {
    Write-Host "🎉 ¡Todo funcionando correctamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Abre tu navegador en: " -NoNewline
    Write-Host "http://localhost:5173" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  Algunos servicios no están corriendo" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para iniciar todos los servicios:" -ForegroundColor Cyan
    Write-Host "  .\start_all.ps1" -ForegroundColor White
}

Write-Host ""
