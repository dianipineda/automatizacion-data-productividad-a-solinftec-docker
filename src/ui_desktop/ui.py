import tkinter as tk
from tkinter import StringVar, messagebox, OptionMenu
from src.controllers.ins_productividad import ins_productividad
from src.utils.database_haciendas import get_haciendas
from src.utils.database_suertes import get_suertes
from src.ui_desktop.common_styles import center_window
import oracledb

hacienda_seleccionada = ""
suerte_seleccionada = ""
def vista():
    global hacienda_seleccionada
    global suerte_seleccionada
    window_width = 296
    window_height = 200
    window = tk.Tk()
    window.title('Inicio')
    window.geometry(f"{window_width}x{window_height}")
    window.resizable(0, 0)
    center_window(window,window_width,window_height)

    # Variables
    clicked_haciendas = StringVar()
    clicked_suertes = StringVar()

    # fragmento de codigo que evita que se reviente si no hay ping al servidor
    haciendas = get_haciendas()
    if not haciendas:
        return
    
    def actualizar_suertes(*args):
        global hacienda_seleccionada
        hacienda_seleccionada = clicked_haciendas.get()

        if hacienda_seleccionada:
            hacienda_seleccionada = hacienda_seleccionada.strip("(),'\" ")
            suertes = get_suertes(hacienda_seleccionada)
            clicked_suertes.set("")
            dropDownMenu_suertes["menu"].delete(0, "end")
            for suerte in suertes:
                dropDownMenu_suertes["menu"].add_command(
                    label=suerte, command=lambda value=suerte: clicked_suertes.set(value)
                )
        else:
            clicked_suertes.set("")
            dropDownMenu_suertes["menu"].delete(0, "end")

    def actualizar_suerte_seleccionada(*args):
        global suerte_seleccionada
        suerte_seleccionada = clicked_suertes.get()
        suerte_seleccionada = suerte_seleccionada.strip("(),'\" ")
        # print("la suerte seleccionada es: ", suerte_seleccionada)
    # Dropdown Haciendas
    clicked_haciendas.trace_add("write", actualizar_suertes)  # Usando trace_add en lugar de trace
    dropDownMenu_haciendas = OptionMenu(window, clicked_haciendas, *get_haciendas())
    dropDownMenu_haciendas.grid(row=0, column=0)

    # Dropdown Suertes
    clicked_suertes.trace_add("write", actualizar_suerte_seleccionada)
    dropDownMenu_suertes = OptionMenu(window, clicked_suertes, "")
    dropDownMenu_suertes.grid(row=0, column=1)

    # Botón de enviar
    def enviar():
        if not hacienda_seleccionada:
            messagebox.showerror("Error", "Por favor seleccione una hacienda.")
            return

        if not suerte_seleccionada:
            messagebox.showerror("Error", "Por favor seleccione una suerte.")
            return
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
            # messagebox.showinfo("Éxito", "Datos enviados correctamente.")

    button = tk.Button(window, text="Enviar", command=enviar)
    button.grid(row=1, column=0)

    window.mainloop()


if __name__ == "__main__":
    vista()
