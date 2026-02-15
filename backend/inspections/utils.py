"""
Utilidades para cálculo de muestreo.
"""
import math
import random


# ==================== CLASIFICACIÓN DE ESPECIES ====================

ESPECIES_HIPERGEOMETRICA_3 = [
    'Damasco',
    'Damascos',
]

ESPECIES_HIPERGEOMETRICA_6 = [
    'Ciruela',
    'Ciruelas',
    'Damasco_condicional',
    'Durazno',
    'Duraznos',
    'Nectarino',
    'Nectarinos',
    'Nectarin',
    'Nectarines',
    'Plumcot',
    'Plumcots',
    'Uchuva',
    'Uchuvas',
    'Cranberry',
    'Cranberries',
]

ESPECIES_BIOMETRICA = [
    'Manzana',
    'Manzanas',
    'Pera',
    'Peras',
    'Pera Asiática',
    'Peras Asiáticas',
    'Clementina',
    'Clementinas',
    'Tangerina',
    'Tangerinas',
    'Mandarina',
    'Mandarinas',
    'Naranja',
    'Naranjas',
    'Granada',
    'Granadas',
    'Baby Kiwi',
    'Baby Kiwis',
    'Kiwi',
    'Kiwis',
    'Pomelo',
    'Pomelos',
    'Limón',
    'Limones',
    'Chirimoya_condicional',
    'Chirimoyas_condicional',
]

# ==================== TABLAS DE MUESTREO OFICIALES SAG-USDA ====================

# Tabla Hipergeométrica 3% (3% infestación - 95% confianza)
# Especie: Damasco (sin frío autorizado)
TABLA_HIPERGEOMETRICA_3 = [
    (1, 900, None),      # Todas las unidades
    (901, 1500, 63),
    (1501, 4000, 90),
    (4001, 10000, 94),
    (10001, 15000, 96),
    (15001, 20000, 98),
    (20001, float('inf'), 99),
]

# Tabla Hipergeométrica 6% (6% infestación - 95% confianza)
# Especies: Ciruela, Durazno, Nectarino, Plumcot, Uchuva, Cranberry, Damasco (con frío)
# 🚨 LÍMITE MÁXIMO: 49 unidades
TABLA_HIPERGEOMETRICA_6 = [
    (1, 37, None),       # Todas las unidades
    (38, 78, 37),
    (79, 88, 38),
    (89, 117, 39),
    (118, 140, 40),
    (141, 157, 41),
    (158, 175, 42),
    (176, 207, 43),
    (208, 257, 44),
    (258, 335, 45),
    (336, 425, 46),
    (426, 850, 47),
    (851, 2250, 48),
    (2251, float('inf'), 49),  # LÍMITE MÁXIMO ABSOLUTO: 49
]

# Tabla Biométrica
# Especies: Manzana, Pera, Pera Asiática, Clementina, Tangerina, Mandarina, 
#           Naranja, Granada, Baby Kiwi, Kiwi, Pomelo, Limón, Chirimoya (Systems Approach)
TABLA_BIOMETRICA = [
    (1, 30, None),       # Todas las unidades
    (31, 2000, 30),
    (2001, 10000, 50),
    (10001, float('inf'), 100),
]


def obtener_tipo_tabla_muestreo(especie):
    """
    Determina qué tipo de tabla de muestreo usar según la especie.
    
    Args:
        especie (str): Nombre de la especie
    
    Returns:
        str: Tipo de tabla ('HIPERGEOMETRICA_3', 'HIPERGEOMETRICA_6', 'BIOMETRICA', 'PORCENTUAL')
    """
    # Normalizar la especie para comparación case-insensitive
    especie_lower = especie.lower() if especie else ''
    
    # Crear versiones normalizadas de las listas
    especies_h3_lower = [e.lower() for e in ESPECIES_HIPERGEOMETRICA_3]
    especies_h6_lower = [e.lower() for e in ESPECIES_HIPERGEOMETRICA_6]
    especies_bio_lower = [e.lower() for e in ESPECIES_BIOMETRICA]
    
    if especie_lower in especies_h3_lower:
        return 'HIPERGEOMETRICA_3'
    elif especie_lower in especies_h6_lower:
        return 'HIPERGEOMETRICA_6'
    elif especie_lower in especies_bio_lower:
        return 'BIOMETRICA'
    else:
        return 'PORCENTUAL'


def calcular_tamano_muestra_por_tabla(tamano_lote, tipo_tabla):
    """
    Calcula el tamaño de muestra según la tabla de muestreo SAG-USDA oficial.
    
    Args:
        tamano_lote (int): Tamaño total del lote
        tipo_tabla (str): Tipo de tabla a usar
    
    Returns:
        tuple: (tamano_muestra: int, nombre_tabla: str)
    """
    if tipo_tabla == 'HIPERGEOMETRICA_3':
        tabla = TABLA_HIPERGEOMETRICA_3
        nombre = 'Hipergeométrica del 3%'
    elif tipo_tabla == 'HIPERGEOMETRICA_6':
        tabla = TABLA_HIPERGEOMETRICA_6
        nombre = 'Hipergeométrica del 6%'
    elif tipo_tabla == 'BIOMETRICA':
        tabla = TABLA_BIOMETRICA
        nombre = 'Biométrica'
    else:  # PORCENTUAL
        # Reglas especiales para Porcentual 2%
        if tamano_lote <= 100:
            tamano_muestra = 2
        else:
            # Calcular 2% con reglas de redondeo especiales
            valor = tamano_lote * 0.02
            decimal = valor - int(valor)
            
            if decimal >= 0.50:
                tamano_muestra = math.ceil(valor)
            else:
                tamano_muestra = math.floor(valor)
        
        return tamano_muestra, 'Porcentual 2%'
    
    # Buscar en la tabla el rango correspondiente
    for rango_min, rango_max, muestra in tabla:
        if rango_min <= tamano_lote <= rango_max:
            # Si muestra es None, significa "Todas las unidades"
            if muestra is None:
                return tamano_lote, nombre
            else:
                return muestra, nombre
    
    # Si no se encuentra en la tabla, usar el último valor
    ultima_muestra = tabla[-1][2]
    if ultima_muestra is None:
        return tamano_lote, nombre
    else:
        return ultima_muestra, nombre


def calcular_muestreo(tamano_lote, especie=None, porcentaje=None):
    """
    Calcula el muestreo según la especie o porcentaje especificado.
    
    Args:
        tamano_lote (int): Tamaño total del lote
        especie (str, optional): Nombre de la especie para determinar la tabla
        porcentaje (float, optional): Porcentaje de muestreo manual (solo si no se especifica especie)
    
    Returns:
        dict: Diccionario con:
            - tamano_lote: Tamaño del lote
            - tipo_tabla: Tipo de tabla utilizada
            - nombre_tabla: Nombre descriptivo de la tabla
            - tamano_muestra: Cantidad de cajas a muestrear
            - cajas_seleccionadas: Lista ordenada de números de caja
    """
    if tamano_lote <= 0:
        raise ValueError("El tamaño del lote debe ser mayor a 0")
    
    # Determinar el tamaño de muestra según la especie o porcentaje
    if especie:
        tipo_tabla = obtener_tipo_tabla_muestreo(especie)
        tamano_muestra, nombre_tabla = calcular_tamano_muestra_por_tabla(tamano_lote, tipo_tabla)
    elif porcentaje:
        if porcentaje <= 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        tamano_muestra = math.ceil(tamano_lote * (porcentaje / 100))
        tipo_tabla = 'PORCENTUAL'
        nombre_tabla = f'Porcentual {porcentaje}%'
    else:
        # Default: 2%
        tamano_muestra = math.ceil(tamano_lote * 0.02)
        tipo_tabla = 'PORCENTUAL'
        nombre_tabla = 'Porcentual 2%'
    
    # 🚨 VALIDACIONES CRÍTICAS OFICIALES SAG-USDA 🚨
    
    # Validación 1: NUNCA exceder 49 en tabla Hipergeométrica 6%
    if tipo_tabla == 'HIPERGEOMETRICA_6' and tamano_muestra > 49:
        tamano_muestra = 49
    
    # Validación 2: NUNCA exceder el tamaño del lote
    if tamano_muestra > tamano_lote:
        tamano_muestra = tamano_lote
    
    # Validación 3: Asegurar al menos 1 unidad de muestra
    if tamano_muestra < 1:
        tamano_muestra = 1
    
    # Generar números aleatorios únicos
    cajas_seleccionadas = generar_cajas_aleatorias(tamano_lote, tamano_muestra)
    
    return {
        'tamano_lote': tamano_lote,
        'tipo_tabla': tipo_tabla,
        'nombre_tabla': nombre_tabla,
        'tamano_muestra': tamano_muestra,
        'cajas_seleccionadas': cajas_seleccionadas
    }


def generar_cajas_aleatorias(tamano_lote, cantidad):
    """
    Genera una lista de números de caja aleatorios únicos.
    
    Args:
        tamano_lote (int): Rango máximo (1 a tamano_lote)
        cantidad (int): Cantidad de números a generar
    
    Returns:
        list: Lista ordenada de números únicos
    """
    if cantidad > tamano_lote:
        raise ValueError("La cantidad no puede ser mayor al tamaño del lote")
    
    # Generar números aleatorios únicos en el rango [1, tamano_lote]
    cajas = random.sample(range(1, tamano_lote + 1), cantidad)
    
    # Ordenar la lista
    cajas.sort()
    
    return cajas


def validar_datos_inspeccion(data):
    """
    Valida los datos de una inspección antes de procesarla.
    
    Args:
        data (dict): Datos de la inspección
    
    Returns:
        tuple: (es_valido: bool, errores: list)
    """
    errores = []
    
    # Validar campos requeridos
    campos_requeridos = [
        'exportador', 'establishment', 'inspector_sag', 'contraparte_sag',
        'especie', 'numero_lote', 'tamano_lote', 'tipo_muestreo',
        'tipo_despacho', 'cantidad_pallets'
    ]
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            errores.append(f"El campo '{campo}' es requerido")
    
    # Validar valores numéricos
    if 'tamano_lote' in data:
        try:
            tamano_lote = int(data['tamano_lote'])
            if tamano_lote <= 0:
                errores.append("El tamaño del lote debe ser mayor a 0")
        except (ValueError, TypeError):
            errores.append("El tamaño del lote debe ser un número válido")
    
    if 'cantidad_pallets' in data:
        try:
            cantidad_pallets = int(data['cantidad_pallets'])
            if cantidad_pallets <= 0:
                errores.append("La cantidad de pallets debe ser mayor a 0")
        except (ValueError, TypeError):
            errores.append("La cantidad de pallets debe ser un número válido")
    
    return len(errores) == 0, errores
