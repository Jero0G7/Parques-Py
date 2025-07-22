from ficha import Ficha

class Jugador: 
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.fichas = [Ficha(color, i + 1) for i in range(4)]
        self.movimientos_extra = 0

    def fichas_en_juego(self):
        return [f for f in self.fichas if isinstance(f.posicion, int)]

    def fichas_en_carcel(self):
        return [f for f in self.fichas if f.posicion is None]

    def fichas_en_llegada(self):
        return [f for f in self.fichas if f.posicion == "llegada"]
