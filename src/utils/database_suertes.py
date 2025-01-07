import oracledb
from src.utils.coneccion_db import connection_db, configurar_cliente_oracle
import socket
import os
from tkinter import messagebox

"""
Nota: Trayecto de la DATA: 
Aqui no se importa ninguna data
"""
configurar_cliente_oracle()
def query_get_suertes(hacienda):
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
        ) tl ON tl.p2 = vw.tal
        WHERE
            vw.data_ultcol between current_date-60 AND current_date
            AND vw.ton_mol > 0
            AND vw.faz = :hacienda
        ORDER BY
            vw.tal
    """
def get_suertes(hacienda):
    try:
        connection = connection_db()  
        if not connection:
            raise Exception("No se pudo establecer la conexión a la base de datos.")       
        cursor = connection.cursor()
        query = query_get_suertes(hacienda)
        # print("query_suertes: ", query_suertes)
        cursor.execute(query, {
            'hacienda':hacienda
        })
        suertes = cursor.fetchall()
        if suertes == []:
            messagebox.showinfo("No hay resultados de 'Suertes' en la consulta realizada.")
            return
        else:
            return suertes
    except oracledb.DatabaseError as e:
        messagebox.showerror("Error",f"Error en la base de datos en suertes: {e}")
    except oracledb.InterfaceError as e:
        messagebox.showerror("Error",f"No se pudo establecer una conexión con la base de datos. Verifica la configuración de red y el cliente Oracle: {e}")
    except socket.gaierror as e:
        messagebox.showerror("Error",f"Error de red: No se pudo resolver el host {os.getenv('DB_HOST')}. Detalles: {e}")
    except Exception as e:
        messagebox.showerror("Error",f"Ocurrió un error inesperado en la obtención de suertes por hacienda: {e}")
    finally:
        try:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection_db():
                connection_db().close()
        except Exception as close_error:
            messagebox.showerror("Error",f"Error al cerrar recursos: {close_error}")

