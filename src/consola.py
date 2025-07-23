def mostrar_tablero(jugadores, tablero):
    casillas = ["--" for _ in range(68)]

    for jugador in jugadores:
        inicial = jugador.color[0].upper()
        for i, ficha in enumerate(jugador.fichas):
            if ficha.posicion >= 0 and ficha.posicion < 68:
                if casillas[ficha.posicion] == "--":
                    casillas[ficha.posicion] = f"{inicial}{i+1}"
                else:
                    casillas[ficha.posicion] += f"/{inicial}{i+1}"

    print("\n🧭 Estado del tablero (casillas 0–67):")
    for i in range(0, 68, 10):
        fila = casillas[i:i+10]
        print(f"{i:2d}-{i+9:2d}:", " ".join(fila))

    print("\n🟢 Casillas seguras:")
    print(", ".join(str(c) for c in tablero.seguras))

    print("\n🚪 Casillas de salida:")
    for color, pos in tablero.salidas.items():
        print(f"  {color}: {pos}")

    print("\n🏁 Zonas de llegada:")
    for color, zona in tablero.zonas_llegada.items():
        fichas_zona = []
        for i, ficha in enumerate(zona):
            if ficha:
                fichas_zona.append(f"{color[0].upper()}{ficha.id}(pos {i})")
        if fichas_zona:
            print(f"  {color}: " + ", ".join(fichas_zona))

    print("\n🚧 Fichas en la cárcel:")
    for jugador in jugadores:
        en_carcel = [f for f in jugador.fichas if f.posicion == -1]
        if en_carcel:
            fichas_str = ", ".join(f"{jugador.color[0].upper()}{jugador.color[1].upper()}{f.id}" for f in en_carcel)
            print(f"  {jugador.color}: {fichas_str}")

    print("\n" + "-"*60)

def mostrar_fichas_llegadas(jugadores):
    print("\n🎯 Progreso de llegada:")
    for j in jugadores:
        cantidad = sum(1 for f in j.fichas if f.en_llegada)
        print(f"  {j.color}: {cantidad}/4 fichas llegaron")
