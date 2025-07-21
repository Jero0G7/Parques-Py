def mostrar_tablero(jugadores):
    tablero = ["--" for _ in range(68)]

    for jugador in jugadores:
        inicial = jugador.color[0].upper()
        for i, ficha in enumerate(jugador.fichas):
            if ficha.posicion >= 0 and ficha.posicion < 68:
                if tablero[ficha.posicion] == "--":
                    tablero[ficha.posicion] = f"{inicial}{i+1}"
                else:
                    tablero[ficha.posicion] += f"/{inicial}{i+1}"

    print("\n Estado del tablero:")
    for i in range(0, 68, 10):
        fila = tablero[i:i+10]
        print(" ".join(fila))
