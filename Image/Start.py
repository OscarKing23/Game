# importaciones necesarias
import os
import sys
import customtkinter as ctk
from PIL import Image, ImageTk

# Función para obtener la ruta correcta de los recursos, útil para PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Clase para el menú de inicio
class MenuInicio(ctk.CTkFrame):
    # Inicialización del frame de inicio
    def __init__(self, master, app_controller, **kwargs):
        # Inicialización del frame
        super().__init__(master, **kwargs)
        self.app_controller = app_controller
        # Configuración del frame principal
        self.configure(fg_color=master.pastel_bg)

        # Fondo animado (Canvas estándar)
        self.canvas = ctk.CTkCanvas(self, width=1200, height=800, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Variables para animación de fondo
        self.bg_image_id = None
        self.bg_x = 0
        self.bg_direction = 1  # 1 = derecha, -1 = izquierda

        # Cargar imagen de fondo
        ruta=resource_path("Image/inicial.jpg")
        if os.path.exists(ruta):
            bg_img = Image.open(resource_path("Image/inicial.jpg")).resize((1600, 800))
            # Crear PhotoImage y agregar al canvas
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            self.bg_image_id = self.canvas.create_image(self.bg_x, 0, image=self.bg_photo, anchor="nw")
            # Iniciar animación de fondo
            self.animar_fondo()

        # Contenedor principal encima del canvas (ahora transparente)
        frame_contenido = ctk.CTkFrame(self.canvas, fg_color="transparent", corner_radius=20, width=600, height=400)
        self.frame_contenido_window = self.canvas.create_window(800, 400, window=frame_contenido)

        # Elementos del menú de inicio
        ctk.CTkLabel(frame_contenido, text="⚔️ BATALLA RANDOM ⚔️", 
                     font=("Arial", 40, "bold"), text_color="#3a3a3a", fg_color="transparent").pack(pady=40)
        ctk.CTkLabel(frame_contenido, text="Da click en iniciar juego para comenzar", 
                     font=("Arial", 20, "italic"), text_color="#6a5a3a", fg_color="transparent").pack(pady=10)

        # Botón para iniciar el juego
        ctk.CTkButton(frame_contenido, text="▶️ Iniciar Juego", 
                      font=("Arial", 24, "bold"),
                      fg_color="#f09a21", hover_color="#ce7d15", text_color="white",
                      width=250, height=60, corner_radius=15,
                      command=self.app_controller.mostrar_seleccion).pack(pady=60)

        # Créditos
        ctk.CTkLabel(frame_contenido, text="© 2025 Creadores del juego - Oscar y Axel", 
                     font=("Arial", 12), text_color="#5a5a5a", fg_color="transparent").pack(side="bottom", pady=10)

    def animar_fondo(self):
        # Animación simple de desplazamiento del fondo
        if not self.bg_image_id:
            return
        self.bg_x += self.bg_direction * 1
        # mover la imagen en el canvas
        self.canvas.move(self.bg_image_id, self.bg_direction * 1, 0)
        # Revertir dirección al alcanzar límites
        if self.bg_x >= 15 or self.bg_x <= -70:
            self.bg_direction *= -1
        # Programar siguiente frame de animación
        self.after(30, self.animar_fondo)