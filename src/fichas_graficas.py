import pygame

COLORES = {
    "rojo": (220, 20, 60),
    "verde": (34, 139, 34),
    "azul": (30, 144, 255),
    "amarillo": (255, 215, 0)
}

class FichaGrafica:
    def __init__(self, color, posicion, radio=18):
        self.color = color
        self.posicion = posicion
        self.radio = radio

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, self.posicion, self.radio)
        pygame.draw.circle(pantalla, (0, 0, 0), self.posicion, self.radio, 2)

def crear_fichas():
    fichas = []
    posiciones = {
        "rojo": [(60, 60), (120, 60), (60, 120), (120, 120)],
        "verde": [(480, 60), (540, 60), (480, 120), (540, 120)],
        "azul": [(60, 480), (120, 480), (60, 540), (120, 540)],
        "amarillo": [(480, 480), (540, 480), (480, 540), (540, 540)]
    }
    for equipo, color in COLORES.items():
        for pos in posiciones[equipo]:
            fichas.append(Ficha(color, pos))
    return fichas