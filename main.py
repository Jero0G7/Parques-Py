import pygame
import sys
from src.tablero import Tablero

pygame.init()
pantalla = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Parques")

tablero = Tablero()
reloj = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    tablero.dibujar(pantalla)
    pygame.display.flip()
    reloj.tick(60)