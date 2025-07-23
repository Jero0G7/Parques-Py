#!/usr/bin/env python3
"""
Test simple para verificar la lógica de selección de colores
"""

import pygame
import sys

# Inicializar pygame
pygame.init()
ANCHO_VENTANA = 600
ALTO_VENTANA = 800
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Test - Selección de Colores")

# Configuración
FUENTE_CONSOLA = pygame.font.Font(None, 20)
FUENTE_TITULO = pygame.font.Font(None, 32)
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
        self.lineas.append(str(mensaje))
        if len(self.lineas) > 7:
            self.lineas.pop(0)
    
    def obtener_input(self, prompt=""):
        if prompt:
            self.agregar_mensaje(prompt)
        
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
        # Fondo de la consola
        pygame.draw.rect(pantalla, COLOR_CONSOLA, (self.x, self.y, self.ancho, self.alto))
        pygame.draw.rect(pantalla, (100, 100, 100), (self.x, self.y, self.ancho, self.alto), 2)
        
        # Área de historial
        area_historial = self.alto - 40
        
        # Dibujar líneas de texto
        if self.lineas:
            y_offset = 10
            lineas_a_mostrar = self.lineas[-7:] if len(self.lineas) > 7 else self.lineas
            
            for linea in lineas_a_mostrar:
                if y_offset < area_historial - 20:
                    if len(linea) > 65:
                        linea = linea[:62] + "..."
                    texto_surface = FUENTE_CONSOLA.render(linea, True, (255, 255, 255))
                    pantalla.blit(texto_surface, (self.x + 10, self.y + y_offset))
                    y_offset += 18
        
        # Línea separadora
        pygame.draw.line(pantalla, (100, 100, 100), 
                        (self.x + 5, self.y + area_historial), 
                        (self.x + self.ancho - 5, self.y + area_historial), 2)
        
        # Input
        if self.input_activo:
            input_surface = FUENTE_CONSOLA.render(f"> {self.input_texto}", True, (255, 255, 255))
            pantalla.blit(input_surface, (self.x + 10, self.y + area_historial + 10))

def main():
    consola = ConsolaTest(20, 620, 560, 160)
    
    # Limpiar pantalla
    pantalla.fill(COLOR_FONDO)
    
    # Título
    titulo = FUENTE_TITULO.render("🎲 TEST - SELECCIÓN DE COLORES 🎲", True, COLOR_TEXTO)
    pantalla.blit(titulo, (20, 10))
    
    # Área de prueba
    pygame.draw.rect(pantalla, (200, 200, 200), (20, 50, 560, 560))
    pygame.draw.rect(pantalla, (100, 100, 100), (20, 50, 560, 560), 2)
    
    texto_prueba = FUENTE_TITULO.render("Área de Prueba", True, COLOR_TEXTO)
    pantalla.blit(texto_prueba, (220, 330))
    
    consola.dibujar()
    pygame.display.flip()
    
    # Simular la selección de colores
    consola.agregar_mensaje("🎲 Test de selección de colores")
    consola.agregar_mensaje("")
    
    num_jugadores = 2
    colores_disponibles = ["Rojo", "Azul", "Verde", "Amarillo"]
    jugadores = []

    for i in range(num_jugadores):
        nombre = consola.obtener_input(f"Nombre del jugador {i+1}: ")
        nombre = nombre.capitalize()
        consola.agregar_mensaje("Elige un color, estos son los que están disponibles:")
        for idx, color in enumerate(colores_disponibles, 1):
            consola.agregar_mensaje(f"{idx}. {color}")
        while True:
            try:
                seleccion = int(consola.obtener_input(f"{nombre}, elige tu color (1-{len(colores_disponibles)}): "))
                if 1 <= seleccion <= len(colores_disponibles):
                    color = colores_disponibles.pop(seleccion - 1)
                    consola.agregar_mensaje(f"✅ {nombre} eligió el color {color}")
                    break
                else:
                    consola.agregar_mensaje("❌ Opción inválida. Elige un número de la lista.")
            except ValueError:
                consola.agregar_mensaje("❌ Por favor, ingresa un número válido.")
        
        jugadores.append({"nombre": nombre, "color": color})
        consola.agregar_mensaje("")
    
    consola.agregar_mensaje("🎉 ¡Test completado exitosamente!")
    consola.agregar_mensaje("Jugadores registrados:")
    for jugador in jugadores:
        consola.agregar_mensaje(f"  - {jugador['nombre']}: {jugador['color']}")
    
    consola.agregar_mensaje("")
    consola.agregar_mensaje("Presiona cualquier tecla para salir...")
    consola.obtener_input()
    
    pygame.quit()
    print("Test completado. La lógica de selección de colores funciona correctamente.")

if __name__ == "__main__":
    main() 