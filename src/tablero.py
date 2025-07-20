import pygame

class Tablero:
    def __init__(self):
        self.tamano = 600
        self.tamano_celda = self.tamano // 15  # Dividimos el tablero en 15x15 celdas
        self.colores = {
            'blanco': (255, 255, 255),
            'negro': (0, 0, 0)
        }
        
    def dibujar(self, pantalla):
        # Fondo del tablero
        pantalla.fill(self.colores['blanco'])
        
        # Dibujar el borde exterior del tablero
        pygame.draw.rect(pantalla, self.colores['negro'], (0, 0, self.tamano, self.tamano), 2)
        
        # Dibujar las áreas de las esquinas (blancas)
        self.dibujar_esquinas(pantalla)
        
        # Dibujar el recorrido central
        self.dibujar_recorrido_central(pantalla)
        
        # Dibujar las etiquetas
        self.dibujar_etiquetas(pantalla)
        
    def dibujar_esquinas(self, pantalla):
        # Esquina superior izquierda (blanca)
        pygame.draw.rect(pantalla, self.colores['blanco'], (0, 0, self.tamano_celda * 3, self.tamano_celda * 3))
        pygame.draw.rect(pantalla, self.colores['negro'], (0, 0, self.tamano_celda * 3, self.tamano_celda * 3), 2)
        
        # Esquina superior derecha (blanca)
        pygame.draw.rect(pantalla, self.colores['blanco'], 
                        (self.tamano - self.tamano_celda * 4, 0, self.tamano_celda * 4, self.tamano_celda * 4))
        pygame.draw.rect(pantalla, self.colores['negro'],
                        (self.tamano - self.tamano_celda * 4, 0, self.tamano_celda * 4, self.tamano_celda * 4), 2)
        
        # Esquina inferior izquierda (blanca)
        pygame.draw.rect(pantalla, self.colores['blanco'], 
                        (0, self.tamano - self.tamano_celda * 4, self.tamano_celda * 4, self.tamano_celda * 4))
        pygame.draw.rect(pantalla, self.colores['negro'],
                        (0, self.tamano - self.tamano_celda * 4, self.tamano_celda * 4, self.tamano_celda * 4), 2)
        
        # Esquina inferior derecha (blanca)
        pygame.draw.rect(pantalla, self.colores['blanco'], 
                        (self.tamano - self.tamano_celda * 4, self.tamano - self.tamano_celda * 4, 
                         self.tamano_celda * 4, self.tamano_celda * 4))
        pygame.draw.rect(pantalla, self.colores['negro'],
                        (self.tamano - self.tamano_celda * 4, self.tamano - self.tamano_celda * 4,
                         self.tamano_celda * 4, self.tamano_celda * 4), 2)
        
    def dibujar_recorrido_central(self, pantalla):
        # Dibujar la cruz central (3x3 en el centro)
        # Líneas verticales del centro
        for x in range(6, 9):
            pygame.draw.line(pantalla, self.colores['negro'],
                           (x * self.tamano_celda, 9 * self.tamano_celda),
                           (x * self.tamano_celda, 9 * self.tamano_celda))
        
        # Líneas horizontales del centro
        for y in range(6, 9):
            pygame.draw.line(pantalla, self.colores['negro'],
                           (6 * self.tamano_celda, y * self.tamano_celda),
                           (9 * self.tamano_celda, y * self.tamano_celda))
        
        # Dibujar las diagonales en el centro
        pygame.draw.line(pantalla, self.colores['negro'],
                        (6 * self.tamano_celda, 6 * self.tamano_celda),
                        (9 * self.tamano_celda, 9 * self.tamano_celda))
        pygame.draw.line(pantalla, self.colores['negro'],
                        (6 * self.tamano_celda, 9 * self.tamano_celda),
                        (9 * self.tamano_celda, 6 * self.tamano_celda))
        
        # Brazo superior (3x6)
        for x in range(3, 10):
            pygame.draw.line(pantalla, self.colores['negro'],
                           (x * self.tamano_celda * 1.5, 3),
                           (x * self.tamano_celda * 1.5, 6 * self.tamano_celda))
        """ for y in range(7):
            pygame.draw.line(pantalla, self.colores['negro'],
                           (6 * self.tamano_celda, y * self.tamano_celda),
                           (9 * self.tamano_celda, y * self.tamano_celda)) """
        
        # Brazo inferior (3x6)
        for x in range(6, 9):
            pygame.draw.line(pantalla, self.colores['negro'],
                           (x * self.tamano_celda, 9 * self.tamano_celda),
                           (x * self.tamano_celda, self.tamano))
        for y in range(9, 15):
            pygame.draw.line(pantalla, self.colores['negro'],
                           (6 * self.tamano_celda, y * self.tamano_celda),
                           (9 * self.tamano_celda, y * self.tamano_celda))
        
        # Brazo izquierdo (6x3)
        for x in range(7):
            pygame.draw.line(pantalla, self.colores['negro'],
                           (x * self.tamano_celda, 6 * self.tamano_celda),
                           (x * self.tamano_celda, 9 * self.tamano_celda))
        for y in range(6, 9):
            pygame.draw.line(pantalla, self.colores['negro'],
                           (0, y * self.tamano_celda),
                           (6 * self.tamano_celda, y * self.tamano_celda))
        
        # Brazo derecho (6x3)
        for x in range(9, 15):
            pygame.draw.line(pantalla, self.colores['negro'],
                           (x * self.tamano_celda, 6 * self.tamano_celda),
                           (x * self.tamano_celda, 9 * self.tamano_celda))
        for y in range(6, 9):
            pygame.draw.line(pantalla, self.colores['negro'],
                           (9 * self.tamano_celda, y * self.tamano_celda),
                           (self.tamano, y * self.tamano_celda))
    
    def dibujar_etiquetas(self, pantalla):
        fuente = pygame.font.Font(None, 20)
        fuente_pequena = pygame.font.Font(None, 16)
        
        # "Fichas equipo 1" en la esquina inferior izquierda
        texto_fichas = fuente.render("Fichas equipo 1", True, self.colores['negro'])
        texto_rect = texto_fichas.get_rect(center=(2 * self.tamano_celda, 
                                                  self.tamano - 2 * self.tamano_celda))
        pantalla.blit(texto_fichas, texto_rect)
        
        # "Seguro" en el brazo derecho (vertical, rotado)
        texto_seguro_der = fuente_pequena.render("Seguro", True, self.colores['negro'])
        texto_rotado_der = pygame.transform.rotate(texto_seguro_der, 90)
        texto_rect = texto_rotado_der.get_rect(center=(10 * self.tamano_celda + self.tamano_celda//2,
                                                      7 * self.tamano_celda + self.tamano_celda//2))
        pantalla.blit(texto_rotado_der, texto_rect)
        
        # "Llegada 1" en el centro (vertical, rotado)
        texto_llegada = fuente_pequena.render("Llegada 1", True, self.colores['negro'])
        texto_rotado_llegada = pygame.transform.rotate(texto_llegada, 90)
        texto_rect = texto_rotado_llegada.get_rect(center=(7 * self.tamano_celda + self.tamano_celda//2,
                                                          7 * self.tamano_celda + self.tamano_celda//2))
        pantalla.blit(texto_rotado_llegada, texto_rect)
        
        # "Seguro" en el brazo derecho inferior (vertical, rotado)
        texto_seguro_der_inf = fuente_pequena.render("Seguro", True, self.colores['negro'])
        texto_rotado_der_inf = pygame.transform.rotate(texto_seguro_der_inf, 90)
        texto_rect = texto_rotado_der_inf.get_rect(center=(10 * self.tamano_celda + self.tamano_celda//2,
                                                          13 * self.tamano_celda + self.tamano_celda//2))
        pantalla.blit(texto_rotado_der_inf, texto_rect)
        
        # "Salida 1" en el brazo derecho inferior (vertical, rotado)
        texto_salida = fuente_pequena.render("Salida 1", True, self.colores['negro'])
        texto_rotado_salida = pygame.transform.rotate(texto_salida, 90)
        texto_rect = texto_rotado_salida.get_rect(center=(7 * self.tamano_celda + self.tamano_celda//2,
                                                         13 * self.tamano_celda + self.tamano_celda//2))
        pantalla.blit(texto_rotado_salida, texto_rect)
        
        # "Seguro" en el brazo inferior (horizontal, rotado)
        texto_seguro_inf = fuente_pequena.render("Seguro", True, self.colores['negro'])
        texto_rotado_inf = pygame.transform.rotate(texto_seguro_inf, 90)
        texto_rect = texto_rotado_inf.get_rect(center=(13 * self.tamano_celda + self.tamano_celda//2,
                                                      7 * self.tamano_celda + self.tamano_celda//2))
        pantalla.blit(texto_rotado_inf, texto_rect)