import tkinter as tk
from tkinter import StringVar, messagebox, OptionMenu
# from src.controllers.ins_productividad import ins_productividad
from src.utils.database_haciendas import get_haciendas
from src.utils.database_suertes import get_suertes

hacienda_seleccionada = "106"
suerte_seleccionada = "14"
def vista():
    window = tk.Tk()
    window.title('Productividad de Haciendas Suerte')
    window.geometry("296x265")
    window.resizable(0,0)
    #TODO: Quedé aqui: debo implementar dropdowns para haciendas y suertes
          
    # DropDown Haciendas
    clicked_haciendas = StringVar() # datatype of dropMenu_haciendas
    dropMenu_haciendas = OptionMenu(window, clicked_haciendas, *get_haciendas())
    dropMenu_haciendas.grid(row=0,column=0)
    print("*** Hasta aqui funciona")

    # DropDown Suertes
    clicked_suertes = StringVar() # datatype of dropMenu_suertes
    dropMenu_suertes = OptionMenu(window, clicked_suertes, *get_suertes())
    dropMenu_suertes.grid(row=0,column=1)
    print("*** Hasta aqui funciona 2")
    
    # hacienda_seleccionada = clicked_haciendas.get()
    # suerte_seleccionada = clicked_suertes.get()

    def enviar():
        if 'ins_productividad' in globals():
            return
        else:
            from src.controllers.ins_productividad import ins_productividad
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
    button = tk.Button(window, text="Enviar", command=enviar)
    button.grid(row=1,column=0)

    window.mainloop()