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

    def dibujar(self, pantalla, jugadores=None):
        pantalla.fill(BLANCO)
        c = self.celda

        # Bases de colores
       

        # Cárceles internas más pequeñas (2x2 en vez de 3x3)
        mini = int(c * 2)
        offset = int(c * 0.5)
        for fila in range(2):
            for col in range(2):
                # ROJO
                pygame.draw.rect(pantalla, NEGRO, (col * mini + offset, fila * mini + offset, mini, mini), 2)
                # VERDE
                pygame.draw.rect(pantalla, NEGRO, (c * 9 + col * mini + offset, fila * mini + offset, mini, mini), 2)
                # AZUL
                pygame.draw.rect(pantalla, NEGRO, (col * mini + offset, c * 9 + fila * mini + offset, mini, mini), 2)
                # AMARILLO
                pygame.draw.rect(pantalla, NEGRO, (c * 9 + col * mini + offset, c * 9 + fila * mini + offset, mini, mini), 2)

        # Calles grises con celdas alargadas
        for i in range(15):
            for j in range(15):
                if (i in range(6, 9) or j in range(6, 9)) and not (6 <= i <= 8 and 6 <= j <= 8):
                    x = i * c
                    y = j * c
                    if i in range(6, 9):  # vertical
                        pygame.draw.rect(pantalla, GRIS, (x, y, c, int(c * 2)))
                        pygame.draw.rect(pantalla, NEGRO, (x, y, c, int(c * 2)), 1)
                    else:  # horizontal
                        pygame.draw.rect(pantalla, GRIS, (x, y, int(c * 1.5), c))
                        pygame.draw.rect(pantalla, NEGRO, (x, y, int(c * 1.5), c), 1)

        # Caminos de llegada con rectángulos
        for i in range(6):
            # ROJO - arriba
            pygame.draw.rect(pantalla, ROJO, ((6) * c, (5 - i) * c, c, int(c * 1.5)))
            # VERDE - derecha
            pygame.draw.rect(pantalla, VERDE, ((9 + i) * c, 6 * c, int(c * 1.5), c))
            # AZUL - izquierda
            pygame.draw.rect(pantalla, AZUL, ((5 - i) * c, 8 * c, int(c * 1.5), c))
            # AMARILLO - abajo
            pygame.draw.rect(pantalla, AMARILLO, ((8) * c, (9 + i) * c, c, int(c * 1.5)))

        # Centro del tablero en forma de X
        pygame.draw.polygon(pantalla, BLANCO, [
            (6 * c, 6 * c),
            (9 * c, 6 * c),
            (9 * c, 9 * c),
            (6 * c, 9 * c)
        ])
        pygame.draw.line(pantalla, NEGRO, (6 * c, 6 * c), (9 * c, 9 * c), 2)
        pygame.draw.line(pantalla, NEGRO, (9 * c, 6 * c), (6 * c, 9 * c), 2)
        pygame.draw.rect(pantalla, NEGRO, (6 * c, 6 * c, 3 * c, 3 * c), 2)

        # Dibujar fichas si hay jugadores
        if jugadores:
            self.dibujar_fichas(pantalla, jugadores)

    def dibujar_fichas(self, pantalla, jugadores):
        """Dibuja todas las fichas de los jugadores en el tablero"""
        c = self.celda
        
        for i, jugador in enumerate(jugadores):
            for j, ficha in enumerate(jugador.fichas):
                if ficha.posicion is None:  # Ficha en cárcel
                    self.dibujar_ficha_carcel(pantalla, ficha, i, j, c)
                elif ficha.posicion == "llegada":  # Ficha en llegada
                    self.dibujar_ficha_llegada(pantalla, ficha, i, j, c)
                elif isinstance(ficha.posicion, int):  # Ficha en el tablero
                    self.dibujar_ficha_tablero(pantalla, ficha, c)

    def dibujar_ficha_carcel(self, pantalla, ficha, jugador_idx, ficha_idx, c):
        """Dibuja una ficha en su cárcel correspondiente"""
        # Posiciones de las cárceles para cada jugador
        carceles = [
            (0, 0),  # Rojo - esquina superior izquierda
            (9, 0),  # Verde - esquina superior derecha  
            (0, 9),  # Azul - esquina inferior izquierda
            (9, 9)   # Amarillo - esquina inferior derecha
        ]
        
        x_base, y_base = carceles[jugador_idx]
        mini = int(c * 2)
        offset = int(c * 0.5)
        
        # Posición dentro de la cárcel (2x2)
        fila = ficha_idx // 2
        col = ficha_idx % 2
        
        x = x_base * c + col * mini + offset + mini // 4
        y = y_base * c + fila * mini + offset + mini // 4
        radio = mini // 6
        
        pygame.draw.circle(pantalla, ficha.color, (x, y), radio)
        pygame.draw.circle(pantalla, NEGRO, (x, y), radio, 2)

    def dibujar_ficha_llegada(self, pantalla, ficha, jugador_idx, ficha_idx, c):
        """Dibuja una ficha en su camino de llegada"""
        # Posiciones de llegada para cada jugador
        llegadas = [
            (6, 5),  # Rojo - arriba
            (9, 6),  # Verde - derecha
            (5, 8),  # Azul - izquierda
            (8, 9)   # Amarillo - abajo
        ]
        
        x_base, y_base = llegadas[jugador_idx]
        radio = c // 6
        
        # Posición en el camino de llegada (6 posiciones)
        if jugador_idx == 0:  # Rojo - vertical hacia arriba
            x = x_base * c + c // 2
            y = (y_base - ficha_idx) * c + c // 2
        elif jugador_idx == 1:  # Verde - horizontal hacia la derecha
            x = (x_base + ficha_idx) * c + c // 2
            y = y_base * c + c // 2
        elif jugador_idx == 2:  # Azul - horizontal hacia la izquierda
            x = (x_base - ficha_idx) * c + c // 2
            y = y_base * c + c // 2
        else:  # Amarillo - vertical hacia abajo
            x = x_base * c + c // 2
            y = (y_base + ficha_idx) * c + c // 2
        
        pygame.draw.circle(pantalla, ficha.color, (x, y), radio)
        pygame.draw.circle(pantalla, NEGRO, (x, y), radio, 2)

    def dibujar_ficha_tablero(self, pantalla, ficha, c):
        """Dibuja una ficha en el tablero principal"""
        # Por ahora, las fichas en el tablero se dibujan en posiciones temporales
        # Esto se puede expandir más adelante con la lógica del juego
        radio = c // 6
        
        # Posición temporal (se puede mejorar con un mapeo real de posiciones)
        x = 300  # Centro temporal
        y = 300  # Centro temporal
        
        pygame.draw.circle(pantalla, ficha.color, (x, y), radio)
        pygame.draw.circle(pantalla, NEGRO, (x, y), radio, 2)
