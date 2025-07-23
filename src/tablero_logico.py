class Tablero:
    def __init__(self):
        self.casillas = [[] for _ in range(68)]
        self.seguras = [5, 12, 17, 22, 29, 34, 39, 46, 51, 56, 63, 67]

        self.salidas = {
            "Rojo": 0,
            "Azul": 17,
            "Verde": 34,
            "Amarillo": 51
        }

        self.entrada_llegada = {
            "Rojo": 67,
            "Azul": 16,
            "Verde": 33,
            "Amarillo": 50
        }

        self.zonas_llegada = {
            "Rojo": [None] * 8,
            "Azul": [None] * 8,
            "Verde": [None] * 8,
            "Amarillo": [None] * 8
        } 

    def agregar_ficha(self, ficha):
        if ficha.posicion != -1 and ficha.posicion < 68:
            self.casillas[ficha.posicion].append(ficha)

    def hay_bloqueo(self, desde, pasos, color_ficha):
        for i in range(1, pasos + 1):
            pos = (desde + i) % 68
            casilla = self.casillas[pos]

            if len(casilla) >= 2:
                colores = set(f.color for f in casilla)
                if len(colores) == 1 or pos in self.seguras:
                    print(f"Bloqueo detectado en casilla {pos}")
                    return True
        return False

    def mover_ficha(self, ficha, pasos):
        if ficha.posicion == -1:
            return False, False, None

        if ficha.en_llegada:
            zona = self.zonas_llegada[ficha.color]
            idx_actual = ficha.posicion
            nueva_pos = idx_actual + pasos

            if nueva_pos >= 8:
                return False, False, "❌ Movimiento inválido: se pasa de la meta."

            if zona[nueva_pos] is not None:
                return False, False, f"❌ Movimiento inválido: casilla {nueva_pos} de la llegada está ocupada."

            zona[idx_actual] = None
            zona[nueva_pos] = ficha
            ficha.posicion = nueva_pos

            if nueva_pos == 7:
                return False, True, f"🎉 Ficha {ficha.color} llegó a la meta final en la zona de llegada."
            else:
                return False, False, f"➡️ Ficha {ficha.color} avanzó en zona de llegada a posición {nueva_pos}."

        desde = ficha.posicion
        nueva_pos = desde + pasos

        if self.hay_bloqueo(desde, pasos, ficha.color):
            return False, False, f"❌ No se puede mover ficha {ficha.color}: hay un bloqueo."

        capturada = False
        mensaje_captura = None

        entrada = self.entrada_llegada[ficha.color]
        if desde <= entrada < desde + pasos:
            pasos_a_entrada = entrada - desde
            if pasos == pasos_a_entrada + 1:
                zona = self.zonas_llegada[ficha.color]
                for i in range(len(zona)):
                    if zona[i] is None:
                        zona[i] = ficha
                        ficha.en_llegada = True
                        ficha.posicion = i
                        if desde < 68:
                            self.casillas[desde].remove(ficha)
                        return capturada, True, f"🏁 Ficha {ficha.color} entró a la zona de llegada en la posición {i}"
                return False, False, "❌ Zona de llegada llena. No se puede mover."

        if nueva_pos >= 68:
            nueva_pos %= 68

        otras_fichas = self.casillas[nueva_pos]
        for otra in otras_fichas[:]:
            if otra.color != ficha.color and nueva_pos not in self.seguras:
                otra.enviar_a_la_carcel()
                otras_fichas.remove(otra)
                capturada = True
                mensaje_captura = f"⚔️ {ficha.color} capturó a una ficha de {otra.color}"

        if desde < 68:
            self.casillas[desde].remove(ficha)
        self.casillas[nueva_pos].append(ficha)
        ficha.posicion = nueva_pos

        return capturada, False, mensaje_captura

