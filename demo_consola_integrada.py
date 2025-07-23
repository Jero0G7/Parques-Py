#!/usr/bin/env python3
"""
Demo de la consola integrada en Parqués
Este script muestra cómo funciona la nueva interfaz gráfica con consola integrada
"""

import pygame
import sys

# Inicializar pygame
pygame.init()
ANCHO_VENTANA = 800
ALTO_VENTANA = 700
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Demo - Consola Integrada Parqués")

# Configuración
FUENTE_CONSOLA = pygame.font.Font(None, 20)
FUENTE_TITULO = pygame.font.Font(None, 32)
COLOR_FONDO = (240, 240, 240)
COLOR_TEXTO = (0, 0, 0)
COLOR_CONSOLA = (50, 50, 50)

class ConsolaDemo:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.lineas = [
            "🎲 PARQUÉS - Consola Horizontal 🎲",
            "Consola integrada en la parte inferior",
            "Formato horizontal con 2 columnas",
            "Mejor aprovechamiento del espacio",
            "Input en la parte inferior",
            "Historial de mensajes visible",
            "Interfaz más intuitiva",
            "Presiona cualquier tecla para continuar..."
        ]
        
    def dibujar(self):
        # Fondo de la consola
        pygame.draw.rect(pantalla, COLOR_CONSOLA, (self.x, self.y, self.ancho, self.alto))
        pygame.draw.rect(pantalla, (100, 100, 100), (self.x, self.y, self.ancho, self.alto), 2)
        
        # Área de historial (parte superior de la consola)
        area_historial = self.alto - 50  # Dejar 50px para el input (más espacio para historial)
        
        # Dibujar líneas de texto en formato vertical simple
        if self.lineas:
            y_offset = 10
            # Calcular cuántas líneas caben en el área disponible
            espacio_disponible = area_historial - 40  # Margen de seguridad
            lineas_que_caben = espacio_disponible // 18  # 18px por línea
            
            # Asegurar que al menos se muestren 6 líneas para las preguntas
            lineas_que_caben = max(lineas_que_caben, 6)
            
            # Mostrar las últimas líneas que quepan
            lineas_a_mostrar = self.lineas[-lineas_que_caben:] if len(self.lineas) > lineas_que_caben else self.lineas
            
            for linea in lineas_a_mostrar:
                # Verificar que no se salga del área de historial
                if y_offset < area_historial - 40:  # Más margen para evitar traslape
                    # Truncar líneas muy largas para que quepan en la consola
                    if len(linea) > 65:
                        linea = linea[:62] + "..."
                    texto_surface = FUENTE_CONSOLA.render(linea, True, (255, 255, 255))
                    pantalla.blit(texto_surface, (self.x + 10, self.y + y_offset))
                    y_offset += 18  # Más espacio entre líneas
        
        # Dibujar línea separadora
        pygame.draw.line(pantalla, (100, 100, 100), 
                        (self.x + 5, self.y + area_historial), 
                        (self.x + self.ancho - 5, self.y + area_historial), 2)

def main():
    consola = ConsolaDemo(20, 620, 560, 180)
    
    # Bucle principal
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                ejecutando = False
        
        # Limpiar pantalla
        pantalla.fill(COLOR_FONDO)
        
        # Dibujar título
        titulo = FUENTE_TITULO.render("🎲 PARQUÉS - Demo 🎲", True, COLOR_TEXTO)
        pantalla.blit(titulo, (20, 10))
        
        # Dibujar área del tablero (simulada)
        pygame.draw.rect(pantalla, (200, 200, 200), (20, 50, 760, 560))
        pygame.draw.rect(pantalla, (100, 100, 100), (20, 50, 760, 560), 2)
        
        texto_tablero = FUENTE_TITULO.render("Área del Tablero", True, COLOR_TEXTO)
        pantalla.blit(texto_tablero, (320, 330))
        
        # Dibujar consola
        consola.dibujar()
        
        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()
    print("Demo completado. Ejecuta 'python3 main.py' para jugar el juego completo.")

if __name__ == "__main__":
    main() 