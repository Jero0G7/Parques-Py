import pygame

class ConsolaIntegrada:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.lineas = []  # Ahora cada línea será (texto, color)
        self.input_texto = ""
        self.input_activo = False
        self.max_lineas = 12
        self.scroll_offset = 0
        self.lineas_por_pagina = 8
        self.auto_scroll = True

    def agregar_mensaje(self, mensaje, color=(255,255,255)):
        self.lineas.append((str(mensaje), color))
        if self.auto_scroll and len(self.lineas) > self.lineas_por_pagina:
            self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)

    def dibujar(self):
        import pygame
        from main import FUENTE_CONSOLA, pantalla, COLOR_CONSOLA
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
            for linea, color in lineas_a_mostrar:
                if y_offset < area_historial - 10:
                    if len(linea) > 65:
                        linea = linea[:62] + "..."
                    texto_surface = FUENTE_CONSOLA.render(linea, True, color)
                    pantalla.blit(texto_surface, (self.x + 10, self.y + y_offset))
                    y_offset += 18
        pygame.draw.line(pantalla, (100, 100, 100), 
                        (self.x + 5, self.y + area_historial), 
                        (self.x + self.ancho - 5, self.y + area_historial), 2)
        if self.input_activo:
            input_surface = FUENTE_CONSOLA.render(f"> {self.input_texto}", True, (255, 255, 255))
            pantalla.blit(input_surface, (self.x + 10, self.y + area_historial + 5))

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
