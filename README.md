# 🎲 Parques-Py

Proyecto final para el curso de programación básica PC-2025-1

---

## 🎮 Características

- **Juego de Parqués completo** con todas las reglas tradicionales
- **Interfaz gráfica integrada** con consola horizontal en la parte inferior
- **Visualización en tiempo real** del tablero y movimientos
- **Consola integrada** para todas las interacciones del juego
- **Ventana única** que combina tablero gráfico y consola de texto
- **Diseño optimizado** con mejor aprovechamiento del espacio

## 📦 Requisitos

Este juego requiere el módulo `pygame`.  
Para instalarlo usar el comando:

```bash
pip install pygame
```

O instalar desde el archivo requirements.txt:

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

Para ejecutar el juego usar el comando:

```bash
python3 main.py
```

### 🎬 Demo

Para ver una demostración de la consola integrada:

```bash
python3 demo_consola_integrada.py
```

### 🧪 Test

Para probar la lógica de selección de colores:

```bash
python3 test_colores.py
```

### 🐛 Modo Debug

Para probar el juego con control manual de dados:

```bash
python3 main_debug.py
```

### 🧪 Test de Repetición

Para verificar que la selección de colores no se repite:

```bash
python3 test_seleccion_colores.py
```

### 📜 Demo de Scroll

Para probar la funcionalidad de scroll en la consola:

```bash
python3 demo_scroll.py
```

### 🧪 Test de Auto-Scroll

Para verificar que el auto-scroll funciona correctamente:

```bash
python3 test_auto_scroll.py
```

## 🖥️ Cómo funciona

1. **Se abre una ventana gráfica única** que contiene:
   - **Tablero de Parqués** en la parte superior (600x600)
   - **Consola integrada** en la parte inferior (600x180)
2. **Todo el juego se controla desde la consola integrada** - escribe tus respuestas y presiona Enter
3. **La visualización se actualiza automáticamente** con cada movimiento de ficha
4. **Puedes ver en tiempo real:**
   - Fichas en sus cárceles correspondientes
   - Fichas moviéndose por el tablero
   - Fichas llegando a la meta
   - Capturas de fichas
5. **Consola horizontal** con formato vertical simple para mejor legibilidad
6. **Sistema de scroll** para navegar todo el historial de mensajes
7. **Auto-scroll inteligente** que se activa/desactiva automáticamente
8. **Indicador de posición** en el scroll (📜 X-Y de Z)
9. **Indicador de modo** (🔄 AUTO / ⏸️ MANUAL)

## 🎯 Controles

- **Consola integrada**: Para todas las interacciones del juego
  - Escribe tu respuesta y presiona **Enter**
  - Usa **Backspace** para borrar
  - Usa **ESC** para cancelar una entrada
- **Scroll del historial**:
  - **↑ ↓** : Scroll línea por línea
  - **Page Up/Down** : Scroll rápido
  - **Home** : Ir al inicio del historial
  - **End** : Ir al final del historial
  - **🔄 AUTO** : Auto-scroll activo (verde)
  - **⏸️ MANUAL** : Control manual activo (naranja)
- **Ventana gráfica**: Se actualiza automáticamente con el progreso
- **Cerrar**: Presiona cualquier tecla al final del juego o cierra la ventana