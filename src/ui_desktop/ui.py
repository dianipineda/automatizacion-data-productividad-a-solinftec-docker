import tkinter as tk
from tkinter import StringVar, messagebox, OptionMenu
from src.controllers.ins_productividad import ins_productividad
from src.utils.database_haciendas import get_haciendas
from src.utils.database_suertes import get_suertes
from src.ui_desktop.common_styles import center_window
import oracledb
from src.utils.database_productividad import get_fg_dml
from src.utils.database_log_interfaces import get_logs_by_fields, ins_logs, update_logs
import json

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

    #? Variables
    clicked_haciendas = StringVar()
    clicked_suertes = StringVar()

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
    #? Dropdown Haciendas
    clicked_haciendas.trace_add("write", actualizar_suertes)  # Usando trace_add en lugar de trace
    dropDownMenu_haciendas = OptionMenu(window, clicked_haciendas, *get_haciendas())
    dropDownMenu_haciendas.grid(row=0, column=0)

    #? Dropdown Suertes
    clicked_suertes.trace_add("write", actualizar_suerte_seleccionada)
    dropDownMenu_suertes = OptionMenu(window, clicked_suertes, "")
    dropDownMenu_suertes.grid(row=0, column=1)

    # funciones de envio
    def mensaje_exitoso(fg_dml, estado_envio, estado_solinftec):
        # Mapeo de tipos de operación a su descripción
        tipo_operacion = {
            'I': "Inserción",
            'A': "Actualización"
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
                                f"Estado de recepción de datos en servidor de Solinftec: PARTIALLY_PROCESSED"
        }
        
        # Validación de entrada
        if fg_dml in tipo_operacion and estado_solinftec in mensajes_estado:
            # tipo = tipo_operacion[fg_dml]
            # mensaje = mensajes_estado[estado_solinftec].format(tipo_operacion=tipo, estado_solinftec=estado_solinftec)
            messagebox.showinfo("Éxito", mensajes_estado[estado_solinftec])

    def mensaje_erroneo(fg_dml, estado_envio,estado_solinftec):
        # Mapeo de tipos de operación a su descripción
        tipo_operacion = {
            'I': "Inserción",
            'A': "Actualización"
        }
        
        # Mapeo de estados a mensajes específicos
        mensajes_estado = {
            #todo: Reunion con Joao para darle manejo al estado PENDING: Sucede que si un pending
            #todo  se resuelve sin que yo lo sepa, no tengo forma de saber si dio error o si inserto 
            #todo los datos. Como esto no quueda en mis logs , la proxima vez que vuelva a enviar datos
            #todo  lo hara como insercion debido a que no tengo logs , y si estos ya estan en el sistema, me dara estado_solinftec: "ERROR"
            "PENDING": f"La integración aún se está ejecutando para la validación de los datos enviados en el proceso de {tipo_operacion[fg_dml]} por el sistema de Solinftec.\n\n"
                            f"Estado de envío: {estado_envio}\n"
                            f"Estado de recepción de datos en servidor de Solinftec: PENDING",
            "ERROR": f"Se encontraron errores en todos los datos enviados en el proceso de {tipo_operacion[fg_dml]} por el sistema de Solinftec.\n\n"
                        f"Estado de envío: {estado_envio}\n"
                        f"Estado de recepción de datos en servidor de Solinftec: ERROR"
        }
        
        # Validación de entrada
        if fg_dml in tipo_operacion and estado_solinftec in mensajes_estado:
            # tipo = tipo_operacion[fg_dml]
            # mensaje = mensajes_estado[estado_solinftec].format(tipo_operacion=tipo, estado_solinftec=estado_solinftec)
            messagebox.showinfo("Error", mensajes_estado[estado_solinftec])

    def manejo_solinftec(estado_solinftec, estado_envio,registros_productividad):
        if estado_solinftec in ['FULLY_PROCESSED', 'PROCESSED','PARTIALLY_PROCESSED']:
            if get_fg_dml() == 'I':
                for row in registros_productividad:
                    row["status_solinftec"] = estado_solinftec
                    ins_logs(int(row["cd_ordem_servico"]),row["cd_fazenda"],row["cd_zona"],row["cd_talhao"],row)
                mensaje_exitoso(get_fg_dml(),estado_envio,estado_solinftec)			
                
            if get_fg_dml() == 'A':
                for row in registros_productividad:
                    row["status_solinftec"] = estado_solinftec
                    registro=json.dumps(row)
                    update_logs(row["cd_fazenda"],row["cd_zona"],registro)
                mensaje_exitoso(get_fg_dml(),estado_envio,estado_solinftec)	
        if estado_solinftec in ['PENDING','ERROR']:
            if get_fg_dml() == 'I':
                mensaje_erroneo(get_fg_dml(),estado_envio,estado_solinftec)
            if get_fg_dml() == 'A':
                mensaje_erroneo(get_fg_dml(),estado_envio,estado_solinftec)
    #? Botón de enviar
    def enviar():
        global fg_dml
        global hacienda_seleccionada
        global suerte_seleccionada
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
        else: # cuando el endpoint de envio con ins_productividad() fue Exitoso
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
        # dropDownMenu_suertes["menu"].delete(0, "end")  # Limpia el menú de suertes
    button = tk.Button(window, text="Enviar", command=enviar)
    button.grid(row=1, column=0)

    window.mainloop()


if __name__ == "__main__":
    vista()
