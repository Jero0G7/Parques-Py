import pygame

# Colores
ROJO = (220, 20, 60)
VERDE = (34, 139, 34)
AZUL = (30, 144, 255)
AMARILLO = (255, 215, 0)
GRIS = (211, 211, 211)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

class Tablero:
    def __init__(self):
        self.tamano = 600
        self.celda = self.tamano // 15

    def dibujar(self, pantalla):
        pantalla.fill(BLANCO)

        c = self.celda

        # Bases
        pygame.draw.rect(pantalla, ROJO, (0, 0, c * 6, c * 6))
        pygame.draw.rect(pantalla, VERDE, (c * 9, 0, c * 6, c * 6))
        pygame.draw.rect(pantalla, AZUL, (0, c * 9, c * 6, c * 6))
        pygame.draw.rect(pantalla, AMARILLO, (c * 9, c * 9, c * 6, c * 6))

        # Líneas internas de las bases
        for fila in range(2):
            for col in range(2):
                pygame.draw.rect(pantalla, NEGRO, (col * 3 * c, fila * 3 * c, 3 * c, 3 * c), 2)
                pygame.draw.rect(pantalla, NEGRO, (c * 9 + col * 3 * c, fila * 3 * c, 3 * c, 3 * c), 2)
                pygame.draw.rect(pantalla, NEGRO, (col * 3 * c, c * 9 + fila * 3 * c, 3 * c, 3 * c), 2)
                pygame.draw.rect(pantalla, NEGRO, (c * 9 + col * 3 * c, c * 9 + fila * 3 * c, 3 * c, 3 * c), 2)

        # Calles grises
        for i in range(15):
            for j in range(15):
                if (i in range(6, 9) or j in range(6, 9)) and not (6 <= i <= 8 and 6 <= j <= 8):
                    pygame.draw.rect(pantalla, GRIS, (i * c, j * c, c, c))
                    pygame.draw.rect(pantalla, NEGRO, (i * c, j * c, c, c), 1)

        # Caminos de llegada
        for i in range(6):
            pygame.draw.rect(pantalla, ROJO, ((6) * c, (5 - i) * c, c, c))
            pygame.draw.rect(pantalla, VERDE, ((9 + i) * c, 6 * c, c, c))
            pygame.draw.rect(pantalla, AZUL, ((5 - i) * c, 8 * c, c, c))
            pygame.draw.rect(pantalla, AMARILLO, ((8) * c, (9 + i) * c, c, c))

        # Centro en X
        pygame.draw.polygon(pantalla, BLANCO, [
            (6 * c, 6 * c),
            (9 * c, 6 * c),
            (9 * c, 9 * c),
            (6 * c, 9 * c)
        ])
        pygame.draw.line(pantalla, NEGRO, (6 * c, 6 * c), (9 * c, 9 * c), 2)
        pygame.draw.line(pantalla, NEGRO, (9 * c, 6 * c), (6 * c, 9 * c), 2)
        pygame.draw.rect(pantalla, NEGRO, (6 * c, 6 * c, 3 * c, 3 * c), 2)
