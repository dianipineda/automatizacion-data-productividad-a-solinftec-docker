import tkinter as tk
from src.ui_desktop.common_styles import center_window

class Loader(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("400x200")
        self.title("Cargando...")
        self.label = tk.Label(self, text="Cargando, por favor espere...")
        self.label.pack(pady=20)
        self.resizable(0,0)

        # Tamaño de la ventana
        window_width = 400
        window_height = 200

        # Centrar la ventana
        center_window(self, window_width, window_height)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        pass  # Previene que se cierre el loader manualmente

    def show(self):
        self.deiconify()  # Muestra la ventana
        self.grab_set()    # Bloquea la ventana principal

    def hide(self):
        self.grab_release()  # Libera la ventana principal
        self.withdraw()      # Oculta la ventana
