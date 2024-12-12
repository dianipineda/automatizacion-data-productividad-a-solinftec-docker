import tkinter as tk
from src.controllers.ins_productividad import ins_productividad

def vista():
    window = tk.Tk()
    window.title('Productividad de Haciendas Suerte')
    def enviar():
        response = ins_productividad()
        print(f"la respuesta es: {response}")
    button = tk.Button(window, text="Enviar", command=enviar)
    button.pack()

    window.mainloop()