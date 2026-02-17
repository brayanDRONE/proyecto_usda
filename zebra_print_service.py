"""
Servicio de impresión de etiquetas Zebra para Sistema USDA
Escucha en http://localhost:5000 y recibe peticiones del navegador
"""
import sys
import platform
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import win32print

# Conversión y medidas (asumiendo 203 dpi)
DPI = 203
def mm_to_dots(mm):
    return int(mm * DPI / 25.4)

LABEL_MM = 50              # 5 cm
LABEL_W = mm_to_dots(LABEL_MM)
LABEL_H = mm_to_dots(LABEL_MM)
SMALL_BOX_MM = 20          # 2 cm
SMALL_W = mm_to_dots(SMALL_BOX_MM)
SMALL_H = SMALL_W
MARGIN = mm_to_dots(2)     # margen pequeño

def get_available_printers():
    """Obtiene lista de impresoras disponibles en el sistema."""
    flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    return [p[2] for p in win32print.EnumPrinters(flags)]

def build_zpl_double_label(lote, left_num, right_num=None):
    """
    Construye ZPL para una tira con dos etiquetas 5x5cm lado a lado.
    Ajusta el tamaño del número para que quepa: si el número es muy largo
    (ej. 4 dígitos) reduce la altura hasta que entre en el ancho disponible.
    Mantiene el diseño: MUESTRA/USDA arriba, número grande centrado,
    debajo "LOTE: <número>" y "MUESTRA"/"USDA" con tamaño aumentado.
    """
    left_x = 0
    right_x = LABEL_W

    SCALE = 1.2  # agrandar 20% por defecto para subtexto
    max_big_by_height = max(1, int(LABEL_H * 0.6 * SCALE))   # altura máxima del número
    sub_font_h = max(10, int(LABEL_H * 0.08 * SCALE))       # tamaño de subtexto aumentado 20%

    # Estimación: ancho de caracter ≈ 0.6 * altura_de_fuente (aprox.)
    def fit_number_font_height(text, max_height, max_width):
        if not text:
            return max_height
        chars = max(1, len(str(text)))
        usable_width = int(max_width * 0.85)  # dejar 15% de margen lateral
        # altura estimada permitida por ancho: usable_width / (chars * char_width_ratio)
        approx_h = int(usable_width / (chars * 0.6))
        return max(10, min(max_height, approx_h))

    # Desplazamiento extra para "USDA": 5% del alto de etiqueta
    extra_usda_down = int(LABEL_H * 0.05)

    # Posiciones:
    top_text_y = int(MARGIN)
    muestra_y = top_text_y
    usda_y = muestra_y + int(sub_font_h * 1.05) + extra_usda_down

    # Reservar espacio superior (2 líneas de subtexto) y espacio inferior para LOTE
    reserved_top = usda_y + sub_font_h
    reserved_bottom = sub_font_h + int(sub_font_h * 0.5)
    available_for_number = LABEL_H - reserved_top - reserved_bottom

    # Base para centrar usando la altura máxima; números más pequeños se centran dentro del mismo bloque
    number_block_h = min(max_big_by_height, available_for_number)
    number_y_base = reserved_top + int((available_for_number - number_block_h) / 2)
    lote_y = number_y_base + number_block_h + int(sub_font_h * 0.2)

    # Calcular altura final para cada número (ajustar si es muy largo)
    left_big_h = fit_number_font_height(left_num, number_block_h, LABEL_W)
    right_big_h = fit_number_font_height(right_num if right_num is not None else "", number_block_h, LABEL_W)

    # Ajustar y para centrar cada número dentro del bloque reservado
    left_number_y = number_y_base + int((number_block_h - left_big_h) / 2)
    right_number_y = number_y_base + int((number_block_h - right_big_h) / 2)

    zpl = []
    zpl.append("^XA")
    zpl.append("^LH0,0")

    # --- IZQUIERDA ---
    # MUESTRA (arriba)
    zpl.append(f"^CF0,{sub_font_h}")
    zpl.append(f"^FO{left_x},{muestra_y}^FB{LABEL_W},1,0,C,0")
    zpl.append(f"^FDMUESTRA^FS")
    # USDA (debajo)
    zpl.append(f"^CF0,{sub_font_h}")
    zpl.append(f"^FO{left_x},{usda_y}^FB{LABEL_W},1,0,C,0")
    zpl.append(f"^FDUSDA^FS")

    # Número grande (centrado) - IZQUIERDA
    zpl.append(f"^CF0,{left_big_h}")
    zpl.append(f"^FO{left_x},{left_number_y}")
    zpl.append(f"^FB{LABEL_W},1,0,C,0")
    zpl.append(f"^FD{left_num}^FS")

    # LOTE debajo del número - IZQUIERDA
    zpl.append(f"^CF0,{sub_font_h}")
    zpl.append(f"^FO{left_x},{lote_y}^FB{LABEL_W},1,0,C,0")
    zpl.append(f"^FDLOTE: {lote}^FS")

    # --- DERECHA ---
    # MUESTRA (arriba)
    zpl.append(f"^CF0,{sub_font_h}")
    zpl.append(f"^FO{right_x},{muestra_y}^FB{LABEL_W},1,0,C,0")
    zpl.append(f"^FDMUESTRA^FS")
    # USDA (debajo)
    zpl.append(f"^CF0,{sub_font_h}")
    zpl.append(f"^FO{right_x},{usda_y}^FB{LABEL_W},1,0,C,0")
    zpl.append(f"^FDUSDA^FS")

    # Número grande (centrado) - DERECHA
    zpl.append(f"^CF0,{right_big_h}")
    zpl.append(f"^FO{right_x},{right_number_y}")
    zpl.append(f"^FB{LABEL_W},1,0,C,0")
    zpl.append(f"^FD{right_num if right_num is not None else ''}^FS")

    # LOTE debajo del número derecho (siempre mostrar lote)
    zpl.append(f"^CF0,{sub_font_h}")
    zpl.append(f"^FO{right_x},{lote_y}^FB{LABEL_W},1,0,C,0")
    zpl.append(f"^FDLOTE: {lote}^FS")

    zpl.append("^XZ")
    return "\n".join(zpl)

def imprimir_etiquetas(lote, numeros_caja, printer_name="ZDesigner ZD230-203dpi ZPL"):
    """Imprime etiquetas Zebra con el lote y números de caja."""
    if not numeros_caja:
        return {"success": False, "error": "No hay números de caja para imprimir"}

    if platform.system() != "Windows":
        return {"success": False, "error": "Este servicio solo funciona en Windows"}

    available = get_available_printers()
    if printer_name not in available:
        # Buscar impresora Zebra alternativa
        zebra_printers = [p for p in available if 'zebra' in p.lower() or 'zdesigner' in p.lower()]
        if zebra_printers:
            printer_name = zebra_printers[0]
        else:
            return {
                "success": False, 
                "error": f"Impresora Zebra no encontrada. Disponibles: {', '.join(available)}"
            }

    hPrinter = None
    try:
        hPrinter = win32print.OpenPrinter(printer_name)
        
        # Imprimir en pares: (0,1), (2,3), ...
        i = 0
        strips_printed = 0
        while i < len(numeros_caja):
            left = str(numeros_caja[i])
            right = str(numeros_caja[i+1]) if i+1 < len(numeros_caja) else None
            etiqueta_zpl = build_zpl_double_label(lote, left, right)
            
            # Log para debugging
            print(f"\n{'='*60}")
            print(f"Imprimiendo tira {strips_printed + 1}: Izq={left}, Der={right or 'vacío'}")
            print(f"ZPL generado:")
            print(etiqueta_zpl)
            print(f"{'='*60}\n")
            
            win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta USDA", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, etiqueta_zpl.encode('utf-8'))
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
            
            strips_printed += 1
            i += 2

        return {
            "success": True,
            "message": f"✅ Se imprimieron {strips_printed} tiras ({len(numeros_caja)} etiquetas) en '{printer_name}'"
        }
    
    except Exception as e:
        return {"success": False, "error": f"Error al imprimir: {str(e)}"}
    
    finally:
        if hPrinter:
            try:
                win32print.ClosePrinter(hPrinter)
            except:
                pass


class ZebraServiceHandler(BaseHTTPRequestHandler):
    """Handler HTTP para el servicio de impresión."""
    
    def do_OPTIONS(self):
        """Maneja preflight CORS - Permite acceso desde dominios web."""
        self.send_response(200)
        # Permitir acceso desde Vercel y localhost
        origin = self.headers.get('Origin')
        allowed_origins = [
            'http://localhost:5173',
            'http://127.0.0.1:5173',
            'https://*.vercel.app',  # Cualquier dominio Vercel
        ]
        
        # Si el origen está en la lista o es vercel.app, permitirlo
        if origin:
            if any(origin.startswith(allowed.replace('*', '')) or origin == allowed for allowed in allowed_origins):
                self.send_header('Access-Control-Allow-Origin', origin)
            elif 'vercel.app' in origin:
                self.send_header('Access-Control-Allow-Origin', origin)
            else:
                self.send_header('Access-Control-Allow-Origin', '*')  # Fallback
        else:
            self.send_header('Access-Control-Allow-Origin', '*')
            
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.end_headers()
    
    def _set_cors_headers(self):
        """Configura headers CORS para respuestas."""
        origin = self.headers.get('Origin')
        if origin and ('vercel.app' in origin or 'localhost' in origin or '127.0.0.1' in origin):
            self.send_header('Access-Control-Allow-Origin', origin)
        else:
            self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Credentials', 'true')
    
    def do_GET(self):
        """Health check."""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            printers = get_available_printers()
            response = {
                "status": "online",
                "printers": printers,  # Cambiado de printers_available a printers
                "printers_available": printers,  # Mantener por compatibilidad
                "zebra_available": len(printers) > 0  # True si hay cualquier impresora
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Recibe datos de impresión desde el navegador."""
        if self.path == '/print':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                lote = data.get('lote', '')
                numeros = data.get('numeros', [])
                printer = data.get('printer', 'ZDesigner ZD230-203dpi ZPL')
                
                if not lote:
                    raise ValueError("Número de lote requerido")
                if not numeros:
                    raise ValueError("Lista de números de caja requerida")
                
                result = imprimir_etiquetas(lote, numeros, printer)
                
                self.send_response(200 if result['success'] else 400)
                self.send_header('Content-Type', 'application/json')
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self._set_cors_headers()
                self.end_headers()
                error_response = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Personaliza el log."""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_service(port=5000):
    """Inicia el servicio de impresión."""
    if platform.system() != "Windows":
        print("❌ Este servicio solo funciona en Windows.")
        sys.exit(1)
    
    try:
        import win32print
    except ImportError:
        print("❌ Módulo 'win32print' no encontrado.")
        print("   Instalar con: pip install pywin32")
        sys.exit(1)
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, ZebraServiceHandler)
    
    print("=" * 60)
    print("🖨️  SERVICIO DE IMPRESIÓN ZEBRA - SISTEMA USDA")
    print("=" * 60)
    print(f"✅ Servicio iniciado en http://localhost:{port}")
    print(f"   Health check: http://localhost:{port}/health")
    print(f"   Endpoint: POST http://localhost:{port}/print")
    print()
    
    printers = get_available_printers()
    zebra_printers = [p for p in printers if 'zebra' in p.lower() or 'zdesigner' in p.lower()]
    
    if zebra_printers:
        print(f"✅ Impresoras Zebra detectadas:")
        for p in zebra_printers:
            print(f"   - {p}")
    else:
        print("⚠️  No se detectaron impresoras Zebra")
        print(f"   Impresoras disponibles: {', '.join(printers) if printers else 'Ninguna'}")
    
    print()
    print("🔄 Presiona Ctrl+C para detener el servicio")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✋ Servicio detenido por el usuario")
        httpd.shutdown()


if __name__ == "__main__":
    run_service(port=5000)
