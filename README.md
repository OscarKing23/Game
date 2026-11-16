# Batalla Random

Juego de combate por turnos hecho en Python. Elige un personaje, enfréntate a un jefe y utiliza ataques, defensas, objetos y habilidades especiales para ganar. Incluye una interfaz gráfica, animaciones y efectos de sonido.

## Características

- Menú de inicio y selección entre cinco personajes: Tortuga, Dragón, Jason, Terminator y Kratos.
- Combates por turnos contra un jefe controlado por el juego.
- Ataques normales, especiales y definitivos, además de habilidades de defensa y recarga de energía.
- Estados de combate como veneno, quemadura, parálisis y cansancio.
- Objetos consumibles para recuperar vida o energía y eliminar estados negativos.
- Música, efectos de sonido y animaciones durante el combate.
- Opción para reintentar o cambiar de personaje al terminar una batalla.

## Requisitos

- Python 3
- `customtkinter`
- `Pillow`
- `pygame`

## Instalación y ejecución

Clona el repositorio y entra en la carpeta del proyecto:

```bash
git clone https://github.com/OscarKing23/Game.git
cd Game
```

Instala las dependencias:

```bash
python -m pip install customtkinter Pillow pygame
```

Inicia el juego desde la carpeta raíz del proyecto:

```bash
python Games_Proyect1.py
```

En Windows también puedes usar `py` en lugar de `python` si ese es el comando configurado en tu sistema.

## Cómo jugar

1. Selecciona **Iniciar Juego** en el menú.
2. Escoge uno de los personajes disponibles.
3. En cada turno, elige una acción desde los menús de ataque, defensa, bolsa o energía.
4. Administra la vida y la energía, y aprovecha los objetos y efectos de estado para derrotar al jefe.
5. Al finalizar, selecciona **Reintentar** o vuelve a elegir un personaje.

## Estructura del proyecto

```text
Game/
├── Games_Proyect1.py      # Aplicación e interfaz principal del combate
├── Image/                 # Menú de inicio, imágenes y recursos gráficos
│   └── Start.py
├── Logic_All/
│   └── logic_combat.py    # Lógica de ataques, daño y estados
├── Personajes/            # Personajes, jefe y objetos consumibles
└── Audio/                 # Música y efectos de sonido
```

Ejecuta el programa desde la raíz para que encuentre las carpetas `Audio` e `Image`. Estos recursos forman parte del juego y deben conservarse junto al código.

## Crear un ejecutable (opcional)

El repositorio incluye una especificación de PyInstaller. Instala PyInstaller y ejecútala desde la raíz:

```bash
python -m pip install pyinstaller
pyinstaller "Peleas Random.spec"
```

El ejecutable y los archivos generados se guardarán en la carpeta `dist`.