import tkinter as tk
from tkinter import StringVar, messagebox, OptionMenu
# from src.controllers.ins_productividad import ins_productividad
from src.controllers.ins_productividad import ins_productividad
from src.utils.database_haciendas import get_haciendas
# from src.utils.database_suertes import get_suertes
import oracledb
from src.utils.coneccion_db import connection_db, configurar_cliente_oracle, parametro_ayer_formateado


def vista():
    window = tk.Tk()
    window.title('Productividad de Haciendas Suerte')
    window.geometry("296x265")
    window.resizable(0, 0)

    configurar_cliente_oracle()
    def query_get_suertes(parametro_ayer_formateado,faz):
        return """
        SELECT DISTINCT
            vw.tal AS cd_zona
        FROM
            user_carmelita.historia vw
        LEFT JOIN (
            SELECT
                p2,
                p3
            FROM
                user_carmelita.tab_lq_dados
            WHERE
                codigo = 'CARTO_SOLI'
        )       tl ON tl.p1 = vw.faz
                AND tl ON tl.p2 = vw.tal
        WHERE
            vw.data_ultcol BETWEEN TO_DATE(:parametro_ayer_formateado, 'DD/MM/YYYY') - 30 AND TO_DATE(:parametro_ayer_formateado, 'DD/MM/YYYY')
            AND vw.ton_mol > 0
            AND vw.faz = :faz
        ORDER BY
            vw.tal
        """

    # Variables
    clicked_haciendas = StringVar()
    clicked_suertes = StringVar()

    # Callback para actualizar `dropMenu_suertes`
    def actualizar_suertes(*args):
        hacienda_seleccionada = clicked_haciendas.get()
        
        #TODO: Implementar validaciones de get_productividad()
        def get_suertes(hacienda_seleccionada):
            try:
                cursor_suertes = connection_db().cursor()
                query_suertes = query_get_suertes(parametro_ayer_formateado,hacienda_seleccionada)
                print("query_suertes: ", query_suertes)
                cursor_suertes.execute(query_suertes, {
                    'parametro_ayer_formateado':parametro_ayer_formateado,
                    'faz':hacienda_seleccionada
                })
                suertes = cursor_suertes.fetchall()
                if suertes == []:
                    print("No hay resultados de la consulta realizada")
                    return
                else:
                    # print("---------->", suertes)
                    return suertes
            except oracledb.DatabaseError as e:
                print(f"Error en la base de datos en suertes: {e}")

        # if hacienda_seleccionada:  # Si hay una hacienda seleccionada
        #     print("hacienda seleccionada: ", type(hacienda_seleccionada))
        #     suertes = get_suertes(hacienda_seleccionada)
        #     print("suertes: ", suertes)
        #     clicked_suertes.set("")  # Resetea el valor seleccionado
        #     dropMenu_suertes["menu"].delete(0, "end")  # Limpia las opciones previas
        #     for suerte in suertes:
        #         dropMenu_suertes["menu"].add_command(
        #             label=suerte, command=lambda value=suerte: clicked_suertes.set(value)
        #         )
        # else:  # Si no hay una hacienda seleccionada, limpia el menú
        #     clicked_suertes.set("")
        #     dropMenu_suertes["menu"].delete(0, "end")

    # Dropdown Haciendas
    clicked_haciendas.trace_add("write", actualizar_suertes)  # Usando trace_add en lugar de trace
    dropMenu_haciendas = OptionMenu(window, clicked_haciendas, *get_haciendas())
    dropMenu_haciendas.grid(row=0, column=0)

    # Dropdown Suertes
    # dropMenu_suertes = OptionMenu(window, clicked_suertes, "")
    # dropMenu_suertes.grid(row=0, column=1)

    # Botón de enviar
    def enviar():
        # hacienda_seleccionada = clicked_haciendas.get()
        # suerte_seleccionada = clicked_suertes.get()

        # if not hacienda_seleccionada:
        #     messagebox.showerror("Error", "Seleccione una hacienda.")
        #     return

        # if not suerte_seleccionada:
        #     messagebox.showerror("Error", "Seleccione una suerte.")
        #     return

        # # Aquí iría la lógica de enviar con `ins_productividad`
        # print(f"Hacienda seleccionada: {hacienda_seleccionada}")
        # print(f"Suerte seleccionada: {suerte_seleccionada}")
        # messagebox.showinfo("Éxito", "Datos enviados correctamente.")

        #################################################################
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
    button.grid(row=1, column=0)

    window.mainloop()


if __name__ == "__main__":
    vista()
