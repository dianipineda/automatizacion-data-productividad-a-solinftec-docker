import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Función para centrar una ventana
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)    
    window.geometry(f"{width}x{height}+{x}+{y}")    

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="",*args,**kwargs):
        super().__init__(master,*args,**kwargs)
        self.placeholder = placeholder = placeholder
        # Crear un estilo para el placeholder
        self.style = ttk.Style()
        self.style.configure("Placeholder.TEntry", foreground="grey")
        self.style.configure("Normal.TEntry", foreground="black")

        self.bind("<FocusIn>", self.on_focus)
        self.bind("<FocusOut>", self.on_focusout)
        self.insert(0, self.placeholder)
        self.configure(style="Placeholder.TEntry") 

    def on_focus(self, event):
        if self.get() == self.placeholder:
            self.delete(0, 'end')
            self.configure(style="Normal.TEntry")

    def on_focusout(self, event):
        if self.get() == '':
            self.insert(0, self.placeholder)
            self.configure(style="Placeholder.TEntry")