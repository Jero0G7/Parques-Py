class Tablero:
    def __init__(self):
        self.casillas = [[] for _ in range(68)]
        self.seguras = [5, 12, 17, 22, 29, 34, 39, 46, 51, 56, 63, 67]  

    def agregar_ficha(self, ficha):
        if ficha.posicion != -1 and ficha.posicion < 68:
            self.casillas[ficha.posicion].append(ficha)

    def hay_bloqueo(self, desde, pasos, color_ficha):
        for i in range(desde + 1, desde + pasos + 1):
            if i >= 68:
                break
            casilla = self.casillas[i]
            if len(casilla) == 2:
                colores = set(f.color for f in casilla)
                if len(colores) == 1 or i in self.seguras:
                    return True
        return False

    def mover_ficha(self, ficha, pasos):
        if ficha.posicion == -1 or ficha.en_llegada:
            return False, False

        desde = ficha.posicion
        nueva_pos = desde + pasos

        if nueva_pos >= 68:
            nueva_pos = 67

        if self.hay_bloqueo(desde, pasos, ficha.color):
            print(f"No se puede mover ficha {ficha.color}: hay un bloqueo.")
            return False, False

        capturada = False
        otras_fichas = self.casillas[nueva_pos]

        for otra in otras_fichas:
            if otra.color != ficha.color and nueva_pos not in self.seguras:
                otra.enviar_a_la_carcel()
                otras_fichas.remove(otra)
                capturada = True
                print(f"{ficha.color} capturó a una ficha de {otra.color}")

        if desde < 68:
            self.casillas[desde].remove(ficha)
        self.casillas[nueva_pos].append(ficha)
        ficha.posicion = nueva_pos

        llego = False
        if ficha.posicion >= 67:
            ficha.en_llegada = True
            self.casillas[ficha.posicion].remove(ficha)
            ficha.posicion = -2
            llego = True
            print(f"Ficha {ficha.color} llegó a la meta 🎯")

        return capturada, llego
