from src.jugador import Jugador
from src.dados import lanzar_dados, es_par
from src.tablero_logico import Tablero
from src.consola import mostrar_fichas_llegadas, mostrar_tablero
import pygame
from src.tablero_grafico import Tablero as TableroGrafico
import time
import sys

MODO_DESARROLLO = False  # Cambiar a False para juego normal

# Inicializar pygame para la visualización gráfica
pygame.init()
ANCHO_VENTANA = 600
ALTO_VENTANA = 800  # Aumentar altura para la consola horizontal
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Parqués - Juego Completo")
tablero_grafico = TableroGrafico()

# Configuración de la consola integrada
FUENTE_CONSOLA = pygame.font.Font(None, 20)  # Fuente más pequeña para más texto
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
        self.max_lineas = 12  # Más líneas para consola más alta
        self.scroll_offset = 0  # Offset para el scroll
        self.lineas_por_pagina = 8  # Líneas visibles por página
        self.auto_scroll = True  # Controlar si debe hacer auto-scroll
        
    def agregar_mensaje(self, mensaje):
        """Agrega un mensaje a la consola"""
        self.lineas.append(str(mensaje))
        # Auto-scroll al final cuando se agrega un mensaje (solo si auto_scroll está activo)
        if self.auto_scroll and len(self.lineas) > self.lineas_por_pagina:
            self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)
    
    def obtener_input(self, prompt=""):
        """Obtiene input del usuario desde la consola integrada"""
        if prompt:
            self.agregar_mensaje(prompt)
            # Forzar actualización inmediata para mostrar la pregunta
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
                        if self.input_texto.strip():  # Solo aceptar si hay texto
                            texto = self.input_texto
                            self.input_texto = ""
                            self.input_activo = False
                            self.agregar_mensaje(f"> {texto}")
                            # Forzar auto-scroll al final después de agregar el mensaje
                            if self.auto_scroll and len(self.lineas) > self.lineas_por_pagina:
                                self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)
                            pygame.time.wait(100)  # Pequeña pausa para evitar múltiples inputs
                            return texto
                    elif evento.key == pygame.K_BACKSPACE:
                        self.input_texto = self.input_texto[:-1]
                    elif evento.key == pygame.K_ESCAPE:
                        # Permitir cancelar con ESC
                        self.input_texto = ""
                        self.input_activo = False
                        pygame.time.wait(100)  # Pequeña pausa para evitar múltiples inputs
                        return ""
                    elif evento.key == pygame.K_UP:
                        # Scroll hacia arriba
                        if self.scroll_offset > 0:
                            self.scroll_offset -= 1
                            self.auto_scroll = False  # Desactivar auto-scroll cuando el usuario hace scroll manual
                    elif evento.key == pygame.K_DOWN:
                        # Scroll hacia abajo
                        if self.scroll_offset < max(0, len(self.lineas) - self.lineas_por_pagina):
                            self.scroll_offset += 1
                            # Si llega al final, reactivar auto-scroll
                            if self.scroll_offset >= max(0, len(self.lineas) - self.lineas_por_pagina):
                                self.auto_scroll = True
                    elif evento.key == pygame.K_PAGEUP:
                        # Scroll rápido hacia arriba
                        self.scroll_offset = max(0, self.scroll_offset - 3)
                        self.auto_scroll = False  # Desactivar auto-scroll
                    elif evento.key == pygame.K_PAGEDOWN:
                        # Scroll rápido hacia abajo
                        self.scroll_offset = min(len(self.lineas) - self.lineas_por_pagina, self.scroll_offset + 3)
                        # Si llega al final, reactivar auto-scroll
                        if self.scroll_offset >= max(0, len(self.lineas) - self.lineas_por_pagina):
                            self.auto_scroll = True
                    elif evento.key == pygame.K_HOME:
                        # Ir al inicio
                        self.scroll_offset = 0
                        self.auto_scroll = False  # Desactivar auto-scroll
                    elif evento.key == pygame.K_END:
                        # Ir al final
                        self.scroll_offset = max(0, len(self.lineas) - self.lineas_por_pagina)
                        self.auto_scroll = True  # Reactivar auto-scroll
                    elif evento.unicode.isprintable():  # Solo caracteres imprimibles
                        self.input_texto += evento.unicode
            
            # Actualizar solo la consola sin llamar a actualizar_visualizacion
            self.dibujar()
            pygame.display.flip()
            pygame.time.wait(10)  # Pequeña pausa para no saturar la CPU
    
    def dibujar(self):
        """Dibuja la consola en la pantalla"""
        # Fondo de la consola
        pygame.draw.rect(pantalla, COLOR_CONSOLA, (self.x, self.y, self.ancho, self.alto))
        pygame.draw.rect(pantalla, (100, 100, 100), (self.x, self.y, self.ancho, self.alto), 2)
        
        # Área de historial (parte superior de la consola)
        area_historial = self.alto - 30  # Dejar 30px para el input (más espacio para historial)
        
        # Dibujar líneas de texto con scroll
        if self.lineas:
            y_offset = 10
            
            # Calcular líneas a mostrar basadas en el scroll
            inicio = self.scroll_offset
            fin = min(inicio + self.lineas_por_pagina, len(self.lineas))
            lineas_a_mostrar = self.lineas[inicio:fin]
            
            # Mostrar indicador de scroll si hay más líneas
            if len(self.lineas) > self.lineas_por_pagina:
                # Indicador de posición en el scroll
                scroll_info = f"📜 {inicio + 1}-{fin} de {len(self.lineas)}"
                scroll_surface = FUENTE_CONSOLA.render(scroll_info, True, (200, 200, 200))
                pantalla.blit(scroll_surface, (self.x + self.ancho - 120, self.y + 5))
                
                # Indicador de auto-scroll
                if self.auto_scroll:
                    auto_scroll_info = "🔄 AUTO"
                    auto_scroll_surface = FUENTE_CONSOLA.render(auto_scroll_info, True, (100, 255, 100))
                    pantalla.blit(auto_scroll_surface, (self.x + 10, self.y + 5))
                else:
                    auto_scroll_info = "⏸️ MANUAL"
                    auto_scroll_surface = FUENTE_CONSOLA.render(auto_scroll_info, True, (255, 200, 100))
                    pantalla.blit(auto_scroll_surface, (self.x + 10, self.y + 5))
            
            for linea in lineas_a_mostrar:
                # Verificar que no se salga del área de historial
                if y_offset < area_historial - 10:  # Mínimo margen para mostrar todas las líneas
                    # Truncar líneas muy largas para que quepan en la consola
                    if len(linea) > 65:  # Más espacio para texto
                        linea = linea[:62] + "..."
                    texto_surface = FUENTE_CONSOLA.render(linea, True, (255, 255, 255))
                    pantalla.blit(texto_surface, (self.x + 10, self.y + y_offset))
                    y_offset += 18  # Más espacio entre líneas
        
        # Dibujar línea separadora
        pygame.draw.line(pantalla, (100, 100, 100), 
                        (self.x + 5, self.y + area_historial), 
                        (self.x + self.ancho - 5, self.y + area_historial), 2)
        
        # Dibujar línea de input en la parte inferior (área separada)
        if self.input_activo:
            input_surface = FUENTE_CONSOLA.render(f"> {self.input_texto}", True, (255, 255, 255))
            pantalla.blit(input_surface, (self.x + 10, self.y + area_historial + 5))  # Mínima separación

# Crear instancia de la consola integrada (horizontal en la parte inferior)
consola = ConsolaIntegrada(20, 620, 560, 180)  # Aún más alta para mejor separación

# Asegurar que el auto-scroll esté configurado correctamente
if len(consola.lineas) > consola.lineas_por_pagina:
    consola.scroll_offset = max(0, len(consola.lineas) - consola.lineas_por_pagina)

def actualizar_visualizacion(jugadores, tablero):
    """Actualiza la visualización gráfica del tablero"""
    # Limpiar pantalla
    pantalla.fill(COLOR_FONDO)
    
    # Dibujar título
    titulo = FUENTE_TITULO.render("🎲 PARQUÉS 🎲", True, COLOR_TEXTO)
    pantalla.blit(titulo, (20, 10))
    
    # Dibujar tablero en el área izquierda
    if jugadores:
        tablero_grafico.dibujar(pantalla, jugadores)
    else:
        # Dibujar tablero vacío
        tablero_grafico.dibujar(pantalla, [])
    
    # Dibujar consola
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
    while repetir:
        consola.agregar_mensaje(f"Turno de {jugador.nombre}")
        
        # Manejar el lanzamiento de dados con mejor manejo de errores
        try:
            d1, d2 = lanzar_dados(debug=MODO_DESARROLLO, input_func=consola.obtener_input)
            consola.agregar_mensaje(f"Lanzó: {d1} y {d2}")
        except (ValueError, TypeError):
            # Si hay error en los dados, usar valores aleatorios
            import random
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            consola.agregar_mensaje(f"Error en entrada de dados. Lanzó: {d1} y {d2}")

        movimientos_extra = 0
        jugador.ultima_ficha_movida = None

        if d1 == 5 or d2 == 5 or (d1 + d2) == 5:
            for ficha in jugador.fichas:
                if ficha.posicion == -1:
                    ficha.sacar_de_la_carcel()
                    tablero.agregar_ficha(ficha)
                    consola.agregar_mensaje(f"{jugador.nombre} sacó una ficha de la cárcel.")
                    actualizar_visualizacion(jugadores, tablero)
                    time.sleep(0.5)
                    break

        fichas_disponibles = [f for f in jugador.fichas if f.posicion != -1 and not f.en_llegada]

        if len(fichas_disponibles) == 1:
            ficha = fichas_disponibles[0]
            consola.agregar_mensaje(f"Solo puedes mover una ficha. La moveremos por ti.")
        elif len(fichas_disponibles) > 1:
            consola.agregar_mensaje("Las fichas que puedes mover son:")
            for idx, f in enumerate(fichas_disponibles):
                consola.agregar_mensaje(f"{idx + 1}. Ficha en posición {f.posicion}")
            while True:
                try:
                    seleccion = int(consola.obtener_input("¿Qué ficha quieres mover?"))
                    if 1 <= seleccion <= len(fichas_disponibles):
                        ficha = fichas_disponibles[seleccion - 1]
                        break
                    else:
                        consola.agregar_mensaje("Opción inválida. Elige las que ves en pantalla.")
                except ValueError:
                    consola.agregar_mensaje("Ingresa el número por favor.")
        else:
            ficha = None

        if ficha:
            capturo, llego = tablero.mover_ficha(ficha, d1 + d2)
            jugador.ultima_ficha_movida = ficha
            if capturo:
                movimientos_extra += 20
            if llego:
                movimientos_extra += 10
            actualizar_visualizacion(jugadores, tablero)
            time.sleep(0.5)

        if movimientos_extra > 0:
            usar_movimientos_extra(jugador, tablero, jugadores, movimientos_extra)

        if es_par(d1, d2):
            jugador.pares_consecutivos += 1
            consola.agregar_mensaje(f"{jugador.nombre} sacó un par. ¡Repite turno! ({jugador.pares_consecutivos} consecutivos)")

            if jugador.pares_consecutivos == 3:
                if jugador.ultima_ficha_movida:
                    jugador.ultima_ficha_movida.enviar_a_la_carcel()
                    consola.agregar_mensaje(f"⚠️ ¡{jugador.nombre} sacó 3 pares! Su última ficha fue enviada a la cárcel.")
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
    
    num_jugadores = 2
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
        time.sleep(0.5)  # Pequeña pausa para asegurar que se procese correctamente

    tablero = Tablero()
    turno_actual = 0

    # Mostrar el tablero inicial
    actualizar_visualizacion(jugadores, tablero)
    consola.agregar_mensaje("🎮 ¡El juego comienza!")

    while True:
        turno(jugadores[turno_actual], tablero, jugadores)

        if jugadores[turno_actual].todas_en_llegada():
            consola.agregar_mensaje(f"🎉 ¡{jugadores[turno_actual].nombre} has ganado FELICITACIONES!")
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
