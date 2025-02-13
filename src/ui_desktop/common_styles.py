from tkinter import ttk
from src.config.constants import BIG_FONT, FONT
import tkinter.font as tkFont

# Función para centrar una ventana
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)    
    window.geometry(f"{round(width)}x{round(height)}+{round(x)}+{round(y)}")   

def set_styles() -> None:
    """
    Configura y centraliza los estilos personalizados para el proyecto.
    
    Esta función establece los estilos predeterminados para varios widgets de 
    tkinter como Combobox, Entry, Label y Button. Personaliza la apariencia de
    los botones en función de sus estados (presionado, activo).
    """
    style = ttk.Style()
    style.theme_use("clam")

    # Estilos personalizados
    # style.configure("Custom.TCombobox", font=(FONT, 10, "bold")) # nota: este estilo no funciona en los combobox de la ventana get_connections_window
    style.configure("Custom.TEntry", font=(FONT, BIG_FONT, "bold"))
    style.configure("Custom.TLabel", font=(FONT, BIG_FONT, "bold"), background="#f0f0f0")

    style.configure("Custom.TButton", font=(FONT, BIG_FONT, "bold"), foreground="#fff", background="#006B37",width=10)
    style.map("Custom.TButton",
        background=[('pressed', '#006B37'), ('active', '#c7dcd2')],
        relief=[('pressed', 'groove'), ('active', 'raised')]
    )
    style.configure("Custom_Revert.TButton", font=(FONT, BIG_FONT, "bold"), foreground="#fff", background="#E5006D",width=10)
    style.map("Custom_Revert.TButton",
        background=[('pressed', '#E5006D'), ('active', '#f2bcc8')],
        relief=[('pressed', 'groove'), ('active', 'raised')]
    )
    style.configure("Custom_Cal.TButton", font=(FONT, BIG_FONT), padding=0, background="SystemButtonFace", anchor="center", justify="center",width=10)
    style.map("Custom_Cal.TButton",
        background=[('pressed', '#006C38'), ('active', '#c7dcd2')],
        relief=[('pressed', 'groove'), ('active', 'raised')]
    )

def set_style_iterable_obj(window) -> None:
    """
    Aplica el estilo definido en widgets que tengan como valores objetos iterables tales como
    listas, diccionarios. Los widgets a los que aplicaria son Combobox...
    """
    bigfont:tkFont.Font = tkFont.Font(family=FONT, size=BIG_FONT)  # Crear fuente para los items de la lista desplegable
    window.option_add("*TCombobox*Listbox*Font", bigfont)  # Ahora sí funcionará

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

