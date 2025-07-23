import pygame

ROJO = (220, 20, 60)
VERDE = (34, 139, 34)
AZUL = (30, 144, 255)
AMARILLO = (255, 215, 0)
GRIS = (211, 211, 211)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

class Tablero:
    def generar_diccionario_cruz(self):
        posiciones = {}
        centro = 8
        for i in range(8):
            posiciones[i+1] = (centro, centro - 8 + i)
        for i in range(17):
            posiciones[i+9] = (centro - 8 + i, centro)
        for i in range(17):
            posiciones[i+26] = (centro, centro + 1 + i)
        for i in range(17):
            posiciones[i+43] = (centro + 1 + i, centro)
        for i in range(9):
            posiciones[i+60] = (centro, centro - 1 - i)
        return posiciones

    def __init__(self):
        self.tamano = 600
        self.celda = self.tamano // 19
        self.posiciones = self.generar_diccionario_cruz()
        self.caminos_llegada = {
            "Verde": [(4, 4), (4, 5), (4, 6), (4, 7)],
            "Azul": [(6, 4), (6, 5), (6, 6), (6, 7)],
            "Amarillo": [(4, 6), (5, 6), (6, 6), (7, 6)],
            "Rojo": [(4, 4), (5, 4), (6, 4), (7, 4)]
        }
        self.salidas = {
            "Verde": 0,
            "Azul": 14,
            "Amarillo": 24,
            "Rojo": 34
        }

    def dibujar(self, pantalla, jugadores=None):
        N = 19
        c = self.celda
        COLOR_CUADRO = (220, 220, 220)
        COLOR_BORDE = (0, 0, 0)
        COLOR_CRUZ = (173, 216, 230)
        num = 1
        for i in range(N):
            for j in range(N):
                x = i * c
                y = j * c
                if num in self.mapeo_logica_a_cuadricula.values():
                    color = COLOR_CRUZ
                else:
                    color = COLOR_CUADRO
                pygame.draw.rect(pantalla, color, (x, y, c, c))
                pygame.draw.rect(pantalla, COLOR_BORDE, (x, y, c, c), 1)
                num += 1
        self.dibujar_carceles(pantalla, c)
        if jugadores:
            self.dibujar_fichas(pantalla, jugadores)

    def dibujar_carceles(self, pantalla, c):
        N = 19
        carceles = [
            (0, 0, (34, 139, 34, 150)),
            (N-4, 0, (30, 144, 255, 150)),
            (0, N-4, (255, 215, 0, 150)),
            (N-4, N-4, (220, 20, 60, 150))
        ]
        for x_base, y_base, color in carceles:
            surf = pygame.Surface((4 * c, 4 * c), pygame.SRCALPHA)
            surf.fill(color)
            pantalla.blit(surf, (x_base * c, y_base * c))
            pygame.draw.rect(pantalla, (0,0,0), (x_base * c, y_base * c, 4 * c, 4 * c), 3)
            for fila in range(2):
                for col in range(2):
                    x = x_base * c + (col + 1) * c + c // 2
                    y = y_base * c + (fila + 1) * c + c // 2
                    radio = c // 4
                    pygame.draw.circle(pantalla, (0,0,0), (int(x), int(y)), radio, 2)

    def dibujar_camino_principal(self, pantalla, c):
        fuente_celda = pygame.font.Font(None, 14)
        for i in range(11):
            for j in range(11):
                x = i * c
                y = j * c
                if not ((i < 4 and j < 4) or
                        (i >= 7 and j < 4) or
                        (i < 4 and j >= 7) or
                        (i >= 7 and j >= 7)):
                    pygame.draw.rect(pantalla, BLANCO, (x, y, c, c))
                    pygame.draw.rect(pantalla, NEGRO, (x, y, c, c), 1)
                    numero_celda = self.obtener_numero_celda(i, j)
                    if numero_celda is not None:
                        texto = fuente_celda.render(str(numero_celda), True, NEGRO)
                        texto_rect = texto.get_rect(center=(x + c // 2, y + c // 2))
                        pantalla.blit(texto, texto_rect)

    def dibujar_caminos_llegada(self, pantalla, c):
        for i in range(4):
            x = i * c
            y = 3 * c
            pygame.draw.rect(pantalla, VERDE, (x, y, c, c))
            pygame.draw.rect(pantalla, NEGRO, (x, y, c, c), 1)
        for i in range(4):
            x = (10 - i) * c
            y = 7 * c
            pygame.draw.rect(pantalla, AZUL, (x, y, c, c))
            pygame.draw.rect(pantalla, NEGRO, (x, y, c, c), 1)
        for i in range(4):
            x = 3 * c
            y = (10 - i) * c
            pygame.draw.rect(pantalla, AMARILLO, (x, y, c, c))
            pygame.draw.rect(pantalla, NEGRO, (x, y, c, c), 1)
        for i in range(4):
            x = 7 * c
            y = i * c
            pygame.draw.rect(pantalla, ROJO, (x, y, c, c))
            pygame.draw.rect(pantalla, NEGRO, (x, y, c, c), 1)

    def dibujar_centro(self, pantalla, c):
        x_meta = 5 * c
        y_meta = 5 * c
        pygame.draw.rect(pantalla, (255, 200, 150), (x_meta, y_meta, c, c))
        pygame.draw.rect(pantalla, NEGRO, (x_meta, y_meta, c, c), 3)
        fuente = pygame.font.Font(None, 20)
        texto = fuente.render("META", True, NEGRO)
        texto_rect = texto.get_rect(center=(x_meta + c // 2, y_meta + c // 2))
        pantalla.blit(texto, texto_rect)

    def dibujar_etiquetas(self, pantalla, c):
        fuente = pygame.font.Font(None, 16)
        jugadores_info = [
            (1, 1, "Jugador A", VERDE),
            (8, 1, "Jugador B", AZUL),
            (1, 8, "Jugador C", AMARILLO),
            (8, 8, "Jugador D", ROJO)
        ]
        for x, y, nombre, color in jugadores_info:
            texto = fuente.render(nombre, True, NEGRO)
            texto_rect = texto.get_rect(center=(x * c + c // 2, y * c + c // 2))
            pantalla.blit(texto, texto_rect)
        texto = fuente.render("PASILLO", True, NEGRO)
        texto_rect = texto.get_rect(center=(2 * c + c // 2, 5 * c + c // 2))
        pantalla.blit(texto, texto_rect)

    def obtener_numero_celda(self, i, j):
        for numero, (x, y) in self.posiciones.items():
            if x == i and y == j:
                return numero
        for color, camino in self.caminos_llegada.items():
            for idx, (x, y) in enumerate(camino):
                if x == i and y == j:
                    return f"{color[0]}{idx+1}"
        return None

    def obtener_coordenadas_posicion(self, posicion, c):
        if posicion in self.posiciones:
            x, y = self.posiciones[posicion]
            return x * c + c // 2, y * c + c // 2
        return 5 * c + c // 2, 5 * c + c // 2

    mapeo_logica_a_cuadricula = {
        1: 153, 2: 154, 3: 155, 4: 156, 5: 157, 6: 158, 7: 159, 8: 160,
        9: 142, 10: 123, 11: 104, 12: 85, 13: 66, 14: 47, 15: 28, 16: 9,
        17: 10,
        18: 11, 19: 30, 20: 49, 21: 68, 22: 87, 23: 106, 24: 125, 25: 144,
        26: 164, 27: 165, 28: 166, 29: 167, 30: 168, 31: 169, 32: 170, 33: 171,
        34: 190,
        35: 209, 36: 208, 37: 207, 38: 206, 39: 205, 40: 204, 41: 203, 42: 202,
        43: 220, 44: 239, 45: 258, 46: 277, 47: 296, 48: 315, 49: 334, 50: 353,
        51: 352,
        52: 351, 53: 332, 54: 313, 55: 294, 56: 275, 57: 256, 58: 237, 59: 218,
        60: 198, 61: 197, 62: 196, 63: 195, 64: 194, 65: 193, 66: 192, 67: 191,
        68: 172
    }

    def dibujar_fichas(self, pantalla, jugadores):
        c = self.celda
        N = 19
        for idx, jugador in enumerate(jugadores):
            for j, ficha in enumerate(jugador.fichas):
                if hasattr(ficha, 'posicion') and isinstance(ficha.posicion, int) and 1 <= ficha.posicion <= 68:
                    celda_ficha = self.mapeo_logica_a_cuadricula[ficha.posicion]
                    i_ficha = (celda_ficha - 1) % N
                    j_ficha = (celda_ficha - 1) // N
                    x_ficha = i_ficha * c + c // 2
                    y_ficha = j_ficha * c + c // 2
                    color = self.convertir_color(getattr(ficha, 'color', 'Rojo'))
                    radio = c // 2 - 2
                    pygame.draw.circle(pantalla, color, (x_ficha, y_ficha), radio)
                    pygame.draw.circle(pantalla, (0,0,0), (x_ficha, y_ficha), radio, 2)
                elif hasattr(ficha, 'posicion') and ficha.posicion == -1:
                    self.dibujar_ficha_carcel(pantalla, ficha, idx, j, c)

    def dibujar_ficha_carcel(self, pantalla, ficha, jugador_idx, ficha_idx, c):
        N = 19
        color_a_carcel = {
            'Verde': (0, 0),
            'Azul': (N-4, 0),
            'Amarillo': (0, N-4),
            'Rojo': (N-4, N-4)
        }
        color_nombre = getattr(ficha, 'color', 'Rojo')
        x_base, y_base = color_a_carcel.get(color_nombre, (N-4, N-4))
        fila = ficha_idx // 2
        col = ficha_idx % 2
        x = x_base * c + (col + 1) * c + c // 2
        y = y_base * c + (fila + 1) * c + c // 2
        radio = c // 4
        color_rgb = self.convertir_color(color_nombre)
        pygame.draw.circle(pantalla, color_rgb, (int(x), int(y)), radio)
        pygame.draw.circle(pantalla, (0,0,0), (int(x), int(y)), radio, 2)

    def dibujar_ficha_llegada(self, pantalla, ficha, jugador_idx, ficha_idx, c):
        llegadas = [
            (6, 5),
            (9, 6),
            (5, 8),
            (8, 9)
        ]
        x_base, y_base = llegadas[jugador_idx]
        radio = c // 6
        if jugador_idx == 0:
            x = x_base * c + c // 2
            y = (y_base - ficha_idx) * c + c // 2
        elif jugador_idx == 1:
            x = (x_base + ficha_idx) * c + c // 2
            y = y_base * c + c // 2
        elif jugador_idx == 2:
            x = (x_base - ficha_idx) * c + c // 2
            y = y_base * c + c // 2
        else:
            x = x_base * c + c // 2
            y = (y_base + ficha_idx) * c + c // 2
        color_rgb = self.convertir_color(ficha.color)
        pygame.draw.circle(pantalla, color_rgb, (x, y), radio)
        pygame.draw.circle(pantalla, NEGRO, (x, y), radio, 2)

    def dibujar_ficha_tablero(self, pantalla, ficha, c):
        radio = c // 4
        x, y = self.obtener_coordenadas_posicion(ficha.posicion, c)
        if x is not None and y is not None:
            color_rgb = self.convertir_color(ficha.color)
            pygame.draw.circle(pantalla, color_rgb, (int(x), int(y)), radio)
            pygame.draw.circle(pantalla, NEGRO, (int(x), int(y)), radio, 2)
            pygame.draw.circle(pantalla, NEGRO, (int(x), int(y)), 3)

    def convertir_color(self, color_str):
        colores = {
            "Rojo": ROJO,
            "Verde": VERDE,
            "Azul": AZUL,
            "Amarillo": AMARILLO
        }
        return colores.get(color_str, NEGRO)
