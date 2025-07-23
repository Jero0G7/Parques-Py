#!/usr/bin/env python3
"""
Versión de prueba del juego con modo debug activado
"""

from src.jugador import Jugador
from src.dados import lanzar_dados, es_par
from src.tablero_logico import Tablero
from src.consola import mostrar_fichas_llegadas, mostrar_tablero
import pygame
from src.tablero_grafico import Tablero as TableroGrafico
import time
import sys

MODO_DESARROLLO = True  # Modo debug activado

# Inicializar pygame para la visualización gráfica
pygame.init()
ANCHO_VENTANA = 600
ALTO_VENTANA = 800  # Aumentar altura para la consola horizontal
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Parqués - Modo Debug")
tablero_grafico = TableroGrafico()

# Configuración de la consola integrada
FUENTE_CONSOLA = pygame.font.Font(None, 20)  # Fuente más pequeña para más texto
FUENTE_TITULO = pygame.font.Font(None, 32)
COLOR_FONDO = (240, 240, 240)
COLOR_TEXTO = (0, 0, 0)
COLOR_CONSOLA = (50, 50, 50)
COLOR_INPUT = (255, 255, 255)

class ConsolaIntegrada:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.lineas = []
        self.input_texto = ""
        self.input_activo = False
        self.max_lineas = 12  # Más líneas para consola más alta
        
    def agregar_mensaje(self, mensaje):
        """Agrega un mensaje a la consola"""
        self.lineas.append(str(mensaje))
        if len(self.lineas) > self.max_lineas:
            self.lineas.pop(0)
    
    def obtener_input(self, prompt=""):
        """Obtiene input del usuario desde la consola integrada"""
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
                        if self.input_texto.strip():  # Solo aceptar si hay texto
                            texto = self.input_texto
                            self.input_texto = ""
                            self.input_activo = False
                            self.agregar_mensaje(f"> {texto}")
                            pygame.time.wait(100)  # Pequeña pausa para evitar múltiples inputs
                            return texto
                    elif evento.key == pygame.K_BACKSPACE:
                        self.input_texto = self.input_texto[:-1]
                    elif evento.key == pygame.K_ESCAPE:
                        # Permitir cancelar con ESC
                        self.input_texto = ""
                        self.input_activo = False
                        pygame.time.wait(100)  # Pequeña pausa para evitar múltiples inputs
                        return ""
                    elif evento.unicode.isprintable():  # Solo caracteres imprimibles
                        self.input_texto += evento.unicode
            
            # Actualizar solo la consola sin llamar a actualizar_visualizacion
            self.dibujar()
            pygame.display.flip()
            pygame.time.wait(10)  # Pequeña pausa para no saturar la CPU
    
    def dibujar(self):
        """Dibuja la consola en la pantalla"""
        # Fondo de la consola
        pygame.draw.rect(pantalla, COLOR_CONSOLA, (self.x, self.y, self.ancho, self.alto))
        pygame.draw.rect(pantalla, (100, 100, 100), (self.x, self.y, self.ancho, self.alto), 2)
        
        # Área de historial (parte superior de la consola)
        area_historial = self.alto - 40  # Dejar 40px para el input
        
        # Dibujar líneas de texto en formato vertical simple
        if self.lineas:
            y_offset = 10
            # Mostrar las últimas líneas (hasta 7 líneas para dejar espacio)
            lineas_a_mostrar = self.lineas[-7:] if len(self.lineas) > 7 else self.lineas
            
            for linea in lineas_a_mostrar:
                # Verificar que no se salga del área de historial
                if y_offset < area_historial - 20:
                    # Truncar líneas muy largas para que quepan en la consola
                    if len(linea) > 65:  # Más espacio para texto
                        linea = linea[:62] + "..."
                    texto_surface = FUENTE_CONSOLA.render(linea, True, (255, 255, 255))
                    pantalla.blit(texto_surface, (self.x + 10, self.y + y_offset))
                    y_offset += 18  # Más espacio entre líneas
        
        # Dibujar línea separadora
        pygame.draw.line(pantalla, (100, 100, 100), 
                        (self.x + 5, self.y + area_historial), 
                        (self.x + self.ancho - 5, self.y + area_historial), 2)
        
        # Dibujar línea de input en la parte inferior (área separada)
        if self.input_activo:
            input_surface = FUENTE_CONSOLA.render(f"> {self.input_texto}", True, (255, 255, 255))
            pantalla.blit(input_surface, (self.x + 10, self.y + area_historial + 10))

# Crear instancia de la consola integrada (horizontal en la parte inferior)
consola = ConsolaIntegrada(20, 620, 560, 160)  # Más alta y ajustada al ancho

def actualizar_visualizacion(jugadores, tablero):
    """Actualiza la visualización gráfica del tablero"""
    # Limpiar pantalla
    pantalla.fill(COLOR_FONDO)
    
    # Dibujar título
    titulo = FUENTE_TITULO.render("🎲 PARQUÉS - MODO DEBUG 🎲", True, COLOR_TEXTO)
    pantalla.blit(titulo, (20, 10))
    
    # Dibujar tablero en el área izquierda
    if jugadores:
        tablero_grafico.dibujar(pantalla, jugadores)
    else:
        # Dibujar tablero vacío
        tablero_grafico.dibujar(pantalla, [])
    
    # Dibujar consola
    consola.dibujar()
    
    pygame.display.flip()

def juego_debug():
    consola.agregar_mensaje("🎲 Bienvenido al modo DEBUG de Parqués! 🎲")
    consola.agregar_mensaje("📺 En este modo puedes controlar los dados")
    
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
                    break
                else:
                    consola.agregar_mensaje("Opción inválida. Elige un número de la lista.")
            except ValueError:
                consola.agregar_mensaje("Por favor, ingresa un número válido.")
        jugador = Jugador(nombre, color)
        jugadores.append(jugador)

    tablero = Tablero()
    turno_actual = 0

    # Mostrar el tablero inicial
    actualizar_visualizacion(jugadores, tablero)
    consola.agregar_mensaje("🎮 ¡El juego comienza en modo DEBUG!")

    # Simular solo 3 turnos para prueba
    for turno_num in range(3):
        consola.agregar_mensaje(f"--- TURNO {turno_num + 1} ---")
        
        # Lanzar dados con manejo de errores
        try:
            d1, d2 = lanzar_dados(debug=True, input_func=consola.obtener_input)
            consola.agregar_mensaje(f"Lanzó: {d1} y {d2}")
        except (ValueError, TypeError):
            import random
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            consola.agregar_mensaje(f"Error en entrada de dados. Lanzó: {d1} y {d2}")
        
        actualizar_visualizacion(jugadores, tablero)
        time.sleep(1)
        
        turno_actual = (turno_actual + 1) % len(jugadores)
    
    consola.agregar_mensaje("🎉 ¡Prueba de modo DEBUG completada!")
    consola.agregar_mensaje("Presiona cualquier tecla para cerrar...")
    consola.obtener_input()

if __name__ == "__main__":
    try:
        juego_debug()
    finally:
        pygame.quit() 