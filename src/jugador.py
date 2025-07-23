from src.fichas import Ficha

class Jugador:
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.id = id
        self.fichas = [Ficha(color, i + 1) for i in range(4)]
        self.pares_consecutivos = 0
        self.ultima_ficha_movida = None  

    def todas_en_llegada(self):
        return all(f.en_llegada for f in self.fichas)

    def fichas_fuera(self):
        return [f for f in self.fichas if f.posicion != -1]