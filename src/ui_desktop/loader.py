import tkinter as tk
from src.ui_desktop.common_styles import center_window

class Loader(tk.Toplevel):
    def __init__(self):
        super().__init__()
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
        """Muestra la ventana de carga y bloquea la interacción con la ventana principal"""
        self.deiconify()  # Muestra la ventana si está oculta
        self.update_idletasks()  # 🔹 Fuerza la actualización de la interfaz
        self.grab_set()  # 🔹 Bloquea la interacción con otras ventanas
        self.update()  # 🔹 Refresca la ventana inmediatamente  
    def hide(self):
        """Oculta la ventana de carga y libera la interacción con la ventana principal"""
        self.grab_release()  
        self.withdraw()      
