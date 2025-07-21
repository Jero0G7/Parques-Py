from jugador import Jugador
from dados import lanzar_dados, es_par
from tablero import Tablero
from consola import mostrar_tablero

def usar_movimientos_extra(jugador, tablero, cantidad):
    print(f"\n {jugador.nombre} tiene {cantidad} movimientos extra")
    movimientos_usados = 0
    while movimientos_usados < cantidad:
        fichas_movibles = [f for f in jugador.fichas if f.posicion >= 0 and not f.en_llegada]
        if not fichas_movibles:
            break
        ficha = fichas_movibles[0]
        tablero.mover_ficha(ficha, 1)
        movimientos_usados += 1
        print(f"{jugador.nombre} movió una ficha extra ({movimientos_usados}/{cantidad})")

def turno(jugador, tablero):
    repetir = True
    while repetir:
        print(f"\nTurno de {jugador.nombre}")
        d1, d2 = lanzar_dados()
        print(f"Lanzó: {d1} y {d2}")

        movimientos_extra = 0
        jugador.ultima_ficha_movida = None

        if d1 == 5 or d2 == 5 or (d1 + d2) == 5:
            for ficha in jugador.fichas:
                if ficha.posicion == -1:
                    ficha.sacar_de_la_carcel()
                    tablero.agregar_ficha(ficha)
                    print(f"{jugador.nombre} sacó una ficha de la cárcel.")
                    break

        fichas_disponibles = [f for f in jugador.fichas if f.posicion != -1 and not f.en_llegada]

        if len(fichas_disponibles) == 1:
            ficha = fichas_disponibles[0]
            print(f"Solo hay una ficha disponible. Se moverá automáticamente.")
        elif len(fichas_disponibles) > 1:
            print("Fichas disponibles para mover:")
            for idx, f in enumerate(fichas_disponibles):
                print(f"{idx + 1}. Ficha en posición {f.posicion}")
            while True:
                try:
                    seleccion = int(input("Elige el número de la ficha que deseas mover: "))
                    if 1 <= seleccion <= len(fichas_disponibles):
                        ficha = fichas_disponibles[seleccion - 1]
                        break
                    else:
                        print("Opción inválida. Intenta de nuevo.")
                except ValueError:
                    print("Por favor ingresa un número.")
        else:
            ficha = None

        if ficha:
            capturo, llego = tablero.mover_ficha(ficha, d1 + d2)
            jugador.ultima_ficha_movida = ficha
            if capturo:
                movimientos_extra += 20
            if llego:
                movimientos_extra += 10

        if movimientos_extra > 0:
            usar_movimientos_extra(jugador, tablero, movimientos_extra)

        if es_par(d1, d2):
            jugador.pares_consecutivos += 1
            print(f"{jugador.nombre} sacó un par. ¡Repite turno! ({jugador.pares_consecutivos} consecutivos)")

            if jugador.pares_consecutivos == 3:
                if jugador.ultima_ficha_movida:
                    jugador.ultima_ficha_movida.enviar_a_la_carcel()
                    print(f" ¡{jugador.nombre} sacó 3 pares! Su última ficha fue enviada a la cárcel.")
                jugador.pares_consecutivos = 0
                repetir = False
            else:
                repetir = True
        else:
            jugador.pares_consecutivos = 0
            repetir = False

        mostrar_tablero([jugador])

def juego():
    print(" Bienvenido a Parqués UN ")
    num_jugadores = 4
    colores_disponibles = ["rojo", "azul", "verde", "amarillo"]
    jugadores = []

    for i in range(num_jugadores):
        nombre = input(f"\nNombre del jugador {i+1}: ")
        print("Colores disponibles:", ", ".join(colores_disponibles))
        while True:
            color = input(f"{nombre}, elige un color: ").lower()
            if color in colores_disponibles:
                colores_disponibles.remove(color)
                break
            else:
                print("Color no disponible. Intenta de nuevo.")
        jugador = Jugador(nombre, color)
        jugadores.append(jugador)

    tablero = Tablero()
    turno_actual = 0

    while True:
        turno(jugadores[turno_actual], tablero)

        if jugadores[turno_actual].todas_en_llegada():
            print(f"\n ¡{jugadores[turno_actual].nombre} ha ganado el juego!")
            break

        turno_actual = (turno_actual + 1) % len(jugadores)

if __name__ == "__main__":
    juego()
