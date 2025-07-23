import pygame
import time
import sys
from src.jugador import Jugador
from src.dados import lanzar_dados, es_par
from src.tablero_logico import Tablero
from src.consola import mostrar_fichas_llegadas, mostrar_tablero
from src.tablero_grafico import Tablero as TableroGrafico

MODO_DESARROLLO = False

pygame.init()
ANCHO_VENTANA = 600
ALTO_VENTANA = 800
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Parqués - Juego Completo")
tablero_grafico = TableroGrafico()

FUENTE_CONSOLA = pygame.font.Font(None, 20)
FUENTE_TITULO = pygame.font.Font(None, 32)
COLOR_FONDO = (240, 240, 240)
COLOR_TEXTO = (0, 0, 0)
COLOR_CONSOLA = (50, 50, 50)
COLOR_INPUT = (255, 255, 255)

class ConsolaIntegrada:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.lineas = []
        self.input_texto = ""
        self.input_activo = False
        self.max_lineas = 12
        self.scroll_offset = 0
        self.lineas_por_pagina = 8
        self.auto_scroll = True
        
    def agregar_mensaje(self, mensaje, color=(255, 255, 255)):
        self.lineas.append((mensaje, color))
        if self.auto_scroll and len(self.lineas) > self.lineas_por_pagina:
            self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)
    
    def obtener_input(self, prompt=""):
        if prompt:
            self.agregar_mensaje(prompt)
            self.dibujar()
            pygame.display.flip()
        
        self.input_activo = True
        self.input_texto = ""
        
        while self.input_activo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if self.input_texto.strip():
                            texto = self.input_texto
                            self.input_texto = ""
                            self.input_activo = False
                            self.agregar_mensaje(f"> {texto}")
                            if self.auto_scroll and len(self.lineas) > self.lineas_por_pagina:
                                self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)
                            pygame.time.wait(100)
                            return texto
                    elif evento.key == pygame.K_BACKSPACE:
                        self.input_texto = self.input_texto[:-1]
                    elif evento.key == pygame.K_ESCAPE:
                        self.input_texto = ""
                        self.input_activo = False
                        pygame.time.wait(100)
                        return ""
                    elif evento.key == pygame.K_UP:
                        if self.scroll_offset > 0:
                            self.scroll_offset -= 1
                            self.auto_scroll = False
                    elif evento.key == pygame.K_DOWN:
                        if self.scroll_offset < max(0, len(self.lineas) - self.lineas_por_pagina):
                            self.scroll_offset += 1
                            if self.scroll_offset >= max(0, len(self.lineas) - self.lineas_por_pagina):
                                self.auto_scroll = True
                    elif evento.key == pygame.K_PAGEUP:
                        self.scroll_offset = max(0, self.scroll_offset - 3)
                        self.auto_scroll = False
                    elif evento.key == pygame.K_PAGEDOWN:
                        self.scroll_offset = min(len(self.lineas) - self.lineas_por_pagina, self.scroll_offset + 3)
                        if self.scroll_offset >= max(0, len(self.lineas) - self.lineas_por_pagina):
                            self.auto_scroll = True
                    elif evento.key == pygame.K_HOME:
                        self.scroll_offset = 0
                        self.auto_scroll = False
                    elif evento.key == pygame.K_END:
                        self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)
                        self.auto_scroll = True
                    elif evento.unicode.isprintable():
                        self.input_texto += evento.unicode
            self.dibujar()
            pygame.display.flip()
            pygame.time.wait(10)
    
    def dibujar(self):
        pygame.draw.rect(pantalla, COLOR_CONSOLA, (self.x, self.y, self.ancho, self.alto))
        pygame.draw.rect(pantalla, (100, 100, 100), (self.x, self.y, self.ancho, self.alto), 2)
        
        area_historial = self.alto - 30
        
        if self.lineas:
            y_offset = 10
            
            inicio = self.scroll_offset
            fin = min(inicio + self.lineas_por_pagina, len(self.lineas))
            lineas_a_mostrar = self.lineas[inicio:fin]
            
            if len(self.lineas) > self.lineas_por_pagina:
                scroll_info = f"📜 {inicio + 1}-{fin} de {len(self.lineas)}"
                scroll_surface = FUENTE_CONSOLA.render(scroll_info, True, (200, 200, 200))
                pantalla.blit(scroll_surface, (self.x + self.ancho - 120, self.y + 5))
            
            for mensaje, color in lineas_a_mostrar:
                if y_offset < area_historial - 10:
                    if len(mensaje) > 65:
                        mensaje = mensaje[:62] + "..."
                    texto_surface = FUENTE_CONSOLA.render(mensaje, True, color)
                    pantalla.blit(texto_surface, (self.x + 10, self.y + y_offset))
                    y_offset += 18
        
        pygame.draw.line(pantalla, (100, 100, 100), 
                        (self.x + 5, self.y + area_historial), 
                        (self.x + self.ancho - 5, self.y + area_historial), 2)
        
        if self.input_activo:
            input_surface = FUENTE_CONSOLA.render(f"> {self.input_texto}", True, (255, 255, 255))
            pantalla.blit(input_surface, (self.x + 10, self.y + area_historial + 5))

consola = ConsolaIntegrada(20, 620, 560, 180)

if len(consola.lineas) > consola.lineas_por_pagina:
    consola.scroll_offset = max(0, len(consola.lineas) - consola.lineas_por_pagina)

def actualizar_visualizacion(jugadores, tablero):
    pantalla.fill(COLOR_FONDO)
    
    titulo = FUENTE_TITULO.render("🎲 PARQUÉS 🎲", True, COLOR_TEXTO)
    pantalla.blit(titulo, (20, 10))
    
    if jugadores:
        tablero_grafico.dibujar(pantalla, jugadores)
    else:
        tablero_grafico.dibujar(pantalla, [])
    
    consola.dibujar()
    
    pygame.display.flip()

def usar_movimientos_extra(jugador, tablero, jugadores, cantidad):
    consola.agregar_mensaje(f"🟡 {jugador.nombre} tiene {cantidad} movimientos extra")
    movimientos_usados = 0
    while movimientos_usados < cantidad:
        fichas_movibles = [f for f in jugador.fichas if f.posicion >= 0 and not f.en_llegada]
        if not fichas_movibles:
            break
        ficha = fichas_movibles[0]
        tablero.mover_ficha(ficha, 1)
        movimientos_usados += 1
        consola.agregar_mensaje(f"{jugador.nombre} movió una ficha extra ({movimientos_usados}/{cantidad})")
        actualizar_visualizacion(jugadores, tablero)
        time.sleep(0.5)

def turno(jugador, tablero, jugadores):
    repetir = True
    color_jugador = tablero_grafico.convertir_color(jugador.color)
    while repetir:
        consola.agregar_mensaje(f"Turno de {jugador.nombre}", color=color_jugador)
        
        try:
            d1, d2 = lanzar_dados(debug=MODO_DESARROLLO, input_func=consola.obtener_input)
            consola.agregar_mensaje(f"Lanzó: {d1} y {d2}", color=color_jugador)
        except (ValueError, TypeError):
            import random
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            consola.agregar_mensaje(f"Error en entrada de dados. Lanzó: {d1} y {d2}", color=color_jugador)

        movimientos_extra = 0
        jugador.ultima_ficha_movida = None

        if d1 == 5 or d2 == 5 or (d1 + d2) == 5:
            for ficha in jugador.fichas:
                if ficha.posicion == -1:
                    ficha.sacar_de_la_carcel()
                    tablero.agregar_ficha(ficha)
                    consola.agregar_mensaje(f"{jugador.nombre} sacó una ficha de la cárcel.", color=color_jugador)
                    actualizar_visualizacion(jugadores, tablero)
                    time.sleep(0.5)
                    break

        fichas_disponibles = [f for f in jugador.fichas if f.posicion != -1 and not f.en_llegada]

        if len(fichas_disponibles) == 1:
            ficha = fichas_disponibles[0]
            consola.agregar_mensaje(f"Solo puedes mover una ficha. La moveremos por ti.", color=color_jugador)
        elif len(fichas_disponibles) > 1:
            consola.agregar_mensaje("Las fichas que puedes mover son:", color=color_jugador)
            for idx, f in enumerate(fichas_disponibles):
                consola.agregar_mensaje(f"{idx + 1}. Ficha en posición {f.posicion}", color=color_jugador)
            while True:
                try:
                    seleccion = int(consola.obtener_input("¿Qué ficha quieres mover?"))
                    if 1 <= seleccion <= len(fichas_disponibles):
                        ficha = fichas_disponibles[seleccion - 1]
                        break
                    else:
                        consola.agregar_mensaje("Opción inválida. Elige las que ves en pantalla.", color=color_jugador)
                except ValueError:
                    consola.agregar_mensaje("Ingresa el número por favor.", color=color_jugador)
        else:
            ficha = None

        if ficha:
            capturo, llego, mensaje_evento = tablero.mover_ficha(ficha, d1 + d2)
            jugador.ultima_ficha_movida = ficha
            if mensaje_evento:
                consola.agregar_mensaje(mensaje_evento, color=color_jugador)
            if capturo:
                consola.agregar_mensaje(f"⚔️ {jugador.color} capturó una ficha enemiga (+20 movimientos)", color=color_jugador)
            if llego:
                consola.agregar_mensaje(f"🎉 {jugador.nombre} llegó a la meta con una ficha (+10 movimientos)", color=color_jugador)
            actualizar_visualizacion(jugadores, tablero)
            time.sleep(0.5)

        if movimientos_extra > 0:
            usar_movimientos_extra(jugador, tablero, jugadores, movimientos_extra)

        if es_par(d1, d2):
            jugador.pares_consecutivos += 1
            consola.agregar_mensaje(f"{jugador.nombre} sacó un par. ¡Repite turno! ({jugador.pares_consecutivos} consecutivos)", color=color_jugador)

            if jugador.pares_consecutivos == 3:
                if jugador.ultima_ficha_movida:
                    jugador.ultima_ficha_movida.enviar_a_la_carcel()
                    consola.agregar_mensaje(f"⚠️ ¡{jugador.nombre} sacó 3 pares! Su última ficha fue enviada a la cárcel.", color=color_jugador)
                jugador.pares_consecutivos = 0
                repetir = False
            else:
                repetir = True
        else:
            jugador.pares_consecutivos = 0
            repetir = False

        actualizar_visualizacion(jugadores, tablero)

def juego():
    consola.agregar_mensaje("🎲 Bienvenido, vamos a jugar Parqués! 🎲")
    consola.agregar_mensaje("📺 Juego con interfaz gráfica integrada")
    
    num_jugadores = 4
    colores_disponibles = ["Rojo", "Azul", "Verde", "Amarillo"]
    jugadores = []

    for i in range(num_jugadores):
        nombre = consola.obtener_input(f"Nombre del jugador {i+1}: ")
        nombre = nombre.capitalize()
        consola.agregar_mensaje(f"✅ Jugador {i+1}: {nombre}")
        
        consola.agregar_mensaje("Elige un color, estos son los que están disponibles:")
        for idx, color in enumerate(colores_disponibles, 1):
            consola.agregar_mensaje(f"{idx}. {color}")
        
        color_seleccionado = False
        while not color_seleccionado:
            try:
                seleccion = int(consola.obtener_input(f"{nombre}, elige tu color (1-{len(colores_disponibles)}): "))
                if 1 <= seleccion <= len(colores_disponibles):
                    color = colores_disponibles.pop(seleccion - 1)
                    consola.agregar_mensaje(f"✅ {nombre} eligió el color {color}")
                    color_seleccionado = True
                else:
                    consola.agregar_mensaje("❌ Opción inválida. Elige un número de la lista.")
            except ValueError:
                consola.agregar_mensaje("❌ Por favor, ingresa un número válido.")
        
        jugador = Jugador(nombre, color)
        jugadores.append(jugador)
        consola.agregar_mensaje(f"🎮 {nombre} ({color}) registrado correctamente")
        consola.agregar_mensaje("")
        time.sleep(0.5)

    tablero = Tablero()
    turno_actual = 0

    actualizar_visualizacion(jugadores, tablero)
    consola.agregar_mensaje("🎮 ¡El juego comienza!")

    while True:
        turno(jugadores[turno_actual], tablero, jugadores)

        if jugadores[turno_actual].todas_en_llegada():
            consola.agregar_mensaje(f"🎉 ¡{jugadores[turno_actual].nombre} ha ganado FELICITACIONES!")
            actualizar_visualizacion(jugadores, tablero)
            consola.agregar_mensaje("Presiona cualquier tecla para cerrar...")
            consola.obtener_input()
            break

        turno_actual = (turno_actual + 1) % len(jugadores)

if __name__ == "__main__":
    try:
        juego()
    finally:
        pygame.quit()
