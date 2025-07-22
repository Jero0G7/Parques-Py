class Ficha:
    def __init__(self, color, id):
        self.color = color
        self.id = id
        self.posicion = None  # None = cárcel, int = casilla, "llegada" = meta

    def __str__(self):
        return f"{self.color[0].upper()}{self.id}"
