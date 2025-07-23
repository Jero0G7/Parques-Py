import pygame
import sys
import time

# Inicializar pygame
pygame.init()
ANCHO_VENTANA = 600
ALTO_VENTANA = 800
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Test - Preguntas y Últimas Líneas")

# Configuración de la consola integrada
FUENTE_CONSOLA = pygame.font.Font(None, 20)
COLOR_FONDO = (240, 240, 240)
COLOR_TEXTO = (0, 0, 0)
COLOR_CONSOLA = (50, 50, 50)

class ConsolaTest:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.lineas = []
        self.input_texto = ""
        self.input_activo = False
        
    def agregar_mensaje(self, mensaje):
        """Agrega un mensaje a la consola"""
        self.lineas.append(str(mensaje))
        print(f"DEBUG: Agregado mensaje: {mensaje}")
        print(f"DEBUG: Total de líneas: {len(self.lineas)}")
    
    def obtener_input(self, prompt=""):
        """Obtiene input del usuario desde la consola integrada"""
        if prompt:
            self.agregar_mensaje(prompt)
            print(f"DEBUG: Pregunta agregada: {prompt}")
        
        self.input_activo = True
        self.input_texto = ""
        
        while self.input_activo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if self.input_texto.strip():
                            texto = self.input_texto
                            self.input_texto = ""
                            self.input_activo = False
                            self.agregar_mensaje(f"> {texto}")
                            pygame.time.wait(100)
                            return texto
                    elif evento.key == pygame.K_BACKSPACE:
                        self.input_texto = self.input_texto[:-1]
                    elif evento.key == pygame.K_ESCAPE:
                        self.input_texto = ""
                        self.input_activo = False
                        pygame.time.wait(100)
                        return ""
                    elif evento.unicode.isprintable():
                        self.input_texto += evento.unicode
            
            self.dibujar()
            pygame.display.flip()
            pygame.time.wait(10)
    
    def dibujar(self):
        """Dibuja la consola en la pantalla"""
        # Fondo de la consola
        pygame.draw.rect(pantalla, COLOR_CONSOLA, (self.x, self.y, self.ancho, self.alto))
        pygame.draw.rect(pantalla, (100, 100, 100), (self.x, self.y, self.ancho, self.alto), 2)
        
        # Área de historial (parte superior de la consola)
        area_historial = self.alto - 60  # Dejar 60px para el input
        
        # Dibujar líneas de texto con cálculo dinámico
        if self.lineas:
            y_offset = 10
            # Calcular cuántas líneas caben en el área disponible
            espacio_disponible = area_historial - 40  # Margen de seguridad
            lineas_que_caben = espacio_disponible // 18  # 18px por línea
            
            print(f"DEBUG: Área historial: {area_historial}, Espacio disponible: {espacio_disponible}")
            print(f"DEBUG: Líneas que caben: {lineas_que_caben}, Total líneas: {len(self.lineas)}")
            
            # Mostrar las últimas líneas que quepan
            lineas_a_mostrar = self.lineas[-lineas_que_caben:] if len(self.lineas) > lineas_que_caben else self.lineas
            
            print(f"DEBUG: Líneas a mostrar: {len(lineas_a_mostrar)}")
            for i, linea in enumerate(lineas_a_mostrar):
                print(f"DEBUG: Mostrando línea {i+1}: {linea[:30]}...")
            
            for linea in lineas_a_mostrar:
                # Verificar que no se salga del área de historial
                if y_offset < area_historial - 40:
                    # Truncar líneas muy largas
                    if len(linea) > 65:
                        linea = linea[:62] + "..."
                    texto_surface = FUENTE_CONSOLA.render(linea, True, (255, 255, 255))
                    pantalla.blit(texto_surface, (self.x + 10, self.y + y_offset))
                    y_offset += 18
        
        # Dibujar línea separadora
        pygame.draw.line(pantalla, (100, 100, 100), 
                        (self.x + 5, self.y + area_historial), 
                        (self.x + self.ancho - 5, self.y + area_historial), 2)
        
        # Dibujar línea de input
        if self.input_activo:
            input_surface = FUENTE_CONSOLA.render(f"> {self.input_texto}", True, (255, 255, 255))
            pantalla.blit(input_surface, (self.x + 10, self.y + area_historial + 20))

def main():
    consola = ConsolaTest(20, 620, 560, 180)
    
    # Limpiar pantalla
    pantalla.fill(COLOR_FONDO)
    
    # Dibujar título
    titulo = FUENTE_CONSOLA.render("🧪 TEST - Preguntas y Últimas Líneas", True, COLOR_TEXTO)
    pantalla.blit(titulo, (20, 10))
    
    # Agregar mensajes de prueba
    consola.agregar_mensaje("🎲 Test de visualización de preguntas")
    consola.agregar_mensaje("📝 Verificando que las últimas líneas se muestren")
    consola.agregar_mensaje("🔍 Especialmente las preguntas importantes")
    consola.agregar_mensaje("")
    consola.agregar_mensaje("Mensaje 1: Información general")
    consola.agregar_mensaje("Mensaje 2: Más información")
    consola.agregar_mensaje("Mensaje 3: Información adicional")
    consola.agregar_mensaje("Mensaje 4: Datos importantes")
    consola.agregar_mensaje("Mensaje 5: Información crítica")
    consola.agregar_mensaje("Mensaje 6: Última información")
    consola.agregar_mensaje("Mensaje 7: Información final")
    consola.agregar_mensaje("Mensaje 8: Datos finales")
    
    # Dibujar consola
    consola.dibujar()
    pygame.display.flip()
    
    print("\n🧪 TEST INICIADO")
    print("Verifica que las últimas líneas sean visibles")
    print("Especialmente las preguntas importantes")
    print("Presiona ENTER para continuar...")
    
    # Obtener input de prueba
    respuesta = consola.obtener_input("¿Puedes ver esta pregunta claramente?")
    consola.agregar_mensaje(f"Respuesta recibida: {respuesta}")
    
    respuesta2 = consola.obtener_input("¿Y esta segunda pregunta?")
    consola.agregar_mensaje(f"Segunda respuesta: {respuesta2}")
    
    consola.agregar_mensaje("✅ Test completado")
    consola.agregar_mensaje("Presiona ENTER para salir...")
    consola.obtener_input()
    
    print("✅ Test completado exitosamente")

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit() 