# reglas.py

CASILLAS_SEGURAS = [5, 12, 17, 22, 29, 34, 39, 46, 51, 56, 63, 68]

def puede_sacar_ficha(d1, d2):
    return d1 == 5 or d2 == 5 or d1 + d2 == 5

def hay_bloqueo(casilla, tablero):
    fichas = tablero.get(casilla, [])
    if len(fichas) < 2:
        return False
    colores = {f.color for f in fichas}
    return len(colores) == 1 or casilla in CASILLAS_SEGURAS

def mover_ficha(jugador, ficha, pasos, tablero):
    actual = ficha.posicion

    if ficha.posicion is None:
        if pasos == 5:
            destino = 1
            if not hay_bloqueo(destino, tablero):
                ficha.posicion = destino
                agregar_a_tablero(ficha, tablero)
                jugador.ultima_ficha_movida = ficha
                print(f"{ficha} sale de la cárcel a la casilla 1")
                return None
            else:
                print("Salida bloqueada")
        else:
            print("Necesitas un 5 para sacar ficha")
        return None

    if ficha.posicion == "llegada":
        print(f"{ficha} ya está en la meta.")
        return None

    destino = ficha.posicion + pasos
    if destino > 68:
        print("Movimiento excede la meta")
        return None
    elif destino == 68:
        remover_de_tablero(ficha, ficha.posicion, tablero)
        ficha.posicion = "llegada"
        print(f"{ficha} llegó a la meta 🎉 (+10 movimientos)")
        jugador.ultima_ficha_movida = ficha
        return "llegada"

    if hay_bloqueo(destino, tablero):
        print(f"Bloqueo en la casilla {destino}")
        return None

    remover_de_tablero(ficha, ficha.posicion, tablero)
    ficha.posicion = destino
    resultado = verificar_captura(ficha, tablero)
    agregar_a_tablero(ficha, tablero)
    jugador.ultima_ficha_movida = ficha
    return resultado

def verificar_captura(ficha, tablero):
    casilla = ficha.posicion
    ocupantes = tablero.get(casilla, [])
    enemigos = [f for f in ocupantes if f.color != ficha.color and f.posicion not in (None, "llegada")]

    if len(enemigos) == 1:
        enemigo = enemigos[0]
        enemigo.posicion = None
        remover_de_tablero(enemigo, casilla, tablero)
        print(f"{ficha} capturó a {enemigo} (+20 movimientos)")
        return "captura"
    return None

def agregar_a_tablero(ficha, tablero):
    pos = ficha.posicion
    if isinstance(pos, int):
        if pos not in tablero:
            tablero[pos] = []
        tablero[pos].append(ficha)

def remover_de_tablero(ficha, pos, tablero):
    if isinstance(pos, int) and pos in tablero:
        if ficha in tablero[pos]:
            tablero[pos].remove(ficha)
        if not tablero[pos]:
            del tablero[pos]

def hay_ganador(jugador):
    return jugador.todas_en_llegada()
