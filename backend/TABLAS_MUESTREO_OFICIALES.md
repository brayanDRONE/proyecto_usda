# 📊 TABLAS DE MUESTREO OFICIALES SAG-USDA

Implementación de las especificaciones oficiales SAG-USDA para el cálculo de tamaño de muestra.

---

## 🔬 HIPERGEOMÉTRICA 3% (3% infestación - 95% confianza)

**Especie:** Damasco (sin frío autorizado)

| Tamaño Lote | Tamaño Muestra |
|-------------|----------------|
| 1 – 900 | Todas |
| 901 – 1.500 | 63 |
| 1.501 – 4.000 | 90 |
| 4.001 – 10.000 | 94 |
| 10.001 – 15.000 | 96 |
| 15.001 – 20.000 | 98 |
| > 20.000 | 99 |

---

## 🍑 HIPERGEOMÉTRICA 6% (6% infestación - 95% confianza)

**Especies:** Ciruela, Durazno, Nectarino, Plumcot, Uchuva, Cranberry, Damasco (con frío autorizado)

| Tamaño Lote | Tamaño Muestra |
|-------------|----------------|
| ≤ 37 | Todas |
| 38 – 78 | 37 |
| 79 – 88 | 38 |
| 89 – 117 | 39 |
| 118 – 140 | 40 |
| 141 – 157 | 41 |
| 158 – 175 | 42 |
| 176 – 207 | 43 |
| 208 – 257 | 44 |
| 258 – 335 | 45 |
| 336 – 425 | 46 |
| 426 – 850 | 47 |
| 851 – 2.250 | 48 |
| **> 2.250** | **49 (LÍMITE MÁXIMO)** |

### 🚨 REGLA CRÍTICA
**NUNCA exceder 49 unidades de muestra en esta tabla.**

---

## 🍎 BIOMÉTRICA

**Especies:** Manzana, Pera, Pera Asiática, Clementina, Tangerina, Mandarina, Naranja, Granada, Baby Kiwi, Kiwi, Pomelo, Limón, Chirimoya (Systems Approach)

| Tamaño Lote | Tamaño Muestra |
|-------------|----------------|
| ≤ 30 | Todas |
| 31 – 2.000 | 30 |
| 2.001 – 10.000 | 50 |
| > 10.000 | 100 |

---

## 📈 PORCENTUAL 2%

**Especies:** Todas las demás especies no listadas arriba

### Reglas de Cálculo:

- **Lote ≤ 100:** muestra = 2
- **Lote > 100:** muestra = lote × 0.02 con reglas de redondeo:
  - **decimal ≥ 0.50** → ceil (redondear hacia arriba)
  - **decimal < 0.50** → floor (redondear hacia abajo)

**Ejemplos:**
- Lote 100 → 2
- Lote 124 → 2 (2.48 < 0.50)
- Lote 125 → 3 (2.50 ≥ 0.50)
- Lote 150 → 3 (3.00)

---

## ⚙️ LÓGICA DE SELECCIÓN

### Casos Especiales:

#### **DAMASCO**
- `cold_storage = True` → HIPERGEOMÉTRICA 6%
- `cold_storage = False` → HIPERGEOMÉTRICA 3%

#### **CHIRIMOYA**
- `systems_approach = True` → BIOMÉTRICA
- `systems_approach = False` → PORCENTUAL

---

## 🚨 VALIDACIONES OBLIGATORIAS

✅ **NUNCA retornar muestra > 49 en HIPERGEOMÉTRICA 6%**

✅ **NUNCA retornar muestra > tamaño del lote**

✅ **Priorizar tabla oficial sobre cálculo porcentual**

✅ **Asegurar al menos 1 unidad de muestra**

---

## ✅ VERIFICACIÓN DE IMPLEMENTACIÓN

Ejecutar:
```bash
python test_tablas_muestreo.py
```

Todas las pruebas deben mostrar ✓ (verificado).

---

## 📝 NOTAS DE IMPLEMENTACIÓN

- Las especies se detectan **case-insensitive** (mayúsculas/minúsculas)
- Se aceptan **singular y plural** (Durazno/Duraznos)
- Cuando la tabla indica "Todas", se muestrea el lote completo
- El límite de 49 en H6% es **absoluto e inquebrantable**

---

**Fecha de Implementación:** Febrero 2026  
**Estándar:** SAG-USDA Oficial
