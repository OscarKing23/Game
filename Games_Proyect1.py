# Importa las librerías necesarias y módulos (interfaz, imágenes, lógica del combate, etc.)
import customtkinter as ctk
from PIL import Image, ImageTk
from Logic_All.logic_combat import CombatLogic
from Image.Start import MenuInicio
import random
import os
import sys
import pygame

# Importa las clases de personajes y jefe
from Personajes.Personaje_1 import Tortuga
from Personajes.Personaje_2 import Dragon
from Personajes.Personaje_3 import Jason
from Personajes.Personaje_4 import Terminator
from Personajes.Personaje_5 import Kratos
from Personajes.Boss import BossIT

# Función para acceder a recursos locales o empaquetados (.exe)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS   # Ruta temporal si está empaquetado
    except Exception:
        base_path = os.path.abspath(".")  # Ruta local si está normal
    return os.path.join(base_path, relative_path)

# Configura los colores y temas de la interfaz
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Inicializa el sistema de sonido de pygame
pygame.mixer.init()
AUDIO_PATH = "audio"

# Función para cargar sonidos según el nombre del archivo
def load_sound(name):
    path = resource_path(os.path.join(AUDIO_PATH, name))
    # Verifica si el archivo existe antes de cargar
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None

# Carga los sonidos utilizados en distintas acciones del juego
sonido_golpe = load_sound("golpe.mp3")              # Para ataques normales
sonido_especial = load_sound("ataque.mp3")          # Para ataques especiales
sonido_escudo = load_sound("escudo.mp3")            # Para usar defensa/esquive
sonido_antidoto = load_sound("antidoto.mp3")        # Para usar antídoto
sonido_buff = load_sound("Buff_defensa.mp3")        # Para usar buff de defensa
sonido_absoluta = load_sound("defensa_absoluta.mp3")# Para usar defensa absoluta
sonido_habilidad = load_sound("habilidad.mp3")      # Para usar habilidad definitiva
sonido_incremento = load_sound("incremento.mp3")    # Para usar incremento de ataque
sonido_pocion = load_sound("pocion.mp3")            # Para usar poción/hiperpoción/elixir
sonido_explosion = load_sound("explosion.mp3")      # Para habilidad definitiva
sonido_final = load_sound("Final.mp3")              # Al ganar
sonido_inicio = load_sound("inicio.mp3")            # Música de inicio en bucle
sonido_muerte_jefe = load_sound("muerte_jefe.mp3")  # Al perder/jefe gana
sonido_combate = load_sound("combate.mp3")          # Música combate en bucle

# Lista de opciones de personajes disponibles para el jugador
PERSONAJES_OPTIONS = [
    {"nombre": "🐢 Tortuga",    "clase": Tortuga,    "imagen": "Image/TortugaPixel.png"},
    {"nombre": "🐉 Dragón",     "clase": Dragon,     "imagen": "Image/DragonPixel.jpeg"},
    {"nombre": "🧙 Jason",      "clase": Jason,      "imagen": "Image/stick3.png"},
    {"nombre": "🤖 Terminator", "clase": Terminator, "imagen": "Image/Terminator.jpg"},
    {"nombre": "🥷 Kratos",     "clase": Kratos,     "imagen": "Image/kratos.jpg"}
]
# Opción del jefe
BOSS_OPTION = {"nombre": "IT Boss", "clase": BossIT, "imagen": "Imagenes/it.png"}

# Diccionario de emojis para mostrar los estados del jugador
ESTADO_EMOJIS = {
    "paralisis": "🟣",
    "incremento_ataque": "💥",
    "veneno": "🧪",
    "buff_defensa": "🛡️",
    "cura_estado": "🍃",
    "recarga_maxima": "⚡",
    "esquive": "🌀",
    "proteccion": "🛡️",
}

# Diccionario para mostrar mensajes explicativos sobre los estados
ESTADO_TOOLTIP_MSG = {
    "paralisis": "Parálisis: 50% Perder turno.",
    "incremento_ataque": "+20% Daño.",
    "veneno": "Veneno -: Pierdes vida cada turno.",
    "buff_defensa": "+20% Defensa.",
    "cura_estado": "Elimina estados negativos.",
    "recarga_maxima": "+20% Energía.",
    "esquive": "Esquive: +20% evitar ataques.",
    "proteccion": "Defensa absoluta: No Recibe Daño Este Turno.",
}

# Clase para mostrar mensajes emergentes (tooltips) cuando el mouse pasa encima
class Tooltip:
    def __init__(self, widget, text, bg="#333", fg="#fff"):
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)    # Cuando se entra con el mouse
        widget.bind("<Leave>", self.hide_tip)    # Cuando se sale

    # Muestra el mensaje emergente sobre el widget
    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        # Calcula la posición del tooltip
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() - 40
        self.tipwindow = tw = ctk.CTkToplevel(self.widget)
        tw.overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        frame = ctk.CTkFrame(tw, fg_color=self.bg, corner_radius=8)
        frame.pack()
        label = ctk.CTkLabel(frame, text=self.text, text_color=self.fg, bg_color=self.bg, font=("Arial", 11, "bold"))
        label.pack(padx=6, pady=5)
        tw.lift()

    # Oculta el mensaje emergente
    def hide_tip(self, event=None):
        tw = self.tipwindow
        if tw:
            tw.destroy()
        self.tipwindow = None

# Pantalla para seleccionar personaje
class SeleccionFrame(ctk.CTkFrame):
    def __init__(self, master, app_controller, **kwargs):
        super().__init__(master, **kwargs)
        self.app_controller = app_controller
        # Configura el frame principal
        self.configure(fg_color=self.master.pastel_bg)
        self.grid_columnconfigure(tuple(range(len(PERSONAJES_OPTIONS))), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        # Título de la pantalla
        ctk.CTkLabel(self, text="ESCOGE TU GUERRERO", font=("Arial", 30, "bold"), text_color="#3a3a3a").grid(row=0, column=0, columnspan=len(PERSONAJES_OPTIONS), pady=40, sticky="n")
        self.crear_opciones()
        # Cuando entra a selección se detiene música de inicio y inicia música de combate en bucle
        if sonido_inicio:
            sonido_inicio.stop()
        if sonido_combate:
            sonido_combate.play(-1)

    # Crea los botones y vistas para seleccionar los personajes
    def crear_opciones(self):
        # Recorre las opciones de personajes y crea un frame para cada uno
        for i, data in enumerate(PERSONAJES_OPTIONS):
            nombre = data["nombre"]
            clase = data["clase"]
            imagen_path = data["imagen"]
            frame = ctk.CTkFrame(self, fg_color="#fff7bd", corner_radius=15, border_width=2, border_color="#f09a21")
            frame.grid(row=1, column=i, padx=15, pady=10, sticky="nsew")
            img = None
            img_abs_path = resource_path(imagen_path)
            # Carga la imagen del personaje si existe
            if os.path.exists(img_abs_path):
                img = ctk.CTkImage(light_image=Image.open(img_abs_path).resize((130, 130)), size=(130, 130))
            lbl_img = ctk.CTkLabel(frame, image=img, text="" if img else "IMG\nFALTA", width=130, height=130, fg_color="#e5e5e5")
            lbl_img.pack(pady=(2, 3), padx=10)
            # Muestra los atributos básicos del personaje
            temp_obj = clase()
            atributos = (
                f"Vida: {getattr(temp_obj, 'vida', 'N/A')}\n"
                f"Ataque: {getattr(temp_obj, 'ataque', 'N/A')}\n"
                f"Energía: {getattr(temp_obj, 'energia', 'N/A')}\n"
                f"Defensa: {getattr(temp_obj, 'defensa', 'N/A')}\n"
            )
            ctk.CTkLabel(frame, text=atributos, font=("Arial", 14, "bold"), text_color="#222", fg_color="transparent").pack(pady=(10, 2))
            # Botón para seleccionar el personaje y avanzar
            btn = ctk.CTkButton(
                frame, text=f"Seleccionar {nombre.split()[-1]}", 
                command=lambda c=clase: self.seleccionar(c),
                fg_color="#f09a21", hover_color="#ce7d15", text_color="white", corner_radius=10
            )
            btn.pack(pady=(0, 10), padx=10)

    # Llama la función para iniciar la batalla con el personaje elegido
    def seleccionar(self, personaje_clase):
        jugador_obj = personaje_clase()
        self.app_controller.iniciar_batalla(jugador_obj)

# Clase que representa pantalla de la batalla
class BatallaFrame(ctk.CTkFrame):
    pastel_bg = "#f4efe3"
    btn_pastel_attack = "#ffbfbf"
    btn_pastel_def = "#b6dbff"
    btn_pastel_def_alt = "#fbf6ee"
    btn_pastel_bag = "#fff5a3"
    btn_pastel_energy = "#d1f7ff"
    sub_btn_bg = "#ffffff"
    sub_btn_hover = "#f7e9cf"

    # Constructor auxiliar para la barra de estados
    def crear_barra_estados(self):
        self.barra_estado_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent", width=460, height=72)
        self.barra_estado_frame.place(x=15, y=185)
        self.tooltip_objs = []

    # Actualiza los estados que se ven y tooltips en la pantalla
    def actualizar_barra_estados(self):
        # Crea la barra si no existe o no está visible
        if not hasattr(self, "barra_estado_frame") or not self.barra_estado_frame.winfo_ismapped():
            self.crear_barra_estados()
        # Limpia los widgets anteriores
        for widget in self.barra_estado_frame.winfo_children():
            widget.destroy()
        self.tooltip_objs = []
        # Filtra los estados activos del jugador para mostrar
        estados_mostrar = [est for est in self.jugador.estados if est in ESTADO_EMOJIS and self.jugador.turnos_estado.get(est, 0) > 0]
        # Si hay estados, muestra sus íconos y tooltips
        if estados_mostrar:
            icons_frame = ctk.CTkFrame(self.barra_estado_frame, fg_color="transparent")
            icons_frame.pack(pady=(26,0), padx=0)
            # Agrega los íconos y tooltips correspondientes
            for estado in estados_mostrar:
                emoji = ESTADO_EMOJIS[estado]
                lbl = ctk.CTkLabel(icons_frame, text=emoji, font=("Arial", 25),
                                   fg_color="transparent", text_color="black", width=45)
                lbl.pack(side="left", padx=4)
                tip_msg = ESTADO_TOOLTIP_MSG.get(estado, "Efecto especial activo.")
                self.tooltip_objs.append(Tooltip(lbl, tip_msg))
        else:
            lbl = ctk.CTkLabel(self.barra_estado_frame, text="Sin efectos/buffos", font=("Arial", 13),
                               fg_color="transparent", text_color="#888")
            lbl.pack(side="left", padx=4)

    # Constructor principal, inicializa la pantalla y los elementos
    def __init__(self, master, jugador, enemigo, **kwargs):
        super().__init__(master, **kwargs)
        self.jugador = jugador
        self.enemigo = enemigo
        self.configure(fg_color=self.master.cget('fg_color'))
        self.pack(fill="both", expand=True)
        self.sub_buttons = []
        self.fin_juego = False
        self.overlay_final = None
        self.crear_widgets_principales()
        self.crear_barra_estados()
        self.actualizar_barras()

    # Crea paneles de info y botones principales de batalla
    def crear_widgets_principales(self):
        # Crea el frame superior con fondo y sprites
        self.top_frame = ctk.CTkFrame(self, width=1200, height=500, fg_color=self.pastel_bg)
        self.top_frame.place(x=0, y=0)
        fondo_path = resource_path("Image/escenario.png")
        # Carga imagen de fondo si existe
        if os.path.exists(fondo_path):
            bg_img = Image.open(fondo_path).resize((1200, 500))
            self.bg_image = ctk.CTkImage(light_image=bg_img, dark_image=bg_img, size=(1200, 500))
            ctk.CTkLabel(self.top_frame, image=self.bg_image, text="").place(x=0, y=0)
        else:
            ctk.CTkFrame(self.top_frame, fg_color=self.pastel_bg).place(relwidth=1, relheight=1)
        # Crea los sprites del jugador y enemigo
        self.lbl_enemigo = self.crear_sprite(self.enemigo.imagen, 190, 190)
        self.lbl_enemigo.place(x=300, y=100)
        self.lbl_jugador = self.crear_sprite(self.jugador.imagen, 190, 190)
        self.lbl_jugador.place(x=700, y=100)
        # Crea el panel inferior con barras de vida/energía/defensa y botones
        self.bottom_panel = ctk.CTkFrame(self, width=1160, height=260, fg_color="#f09a21", corner_radius=16)
        self.bottom_panel.place(x=20, y=520)
        self.left_frame = ctk.CTkFrame(self.bottom_panel, width=650, height=240, fg_color="#fff7bd")
        self.left_frame.place(x=10, y=10)
        self.right_frame = ctk.CTkFrame(self.bottom_panel, width=490, height=240, fg_color="#fff7bd")
        self.right_frame.place(x=670, y=10)

        bar_w = 200
        # Etiquetas de vida, energía y defensa del jugador
        self.lbl_nombre_j = ctk.CTkLabel(self.left_frame, text=f"{self.jugador.nombre}:", font=("Arial", 12, "bold"), text_color="#5b4a3a")
        self.lbl_nombre_j.place(x=10, y=10)
        self.lbl_nombre_e = ctk.CTkLabel(self.left_frame, text=f"{self.enemigo.nombre} (JEFE):", font=("Arial", 12, "bold"), text_color="#a80000")
        self.lbl_nombre_e.place(x=340, y=10)
        # vida
        self.bar_vida_j = ctk.CTkProgressBar(self.left_frame, width=bar_w, height=10, progress_color="#0af10a")
        self.bar_vida_j.place(x=10, y=35)
        self.lbl_vida_j = ctk.CTkLabel(self.left_frame, text="Vida: ", text_color="black", font=("Arial", 12, "bold"))
        self.lbl_vida_j.place(x=10 + bar_w + 10, y=33)
        # energia
        self.bar_ene_j = ctk.CTkProgressBar(self.left_frame, width=bar_w, height=10, progress_color="#f8ec06")
        self.bar_ene_j.place(x=10, y=55)
        self.lbl_ene_j = ctk.CTkLabel(self.left_frame, text="Energía: ", text_color="black", font=("Arial", 12, "bold"))
        self.lbl_ene_j.place(x=10 + bar_w + 10, y=53)
        # defensa
        self.bar_def_j = ctk.CTkProgressBar(self.left_frame, width=bar_w, height=10, progress_color="#c5c5c5")
        self.bar_def_j.place(x=10, y=75)
        self.lbl_def_j = ctk.CTkLabel(self.left_frame, text="Defensa: ", text_color="black", font=("Arial", 12, "bold"))
        self.lbl_def_j.place(x=10 + bar_w + 10, y=73)

        # Etiquetas del jefe
        # vida
        self.bar_vida_e = ctk.CTkProgressBar(self.left_frame, width=bar_w, height=10, progress_color="#f10e0e")
        self.bar_vida_e.place(x=340, y=35)
        self.lbl_vida_e = ctk.CTkLabel(self.left_frame, text="Vida: ", text_color="black", font=("Arial", 12, "bold"))
        self.lbl_vida_e.place(x=340 + bar_w + 10, y=33)
        # energia
        self.bar_ene_e = ctk.CTkProgressBar(self.left_frame, width=bar_w, height=10, progress_color="#f8ec06")
        self.bar_ene_e.place(x=340, y=55)
        self.lbl_ene_e = ctk.CTkLabel(self.left_frame, text="Energía: ", text_color="black", font=("Arial", 11, "bold"))
        self.lbl_ene_e.place(x=340 + bar_w + 10, y=53)
        # defensa
        self.bar_def_e = ctk.CTkProgressBar(self.left_frame, width=bar_w, height=10, progress_color="#c5c5c5")
        self.bar_def_e.place(x=340, y=75)
        self.lbl_def_e = ctk.CTkLabel(self.left_frame, text="Defensa: ", text_color="black", font=("Arial", 11, "bold"))
        self.lbl_def_e.place(x=340 + bar_w + 10, y=73)

        # Caja de texto para mostrar mensajes de la batalla
        self.texto = ctk.CTkTextbox(self.left_frame, width=630, height=120, text_color="black", fg_color="#fffef6")
        self.texto.place(x=10, y=110)
        self.texto.configure(state="disabled")
        self.insert_text(f"¡Comienza la batalla! {self.jugador.nombre} vs {self.enemigo.nombre}\n", color="#222")

        # Botones principales del panel derecho (acciones)
        # Boton atacar
        self.btn_attack = ctk.CTkButton(self.right_frame, text="⚔️ LUCHAR", fg_color=self.btn_pastel_attack,
                                         hover_color=self.sub_btn_hover, width=220, height=40,
                                         text_color="black", command=self.mostrar_submenu_ataque)
        self.btn_attack.place(x=15, y=10)
        # Boton defender
        self.btn_defend = ctk.CTkButton(self.right_frame, text="🛡️ DEFENSA", fg_color=self.btn_pastel_def,
                                         hover_color=self.sub_btn_hover, width=220, height=40,
                                         text_color="black", command=self.mostrar_submenu_defensa)
        self.btn_defend.place(x=255, y=10)
        # Boton bolsa
        self.btn_bag = ctk.CTkButton(self.right_frame, text="🎒 BOLSA", fg_color=self.btn_pastel_bag,
                                         hover_color=self.sub_btn_hover, width=220, height=40,
                                         text_color="black", command=self.mostrar_submenu_bolsa)
        self.btn_bag.place(x=15, y=60)
        # Boton energía
        self.btn_energy = ctk.CTkButton(self.right_frame, text="⚡ ENERGÍA", fg_color=self.btn_pastel_energy,
                                         hover_color=self.sub_btn_hover, width=220, height=40,
                                         text_color="black", command=self.mostrar_submenu_energia)
        self.btn_energy.place(x=255, y=60)

    # Inserta mensaje en la caja de texto, con color
    def insert_text(self, msg, color="#222"):
        self.texto.configure(state="normal")
        end_index = self.texto.index('end-1c')
        self.texto.insert("end", msg)
        start_index = end_index
        end_index = self.texto.index('end-1c')
        self.texto.tag_add(color, start_index, end_index)
        self.texto.tag_config(color, foreground=color)
        self.texto.configure(state="disabled")

    # Mensaje para acciones del usuario
    def insert_user_action(self, msg):
        self.insert_text(msg, color="#3182ce")

    # Mensaje para acciones del jefe/enemigo
    def insert_enemy_action(self, msg):
        self.insert_text(msg, color="#ba181b")

    # Muestra el submenu para ataques (4 tipos)
    def mostrar_submenu_ataque(self):
        if self.fin_juego: return
        self.ocultar_botones_principales()
        self.eliminar_submenu()
        # Usa color pastel para ataques
        color = self.btn_pastel_attack
        # Nombres de los ataques
        n_normal = self.jugador.nombre_ataque_normal()
        n_especial = self.jugador.nombre_ataque_especial()
        n_definitiva = self.jugador.nombre_habilidad_definitiva()
        n_inc = self.jugador.nombre_incremento()
        # Crea los botones de ataque con sus respectivos sonidos
        self.sub_buttons.append(ctk.CTkButton(
            self.right_frame, text=n_normal, fg_color=color, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.ataque_normal(self.enemigo), sonido_golpe)))
        self.sub_buttons[-1].place(x=15, y=10)
        # Cambia el sonido de especial a ataque
        self.sub_buttons.append(ctk.CTkButton(
            self.right_frame, text=n_especial, fg_color=color, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.ataque_especial(self.enemigo), sonido_especial)))
        self.sub_buttons[-1].place(x=255, y=10)
        # Cambia el sonido de definitiva a explosion
        self.sub_buttons.append(ctk.CTkButton(
            self.right_frame, text=n_definitiva, fg_color=color, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.habilidad_definitiva(self.enemigo), sonido_explosion)))
        self.sub_buttons[-1].place(x=15, y=60)
        # Incremento de ataque
        self.sub_buttons.append(ctk.CTkButton(
            self.right_frame, text=n_inc, fg_color=color, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.incremento(), sonido_incremento)))
        self.sub_buttons[-1].place(x=255, y=60)
        self.add_volver_submenu()
        self.actualizar_barra_estados()

    # Muestra submenu de defensa
    def mostrar_submenu_defensa(self):
        if self.fin_juego: return
        self.ocultar_botones_principales()
        self.eliminar_submenu()
        # Usa colores pastel para defensa
        color1 = self.btn_pastel_def
        color2 = self.btn_pastel_def_alt
        # Nombres de las defensas
        n1 = self.jugador.nombre_defensa_1()
        n2 = self.jugador.nombre_defensa_2()
        n_buff = self.jugador.nombre_defensa_buff()
        n_esq = self.jugador.nombre_defensa_esquive()
        # Crea los botones de defensa con sus respectivos sonidos
        self.sub_buttons.append(ctk.CTkButton(
            self.right_frame, text=n1, fg_color=color1, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.defensa_habilidad_1(), sonido_escudo)))
        self.sub_buttons[-1].place(x=15, y=10)
        # Segundo botón de defensa
        self.sub_buttons.append(ctk.CTkButton(
            self.right_frame, text=n2, fg_color=color2, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.defensa_habilidad_2(), sonido_absoluta)))
        self.sub_buttons[-1].place(x=255, y=10)
        # Buff de defensa
        self.sub_buttons.append(ctk.CTkButton(
            self.right_frame, text=n_buff, fg_color=color1, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.defensa_buff(), sonido_buff)))
        self.sub_buttons[-1].place(x=15, y=60)
        # Esquive
        self.sub_buttons.append(ctk.CTkButton(
            self.right_frame, text=n_esq, fg_color=color1, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.defensa_esquive(), sonido_escudo)))
        self.sub_buttons[-1].place(x=255, y=60)
        self.add_volver_submenu()
        self.actualizar_barra_estados()

    # Muestra submenu de bolsa (consumibles)
    def mostrar_submenu_bolsa(self):
        if self.fin_juego: return
        self.ocultar_botones_principales()
        self.eliminar_submenu()
        color = self.btn_pastel_bag
        # Crea los botones de consumibles con sus respectivos sonidos
        self.sub_buttons.append(ctk.CTkButton(self.right_frame, text="Poción (+25%)", fg_color=color, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.usar_objeto("pocion"), sonido_pocion)))
        self.sub_buttons[-1].place(x=15, y=10)
        # Segundo botón de antídoto
        self.sub_buttons.append(ctk.CTkButton(self.right_frame, text="Antídoto", fg_color=color, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.usar_objeto("cura_estado"), sonido_antidoto)))
        self.sub_buttons[-1].place(x=255, y=10)
        # Hiperpoción
        self.sub_buttons.append(ctk.CTkButton(self.right_frame, text="HiperPoción (+70%)", fg_color=color, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.usar_objeto("hiper_pocion"), sonido_pocion)))
        self.sub_buttons[-1].place(x=15, y=60)
        # Elixir
        self.sub_buttons.append(ctk.CTkButton(self.right_frame, text="Elixir (60% energía/Habilidad +1)", fg_color=color, hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.usar_objeto("elixir"), sonido_pocion)))
        self.sub_buttons[-1].place(x=255, y=60)
        self.add_volver_submenu()
        self.actualizar_barra_estados()

    # Muestra submenu de energía
    def mostrar_submenu_energia(self):
        if self.fin_juego: return
        self.ocultar_botones_principales()
        self.eliminar_submenu()
        color = self.btn_pastel_energy
        # Nombres de las recargas de energía
        n_carga = self.jugador.nombre_energia_carga()
        n_max = self.jugador.nombre_energia_carga_max()
        # Crea los botones de energía con sus respectivos sonidos
        self.sub_buttons.append(ctk.CTkButton(self.right_frame, text=n_carga, fg_color=color,
            hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.energia_carga(), sonido_incremento)))
        self.sub_buttons[-1].place(x=15, y=10)
        # Segundo botón de recarga máxima
        self.sub_buttons.append(ctk.CTkButton(self.right_frame, text=n_max, fg_color=color,
            hover_color=self.sub_btn_hover, width=220, height=40, text_color="black",
            command=lambda: self.accion_y_volver_with_sound(self.jugador.energia_carga_max(), sonido_incremento)))
        self.sub_buttons[-1].place(x=255, y=10)
        self.add_volver_submenu()
        self.actualizar_barra_estados()

    # Ejecuta la acción y reproduce sonido, luego regresa menú principal
    def accion_y_volver_with_sound(self, resultado, sound=None):
        if sound: sound.play()
        self.accion_y_volver(resultado)

    # Ejecuta recarga máxima, reproduce sonido y pasa turno
    def accion_recarga_maxima_with_sound(self):
        if sonido_incremento: sonido_incremento.play()
        self.accion_recarga_maxima()

    # Recarga máxima: cambia estado y pasa turno
    def accion_recarga_maxima(self):
        # Agrega estado de recarga máxima si no existe
        if "recarga_maxima" not in self.jugador.estados:
            self.jugador.estados.append("recarga_maxima")
        # Llama a la función específica del personaje para recarga máxima
        resultado = getattr(self.jugador, "consentracion_visual", 
            getattr(self.jugador, "vision_flamante", 
                getattr(self.jugador, "vision_asesina", 
                    getattr(self.jugador, "modo_infinito", 
                        getattr(self.jugador, "vision_apolo", 
                            lambda: "Sin función recarga máxima")))))()
        # Asigna turnos para el estado
        self.jugador.turnos_estado["recarga_maxima"] = 3
        self.insert_user_action(str(resultado) + "\n")
        # Regresa al menú principal y pasa turno al enemigo
        self.eliminar_submenu()
        self.mostrar_botones_principales()
        self.actualizar_barra_estados()
        self.master.after(800, self.turno_enemigo)

    # Ejecuta acción y regresa al menú de botones principales
    def accion_y_volver(self, resultado):
        # Muestra el resultado de la acción si existe
        if resultado is not None:
            if isinstance(resultado, str):
                self.insert_user_action(resultado + "\n")
        # Regresa al menú principal y pasa turno al enemigo
        self.eliminar_submenu()
        self.mostrar_botones_principales()
        self.actualizar_barra_estados()
        self.master.after(800, self.turno_enemigo)

    # Turno del jefe/enemigo, decide aleatoriamente el ataque y chequea condiciones de victoria/derrota
    def turno_enemigo(self):
        if self.fin_juego: return
        if self.enemigo.vida <= 0:
            self.enemigo.vida = 0
            self.actualizar_barras()
            # Detiene música de combate y reproduce música de victoria
            if sonido_combate:
                sonido_combate.stop()
            if sonido_final:
                sonido_final.play()
            self.mostrar_mensaje_final("🎉🎉 ¡GANASTE! El jefe ha sido derrotado. 🎉🎉", "win")
            return
        if self.jugador.vida <= 0:
            self.jugador.vida = 0
            self.actualizar_barras()
            # Detiene música de combate y reproduce música de derrota
            if sonido_combate:
                sonido_combate.stop()
            if sonido_muerte_jefe:
                sonido_muerte_jefe.play()
            self.mostrar_mensaje_final("💀💀 ¡HAS PERDIDO! El jefe te ha derrotado. 💀💀", "loser")
            return
        # El jefe elige ataque normal, especial, definitiva (con sonido explosion) o incremento
        idx = random.choice([0, 1, 2, 3])
        if idx == 0:
            msg = self.enemigo.ataque_normal(self.jugador)
        elif idx == 1:
            msg = self.enemigo.ataque_especial(self.jugador)
        elif idx == 2:
            if sonido_explosion:
                sonido_explosion.play()
            msg = self.enemigo.habilidad_definitiva(self.jugador)
        else:
            msg = self.enemigo.incremento(self.jugador)
        # Muestra el mensaje del turno enemigo
        self.insert_enemy_action(f"Turno enemigo: {msg}\n")
        self.animacion_ataque(self.lbl_jugador, color="#ff0000")
        # Actualiza barras y procesa estados
        self.actualizar_barras()
        self.actualizar_barra_estados()
        self.jugador.procesar_estados()
        self.enemigo.procesar_estados()
        self.actualizar_barra_estados()
        self.actualizar_barras()

    # Crea el sprite (imagen) del personaje o jefe
    def crear_sprite(self, imagen_path, w, h):
        # Carga la imagen del sprite si existe
        img = None
        img_abs_path = resource_path(imagen_path)
        if os.path.exists(img_abs_path):
            img = ctk.CTkImage(light_image=Image.open(img_abs_path).resize((w, h)), size=(w, h))
        # Crea la etiqueta con la imagen o texto alternativo
        lbl = ctk.CTkLabel(self.top_frame, image=img, text="" if img else "SPRITE", width=w, height=h, fg_color="transparent")
        lbl.image_ref = img   # Evita que Python elimine la imagen
        return lbl

    # Oculta los botones principales del panel derecho
    def ocultar_botones_principales(self):
        self.btn_attack.place_forget()
        self.btn_defend.place_forget()
        self.btn_bag.place_forget()
        self.btn_energy.place_forget()

    # Muestra los botones principales del panel derecho
    def mostrar_botones_principales(self):
        self.btn_attack.place(x=15, y=10)
        self.btn_defend.place(x=255, y=10)
        self.btn_bag.place(x=15, y=60)
        self.btn_energy.place(x=255, y=60)
        self.eliminar_submenu()
        self.actualizar_barra_estados()
    
    # Elimina el submenu de acciones secundarias
    def eliminar_submenu(self):
        # Destruye los botones del submenu
        for btn in self.sub_buttons:
            btn.destroy()
        self.sub_buttons.clear()
        # Destruye el frame de estados si existe
        if hasattr(self, "estado_frame_submenu") and self.estado_frame_submenu:
            self.estado_frame_submenu.destroy()
            self.estado_frame_submenu = None
        self.actualizar_barra_estados()

    # Botón para volver al menú principal desde submenús
    def add_volver_submenu(self):
        # Crea el botón de volver al menú principal
        btn_volver_submenu = ctk.CTkButton(
            self.right_frame,
            text="← Volver",
            fg_color="#c5c5c5",
            hover_color="#d1d1d1",
            text_color="#5b4a3a",
            width=460, height=40, corner_radius=10,
            font=("Arial", 15, "bold"),
            command=self.mostrar_botones_principales
        )
        btn_volver_submenu.place(x=15, y=110)
        # Añade el botón a la lista de sub_buttons para su gestión
        self.sub_buttons.append(btn_volver_submenu)

    # Acción de curar estado negativo y reproducir sonido
    def accion_cura_estado_with_sound(self):
        # Reproduce sonido de antídoto
        if sonido_antidoto: sonido_antidoto.play()
        self.accion_cura_estado()

    # Ejecuta la curación de estado negativo y sigue con el turno
    def accion_cura_estado(self):
        # Agrega estado de cura si no existe
        if "cura_estado" not in self.jugador.estados:
            self.jugador.estados.append("cura_estado")
        resultado = getattr(self.jugador, "usar_objeto", lambda t: "Sin función cura estado")("cura_estado")
        # Muestra el resultado de la acción
        self.insert_user_action(str(resultado) + "\n")
        self.eliminar_submenu()
        self.mostrar_botones_principales()
        self.actualizar_barra_estados()
        self.master.after(800, self.turno_enemigo)

    # Muestra mensaje de fin de juego y botones para reintentar o volver a seleccionar personaje
    def mostrar_mensaje_final(self, mensaje, tipo):
        # Marca el fin del juego para evitar más acciones
        self.fin_juego = True
        # Crea overlay de mensaje final
        if self.overlay_final:
            self.overlay_final.destroy()
        self.overlay_final = ctk.CTkFrame(self, fg_color="#000000", width=1200, height=800, corner_radius=0)
        self.overlay_final.place(x=0, y=0, relwidth=1, relheight=1)
        # Mensaje de victoria o derrota
        ctk.CTkLabel(
            self.overlay_final,
            text=mensaje,
            font=("Arial", 48, "bold"),
            text_color="#1e9600" if tipo == "win" else "#c80000"
        ).pack(pady=120)
        # Pregunta y botones para reintentar o seleccionar personaje
        ctk.CTkLabel(
            self.overlay_final,
            text="¿Qué deseas hacer ahora?",
            font=("Arial", 24, "bold"),
            text_color="#7a6b5a"
        ).pack(pady=20)
        btn_frame = ctk.CTkFrame(self.overlay_final, fg_color="transparent")
        btn_frame.pack(pady=40)
        ctk.CTkButton(
            btn_frame, text="Reintentar", fg_color="#f09a21", hover_color="#ce7d15",
            text_color="white", corner_radius=10, width=250, height=60, font=("Arial", 20, "bold"),
            command=self.reintentar
        ).pack(side="left", padx=40)
        ctk.CTkButton(
            btn_frame, text="Seleccionar Personaje", fg_color="#b6dbff", hover_color="#7bb1f9",
            text_color="black", corner_radius=10, width=250, height=60, font=("Arial", 20, "bold"),
            command=self.seleccionar_personaje
        ).pack(side="left", padx=40)

    # Función para reintentar el combate
    def reintentar(self):
        self.overlay_final.destroy()
        # Detiene música de fin y música de jefe muerto si están sonando y reactiva la música combate
        if sonido_final: sonido_final.stop()
        if sonido_muerte_jefe: sonido_muerte_jefe.stop()
        if sonido_combate: sonido_combate.play(-1)
        self.master.iniciar_batalla(type(self.jugador)())

    # Función para regresar a selección de personaje
    def seleccionar_personaje(self):
        self.overlay_final.destroy()
        if sonido_final: sonido_final.stop()
        if sonido_muerte_jefe: sonido_muerte_jefe.stop()
        self.master.mostrar_seleccion()
        # La música de combate se reactiva en SeleccionFrame

    # Actualiza las barras de vida, energía y defensa según los datos actuales
    def actualizar_barras(self):
        # Actualiza barras y etiquetas del jugador
        vida_color_j = "#0af10a" if self.jugador.vida > (self.jugador.vida_max * 0.3) else "#f10e0e"
        self.bar_vida_j.set(max(0, min(self.jugador.vida / self.jugador.vida_max, 1)))
        self.bar_ene_j.set(max(0, min(self.jugador.energia / self.jugador.energia_max, 1)))
        self.bar_def_j.set(max(0, min(self.jugador.defensa / self.jugador.defensa_max, 1)))
        self.bar_vida_j.configure(progress_color=vida_color_j)
        self.lbl_vida_j.configure(text=f"Vida: {int(self.jugador.vida)}/{self.jugador.vida_max}")
        self.lbl_ene_j.configure(text=f"Energía: {int(self.jugador.energia)}/{self.jugador.energia_max}")
        self.lbl_def_j.configure(text=f"Defensa: {int(self.jugador.defensa)}/{self.jugador.defensa_max}")
        # Actualiza barras y etiquetas del enemigo/jefe
        vida_color_e = "#f10e0e" if self.enemigo.vida > (self.enemigo.vida_max * 0.15) else "#f8ec06"
        self.bar_vida_e.set(max(0, min(self.enemigo.vida / self.enemigo.vida_max, 1)))
        self.bar_ene_e.set(max(0, min(self.enemigo.energia / self.enemigo.energia_max, 1)))
        self.bar_def_e.set(max(0, min(self.enemigo.defensa / self.enemigo.defensa_max, 1)))
        self.bar_vida_e.configure(progress_color=vida_color_e)
        self.lbl_vida_e.configure(text=f"Vida: {int(self.enemigo.vida)}/{self.enemigo.vida_max}")
        self.lbl_ene_e.configure(text=f"Energía: {int(self.enemigo.energia)}/{self.enemigo.energia_max}")
        self.lbl_def_e.configure(text=f"Defensa: {int(self.enemigo.defensa)}/{self.enemigo.defensa_max}")

    # Efecto de animación cuando ocurre un ataque (parpadeo y sacudida de la ventana)
    def animacion_ataque(self, objetivo, color="#ff5555"):
        def parpadeo(c, i=0):
            # Parpadea el objetivo 4 veces
            if i < 4:
                objetivo.configure(fg_color=c if i % 2 == 0 else "transparent")
                self.master.after(100, lambda: parpadeo(c, i + 1))
            else:
                objetivo.configure(fg_color="transparent")
        def sacudir(n=0):
            # Sacude la ventana 6 veces
            if n < 6:
                dx = (-1)**n * 10
                dy = (-1)**n * 5
                self.master.geometry(f"1200x800+{self.master.winfo_x()+dx}+{self.master.winfo_y()+dy}")
                self.master.after(40, lambda: sacudir(n + 1))
            else:
                self.master.geometry("1200x800")
        # Crea un flash blanco sobre toda la pantalla
        flash = ctk.CTkFrame(self.top_frame, width=1200, height=500, fg_color="white")
        flash.place(x=0, y=0)
        self.master.after(80, flash.destroy)
        parpadeo(color)
        sacudir()

# Clase principal de la aplicación (pantalla principal)
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("⚔️ Batalla Random")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.pastel_bg = "#f4efe3"
        self.configure(fg_color=self.pastel_bg)
        self.pantalla_actual = None
        # Inicia música de inicio en bucle al arrancar
        try:
            if sonido_inicio:
                sonido_inicio.play(-1)
        except:
            pass
        self.mostrar_menu_inicio()

    # Muestra menú de inicio principal
    def mostrar_menu_inicio(self):
        # Destruye la pantalla actual si existe
        if self.pantalla_actual:
            self.pantalla_actual.destroy()
        # Crea y muestra la pantalla de menú de inicio
        self.pantalla_actual = MenuInicio(self, self)
        self.pantalla_actual.pack(fill="both", expand=True)

    # Muestra pantalla para seleccionar personaje
    def mostrar_seleccion(self):
        # Destruye la pantalla actual si existe
        if self.pantalla_actual:
            self.pantalla_actual.destroy()
        # Crea y muestra la pantalla de selección de personaje
        self.pantalla_actual = SeleccionFrame(self, self)
        self.pantalla_actual.pack(fill="both", expand=True)

    # Inicia batalla con el personaje elegido
    def iniciar_batalla(self, personaje_seleccionado):
        # Destruye la pantalla actual si existe
        if self.pantalla_actual:
            self.pantalla_actual.destroy()
        # Crea instancia del jefe seleccionado
        boss_obj = BOSS_OPTION["clase"]()
        # Detiene la música de inicio y pone música de combate en bucle
        try:
            if sonido_inicio: sonido_inicio.stop()
        except:
            pass
        try:
            if sonido_combate: sonido_combate.play(-1)
        except:
            pass
        # Crea y muestra la pantalla de batalla
        self.pantalla_actual = BatallaFrame(self, personaje_seleccionado, boss_obj)
        self.pantalla_actual.pack(fill="both", expand=True)


        

# Punto de inicio del programa
if __name__ == "__main__":
    root = App()
    root.mainloop()