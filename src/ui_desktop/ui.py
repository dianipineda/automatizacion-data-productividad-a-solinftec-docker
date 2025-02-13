import os
from tkinter import ttk 
import tkinter as tk
from tkinter import StringVar, messagebox, Label, Canvas

from dotenv import load_dotenv
from metadata import VERSION_DESKTOP
from src.config.constants import ABS_PATH_BG_WINDOW, ABS_PATH_ICON_WINDOW, BIG_FONT, FONT, SMALL_FONT, WINDOW_HEIGHT, WINDOW_WIDTH
from src.controllers.ins_productividad import ins_productividad, delete_productividad
from src.utils.database_haciendas import get_haciendas
from src.utils.database_suertes import get_suertes
from src.ui_desktop.common_styles import center_window, set_style_iterable_obj, set_styles
from src.utils.database_productividad import get_fg_dml
from src.utils.database_log_interfaces import ins_logs, update_logs, del_logs
import json
from PIL import Image, ImageTk
from src.ui_desktop.loader import Loader


hacienda_seleccionada = ""
suerte_seleccionada = ""
def vista():
    global hacienda_seleccionada
    global suerte_seleccionada
    window = tk.Tk()
    window.title('Inicio')
    window.geometry(f"{round(WINDOW_WIDTH)}x{round(WINDOW_HEIGHT)}")
    window.resizable(0, 0)
    center_window(window,WINDOW_WIDTH,WINDOW_HEIGHT)
    set_styles()
    set_style_iterable_obj(window)

    # Icono 
    original_logo = Image.open(ABS_PATH_ICON_WINDOW)
    resized_image = original_logo.resize((380,int(169.001182)))
    window.icono = ImageTk.PhotoImage(resized_image)
    window.iconphoto(True, window.icono)

    #? Variables
    clicked_haciendas = StringVar(value="")
    clicked_suertes = StringVar(value="")

    #? fragmento de codigo que evita que se reviente si no hay ping al servidor
    haciendas = get_haciendas()
    if not haciendas:
        return
    
    def actualizar_suertes(*args):
        global hacienda_seleccionada
        hacienda_seleccionada = clicked_haciendas.get()

        if hacienda_seleccionada:
            hacienda_seleccionada = hacienda_seleccionada.strip("(),'\" ")
            suertes = get_suertes(hacienda_seleccionada)
            suerte_combobox["values"] = suertes  # Actualiza las opciones del Combobox
            clicked_suertes.set("")  # Reinicia el Combobox de suertes
        else:
            suerte_combobox["values"] = []
            clicked_suertes.set("")


    def actualizar_suerte_seleccionada(*args):
        global suerte_seleccionada
        suerte_seleccionada = clicked_suertes.get()
        suerte_seleccionada = suerte_seleccionada.strip("(),'\" ")

    # Imagen de fondo
    ancho = 120
    alto = int(53.3687944)
    try:
        bg_image = Image.open(ABS_PATH_BG_WINDOW)
        bg_resized = bg_image.resize((ancho, alto))
        bg_photo = ImageTk.PhotoImage(bg_resized)

        # Canvas para la imagen de fondo
        canvas = Canvas(window, width=ancho+30, height=alto+10)
        canvas.grid(row=0,columnspan=12, rowspan=1)  # espacio que abarca de window
        canvas.create_image(30, 0, image=bg_photo, anchor="nw")
        canvas.image = bg_photo  # Evita que se recolecte el objeto por el garbage collector
    except FileNotFoundError:
        print("No se encontró el archivo de imagen de fondo.")

    # ? espacio inicial     
    label_a = tk.Label(window, text="")
    label_a.grid(row=1, column=1, sticky="W",padx=7, pady=6)

    # Label y Dropdown Haciendas #TODO : Quede aqui para empezar a aplicar estilos
    label_haciendas = ttk.Label(window, text="Haciendas", style="Custom.TLabel")
    label_haciendas.grid(row=1, column=2, sticky="W", pady=6, padx=0)
    hacienda_combobox = ttk.Combobox(window, textvariable=clicked_haciendas, values=haciendas, state="normal", width=5,font=(FONT, BIG_FONT, "bold"))
    hacienda_combobox.grid(row=1, column=3, sticky="E", pady=6, padx=0)

    # para texto de entrada
    hacienda_combobox.bind("<Return>", lambda event: actualizar_suertes())
    # para seleccion en el combobox
    hacienda_combobox.bind("<<ComboboxSelected>>", lambda event: actualizar_suertes())

    #? espacio intermedio entre haciendas y suertes
    espacio = ttk.Label(window, text="",style="Custom.TLabel")  # Label vacío para crear espacio
    espacio.grid(row=1, column=4, padx=15)  # Nueva columna para el espacio

    #? Label y  Dropdown Suertes
    label_suertes = ttk.Label(window,text="Suertes", style="Custom.TLabel")
    label_suertes.grid(row=1, column=5, sticky="W", pady=6, padx=0)
    clicked_suertes.trace_add("write", actualizar_suerte_seleccionada)
    suerte_combobox = ttk.Combobox(window, textvariable=clicked_suertes, state="normal", width=5,font=(FONT, BIG_FONT, "bold"))
    suerte_combobox.grid(row=1, column=6, sticky="E", pady=6, padx=0)

    # funciones de envio
    def mensaje(fg_dml, estado_envio, estado_solinftec):
        # Mapeo de tipos de operación a su descripción
        tipo_operacion = {
            'I': "Inserción",
            'A': "Actualización",
            'E': "Anulación"
        }
        
        # Mapeo de estados a mensajes específicos
        mensajes_estado = {
            "FULLY_PROCESSED": f"Todos los datos fueron recibidos correctamente para ser procesados como {tipo_operacion[fg_dml]} por el sistema de Solinftec.\n\n"
                            f"Estado de envío: {estado_envio}\n"
                            f"Estado de recepción de datos en servidor de Solinftec: FULLY_PROCESSED",
            "PROCESSED": f"Todos los datos fueron recibidos correctamente para ser procesados como {tipo_operacion[fg_dml]} por el sistema de Solinftec.\n\n"
                        f"Estado de envío: {estado_envio}\n"
                        f"Estado de recepción de datos en servidor de Solinftec: PROCESSED",
            "PARTIALLY_PROCESSED": f"Algunos datos se recibieron correctamente y otros tenían errores en la {tipo_operacion[fg_dml]} por el sistema de Solinftec.\n\n"
                                f"Estado de envío: {estado_envio}\n"
                                f"Estado de recepción de datos en servidor de Solinftec: PARTIALLY_PROCESSED",
            "PENDING": f"La integración aún se está ejecutando para la validación de los datos enviados en el proceso de {tipo_operacion[fg_dml]} por el sistema de Solinftec.\n\n"
                            f"Estado de envío: {estado_envio}\n"
                            f"Estado de recepción de datos en servidor de Solinftec: PENDING",
            "ERROR": f"Se encontraron errores en todos los datos enviados en el proceso de {tipo_operacion[fg_dml]} por el sistema de Solinftec.\n\n"
                        f"Estado de envío: {estado_envio}\n"
                        f"Estado de recepción de datos en servidor de Solinftec: ERROR"
        }
        
        # Validación de entrada
        if fg_dml in tipo_operacion and estado_solinftec in mensajes_estado:
            messagebox.showinfo("Información de la integración con Solinftec", mensajes_estado[estado_solinftec])

    def manejo_solinftec(estado_solinftec, estado_envio,registros_productividad):
        if estado_solinftec in ['FULLY_PROCESSED', 'PROCESSED','PARTIALLY_PROCESSED','PENDING','ERROR']:
            if get_fg_dml() == 'I':
                for row in registros_productividad:
                    row["status_solinftec"] = estado_solinftec
                    registro=json.dumps(row)
                    ins_logs(row["cd_ordem_servico"],row["cd_fazenda"],row["cd_zona"],row["cd_talhao"],registro)
                mensaje(get_fg_dml(),estado_envio,estado_solinftec)			
                
            if get_fg_dml() == 'A':
                for row in registros_productividad:
                    row["status_solinftec"] = estado_solinftec
                    registro=json.dumps(row)
                    update_logs(row["cd_fazenda"],row["cd_zona"],registro)
                mensaje(get_fg_dml(),estado_envio,estado_solinftec)	

            if get_fg_dml() == 'E':
                for row in registros_productividad:
                    del_logs(row["cd_ordem_servico"],row["cd_talhao"])
                mensaje(get_fg_dml(),estado_envio,estado_solinftec)	
		
    def manejo_respuesta(accion):
        global fg_dml
        global hacienda_seleccionada
        global suerte_seleccionada

        if not hacienda_seleccionada and not suerte_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor seleccione una hacienda y una suerte.")
            return

        if not hacienda_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor seleccione una hacienda.")
            return

        if not suerte_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor seleccione una suerte.")
            return
        
        # if '.' in suerte_seleccionada:
        #     messagebox.showwarning("Advertencia", "Las suertes que contienen '.' no son una ópción válida")
        #     return
        
        # Determinar la función a usar según la acción
        if accion == "anular":
            response = delete_productividad()
        elif accion == "enviar":
            response = ins_productividad()
        else:
            messagebox.showerror("Error", "Acción no válida.")
            return
			
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
            respuesta_json = json.loads((response.get("data")))
            registros_productividad = respuesta_json.get("data")
            estado_solinftec = response.get('get_response')
            estado_envio = response['status_code']      
            manejo_solinftec(estado_solinftec,estado_envio,registros_productividad)

        # Resetear los valores de los Dropdowns
        clicked_haciendas.set("")
        clicked_suertes.set("")
        hacienda_seleccionada = ""
        suerte_seleccionada = ""

    def enviar():
        window.withdraw()
        loader = Loader()
        loader.show()
        try:
            manejo_respuesta("enviar")
        except Exception as e:
            messagebox.showerror("Error",f"Error inesperado al intentar enviar la solicitud: {e}")
        finally:
            if loader is not None and loader.winfo_exists():
                loader.hide()
            window.deiconify()
    
    def anular():
        window.withdraw()
        loader = Loader()
        loader.show()
        try:
            manejo_respuesta("anular")
        except Exception as e:
            messagebox.showerror("Error",f"Error inesperado al intentar anular la solicitud: {e}")
        finally:
            if loader is not None and loader.winfo_exists():
                loader.hide()
            window.deiconify()


    #? Botón de enviar     style="Custom.TButton"  style="Custom_Revert.TButton"
    button = ttk.Button(window, text="Enviar", command=enviar, style="Custom.TButton")
    button.grid(row=3, column=2, columnspan=6, pady=30, sticky="W")


    #? Botón Eliminar
    button = ttk.Button(window, text="Anular", command=anular, style="Custom_Revert.TButton")
    button.grid(row=3, column=4, columnspan=6, pady=30, sticky="E")   

    #? cerrar la aplicacion
    def on_close_app(window):
        """
        Función para confirmar el cierre de una ventana en Tkinter.

        Args:
            window (tk.Tk): La ventana que se va a cerrar.
        """
        if messagebox.askokcancel("Salir", "¿Seguro que deseas cerrar la aplicación?"):
            window.destroy() 
    window.protocol("WM_DELETE_WINDOW", lambda: on_close_app(window))

    #? Footer
    footer = tk.Label(
        window,
        text=f"Aplicativo Integración Productividad a Solinftec - Versión: {VERSION_DESKTOP}",
        anchor="w",
        font=(FONT, SMALL_FONT,"italic"),)
    footer.place(x=232, y=200, anchor="se")

    window.mainloop()

if __name__ == "__main__":
    vista()
