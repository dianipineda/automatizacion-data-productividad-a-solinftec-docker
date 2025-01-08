import oracledb
from src.utils.coneccion_db import connection_db, configurar_cliente_oracle
import socket
import os
from tkinter import messagebox
"""
Nota: Trayecto de la DATA:
data importada
parametro_ayer_formateado: date que viene de connecion_db.py
"""
configurar_cliente_oracle()
def query_get_haciendas():
    return """
        SELECT DISTINCT
            vw.faz AS cd_fazenda
        FROM
            user_carmelita.historia vw
        LEFT JOIN (
            SELECT
                p1,
                p3
            FROM
                user_carmelita.tab_lq_dados
            WHERE
                codigo = 'CARTO_SOLI'
        ) tl ON tl.p1 = vw.faz
        WHERE
            vw.data_ultcol BETWEEN current_date - 60 AND current_date
            AND tl.p3 IS NOT NULL
            AND vw.ton_mol > 0
        ORDER BY
            vw.faz

    """
def get_haciendas():
    try: 
        connection = connection_db()  
        if not connection:
            raise Exception("No se pudo establecer la conexión a la base de datos.")       
        cursor = connection.cursor()
        query = query_get_haciendas()
        cursor.execute(
            query
        )
        results = cursor.fetchall()
        if results == []:
            messagebox.showinfo("Información","No hay resultados de 'Haciendas' en la consulta realizada.")
            return []
        else:
            return results

    except oracledb.DatabaseError as e:
        messagebox.showerror("Error",f"Error en la base de datos en haciendas: {e}")
    except oracledb.InterfaceError as e:
        messagebox.showerror("Error",f"No se pudo establecer una conexión con la base de datos. Verifica la configuración de red y el cliente Oracle: {e}")
    except socket.gaierror as e:
        messagebox.showerror("Error",f"Error de red: No se pudo resolver el host {os.getenv('DB_HOST')}. Detalles: {e}")
    except Exception as e:
        #TODO: Quedé aquí error expected 2, got 1: Ocurrencia: cuando el servidor a pesar de estar levantado y el puerto abierto, problemas internos del servidor
        messagebox.showerror(
            "Error",
            f"Ocurrió un error inesperado en el filtro de haciendas: {e}\n"
            f"Existe un problema interno en el servidor de base de datos, por favor revisa los logs de este servidor. Soluciona estos problemas e intenta nuevamente\n\n"
            f"Posibles causas:\n"
            f"Problemas en las reglas del Firewall del servidor\n"
            f"Límite de Memoria o CPU en el servidor\n"
            f"Para un diagnóstico más acertado, consulta a tu administrador de base de datos"
        )
    finally:
        try:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection_db():
                connection_db().close()
        except Exception as close_error:
            messagebox.showerror("Error",f"Error al cerrar recursos: {close_error}")
