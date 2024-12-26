import tkinter as tk
from tkinter import StringVar, messagebox, OptionMenu
from src.controllers.ins_productividad import ins_productividad
from src.utils.database import get_haciendas, get_suertes

def vista():
    window = tk.Tk()
    window.title('Productividad de Haciendas Suerte')
    #TODO: Quedé aqui: debo implementar dropdowns para haciendas y suertes
    
    def enviar():
        response = ins_productividad()
        if "error" in response:
            if response["error"] == "connection":
                messagebox.showerror("Error de conexión", f"Error de conexión: {response['details']}\nURL: {response['url']}")
            elif response["error"] == "http":
                messagebox.showerror(
                    "Error HTTP",
                    f"Error HTTP: {response['details']}\nCódigo de estado: {response['status_code']}"
                )
            elif response["error"] == "timeout":
                messagebox.showerror(
                    "Error de timeout",
                    f"Error de timeout: {response['details']}\nURL: {response['url']}"
                )
            elif response["error"] == "max_retries":
                messagebox.showerror(
                    "Error de max_retries",
                    f"Error de max_retries: {response['details']}\nURL: {response['url']}"
                )
            else:
                messagebox.showerror("Error inesperado", f"Error inesperado: {response['details']}\nURL: {response['url']}")
        else:
            messagebox.showinfo("Éxito", f"Solicitud completada con éxito.\nEstado: {response['status_code']}")
    
    # DropDown Haciendas
    clicked_haciendas = StringVar() # datatype of dropMenu_haciendas
    dropMenu_haciendas = OptionMenu(window, clicked_haciendas, *get_haciendas())
    dropMenu_haciendas.grid(row=0,column=0)

    # DropDown Suertes
    get_suertes()
    clicked_suertes = StringVar() # datatype of dropMenu_suertes
    dropMenu_suertes = OptionMenu(window, clicked_suertes, *get_suertes())
    dropMenu_suertes.grid(row=0,column=1)

    button = tk.Button(window, text="Enviar", command=enviar)
    button.grid(row=1,column=0)
    window.mainloop()