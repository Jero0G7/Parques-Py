import pygame
import sys
import time

# Inicializar pygame
pygame.init()
ANCHO_VENTANA = 600
ALTO_VENTANA = 800
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Test - Auto-Scroll")

# Configuración de la consola integrada
FUENTE_CONSOLA = pygame.font.Font(None, 20)
FUENTE_TITULO = pygame.font.Font(None, 32)
COLOR_FONDO = (240, 240, 240)
COLOR_TEXTO = (0, 0, 0)
COLOR_CONSOLA = (50, 50, 50)

class ConsolaTestScroll:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.lineas = []
        self.input_texto = ""
        self.input_activo = False
        self.scroll_offset = 0
        self.lineas_por_pagina = 8
        self.auto_scroll = True
        
        # Agregar mensajes de prueba
        for i in range(25):
            self.lineas.append(f"Línea #{i+1:02d}: Mensaje de prueba para verificar auto-scroll")
        
        # Configurar auto-scroll al final después de agregar los mensajes
        if len(self.lineas) > self.lineas_por_pagina:
            self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)
        
        print(f"DEBUG: Total de líneas: {len(self.lineas)}")
        print(f"DEBUG: Scroll offset inicial: {self.scroll_offset}")
        print(f"DEBUG: Líneas por página: {self.lineas_por_pagina}")
        print(f"DEBUG: Líneas visibles: {self.lineas[self.scroll_offset:self.scroll_offset + self.lineas_por_pagina]}")
        
    def agregar_mensaje(self, mensaje):
        """Agrega un mensaje a la consola"""
        self.lineas.append(str(mensaje))
        # Auto-scroll al final cuando se agrega un mensaje (solo si auto_scroll está activo)
        if self.auto_scroll and len(self.lineas) > self.lineas_por_pagina:
            self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)
            print(f"DEBUG: Auto-scroll activado. Nuevo offset: {self.scroll_offset}")
    
    def obtener_input(self, prompt=""):
        """Obtiene input del usuario desde la consola integrada"""
        if prompt:
            self.agregar_mensaje(prompt)
            # Forzar actualización inmediata para mostrar la pregunta
            self.dibujar()
            pygame.display.flip()
        
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
                            # Forzar auto-scroll al final después de agregar el mensaje
                            if self.auto_scroll and len(self.lineas) > self.lineas_por_pagina:
                                self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)
                            pygame.time.wait(100)
                            return texto
                    elif evento.key == pygame.K_BACKSPACE:
                        self.input_texto = self.input_texto[:-1]
                    elif evento.key == pygame.K_ESCAPE:
                        self.input_texto = ""
                        self.input_activo = False
                        pygame.time.wait(100)
                        return ""
                    elif evento.key == pygame.K_UP:
                        # Scroll hacia arriba
                        if self.scroll_offset > 0:
                            self.scroll_offset -= 1
                            self.auto_scroll = False
                            print(f"DEBUG: Scroll arriba. Offset: {self.scroll_offset}, Auto-scroll: {self.auto_scroll}")
                    elif evento.key == pygame.K_DOWN:
                        # Scroll hacia abajo
                        if self.scroll_offset < max(0, len(self.lineas) - self.lineas_por_pagina):
                            self.scroll_offset += 1
                            # Si llega al final, reactivar auto-scroll
                            if self.scroll_offset >= max(0, len(self.lineas) - self.lineas_por_pagina):
                                self.auto_scroll = True
                            print(f"DEBUG: Scroll abajo. Offset: {self.scroll_offset}, Auto-scroll: {self.auto_scroll}")
                    elif evento.key == pygame.K_PAGEUP:
                        # Scroll rápido hacia arriba
                        self.scroll_offset = max(0, self.scroll_offset - 3)
                        self.auto_scroll = False
                        print(f"DEBUG: Page Up. Offset: {self.scroll_offset}, Auto-scroll: {self.auto_scroll}")
                    elif evento.key == pygame.K_PAGEDOWN:
                        # Scroll rápido hacia abajo
                        self.scroll_offset = min(len(self.lineas) - self.lineas_por_pagina, self.scroll_offset + 3)
                        # Si llega al final, reactivar auto-scroll
                        if self.scroll_offset >= max(0, len(self.lineas) - self.lineas_por_pagina):
                            self.auto_scroll = True
                        print(f"DEBUG: Page Down. Offset: {self.scroll_offset}, Auto-scroll: {self.auto_scroll}")
                    elif evento.key == pygame.K_HOME:
                        # Ir al inicio
                        self.scroll_offset = 0
                        self.auto_scroll = False
                        print(f"DEBUG: Home. Offset: {self.scroll_offset}, Auto-scroll: {self.auto_scroll}")
                    elif evento.key == pygame.K_END:
                        # Ir al final
                        self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)
                        self.auto_scroll = True
                        print(f"DEBUG: End. Offset: {self.scroll_offset}, Auto-scroll: {self.auto_scroll}")
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
        area_historial = self.alto - 30  # Dejar 30px para el input
        
        # Dibujar líneas de texto con scroll
        if self.lineas:
            y_offset = 10
            
            # Calcular líneas a mostrar basadas en el scroll
            inicio = self.scroll_offset
            fin = min(inicio + self.lineas_por_pagina, len(self.lineas))
            lineas_a_mostrar = self.lineas[inicio:fin]
            
            # Mostrar indicador de scroll si hay más líneas
            if len(self.lineas) > self.lineas_por_pagina:
                # Indicador de posición en el scroll
                scroll_info = f"📜 {inicio + 1}-{fin} de {len(self.lineas)}"
                scroll_surface = FUENTE_CONSOLA.render(scroll_info, True, (200, 200, 200))
                pantalla.blit(scroll_surface, (self.x + self.ancho - 120, self.y + 5))
                
                # Indicador de auto-scroll
                if self.auto_scroll:
                    auto_scroll_info = "🔄 AUTO"
                    auto_scroll_surface = FUENTE_CONSOLA.render(auto_scroll_info, True, (100, 255, 100))
                    pantalla.blit(auto_scroll_surface, (self.x + 10, self.y + 5))
                else:
                    auto_scroll_info = "⏸️ MANUAL"
                    auto_scroll_surface = FUENTE_CONSOLA.render(auto_scroll_info, True, (255, 200, 100))
                    pantalla.blit(auto_scroll_surface, (self.x + 10, self.y + 5))
            
            for linea in lineas_a_mostrar:
                # Verificar que no se salga del área de historial
                if y_offset < area_historial - 10:  # Mínimo margen para mostrar todas las líneas
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
            pantalla.blit(input_surface, (self.x + 10, self.y + area_historial + 5))  # Mínima separación

def main():
    consola = ConsolaTestScroll(20, 620, 560, 180)
    
    # Limpiar pantalla
    pantalla.fill(COLOR_FONDO)
    
    # Dibujar título
    titulo = FUENTE_TITULO.render("🧪 TEST - Auto-Scroll", True, COLOR_TEXTO)
    pantalla.blit(titulo, (20, 10))
    
    # Dibujar instrucciones
    instrucciones = [
        "📊 TEST DE AUTO-SCROLL:",
        f"Total de líneas: {len(consola.lineas)}",
        f"Líneas por página: {consola.lineas_por_pagina}",
        f"Scroll offset inicial: {consola.scroll_offset}",
        f"Líneas visibles: {consola.scroll_offset + 1}-{min(consola.scroll_offset + consola.lineas_por_pagina, len(consola.lineas))}",
        "",
        "🎯 VERIFICAR:",
        "1. ¿Se ven las últimas 8 líneas?",
        "2. ¿El indicador muestra AUTO?",
        "3. ¿El scroll funciona correctamente?"
    ]
    
    y_offset = 50
    for instruccion in instrucciones:
        texto = FUENTE_CONSOLA.render(instruccion, True, COLOR_TEXTO)
        pantalla.blit(texto, (20, y_offset))
        y_offset += 25
    
    # Dibujar consola
    consola.dibujar()
    pygame.display.flip()
    
    print("\n🧪 TEST DE AUTO-SCROLL INICIADO")
    print("Verifica que se muestren las últimas 8 líneas (18-25)")
    print("El indicador debe mostrar 🔄 AUTO")
    
    # Obtener input de prueba
    respuesta = consola.obtener_input("¿Se ven las últimas líneas? (escribe algo)")
    consola.agregar_mensaje(f"Respuesta: {respuesta}")
    
    consola.agregar_mensaje("✅ Test de auto-scroll completado")
    consola.agregar_mensaje("Presiona ENTER para salir...")
    consola.obtener_input()
    
    print("✅ Test de auto-scroll completado exitosamente")

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit() 