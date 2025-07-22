import pygame
import sys
from src.tablero import Tablero
from jugador import Jugador

pygame.init()
pantalla = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Parqués Clásico")

# Crear jugadores con sus fichas
jugadores = [
    Jugador("Jugador 1", (220, 20, 60)),  # Rojo
    Jugador("Jugador 2", (34, 139, 34)),  # Verde
    Jugador("Jugador 3", (30, 144, 255)), # Azul
    Jugador("Jugador 4", (255, 215, 0))   # Amarillo
]

tablero = Tablero()
reloj = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    tablero.dibujar(pantalla, jugadores)
    pygame.display.flip()
    reloj.tick(60)