import oracledb
import json
import os
import socket
from src.utils.coneccion_db import connection_db, configurar_cliente_oracle
from src.utils.database_log_interfaces import get_logs_by_fields, ins_logs, update_logs
from datetime import datetime, timedelta
from tkinter import messagebox

"""
Nota: Trayecto de la DATA:
data importada
hacienda_seleccionada, suerte_seleccionada: str que viene de ui.py
"""
fg_dml = ""

def set_fg_dml(value):
    global fg_dml
    fg_dml = value

def get_fg_dml():
    return fg_dml

configurar_cliente_oracle()
       
def query_get_productividad(hacienda, suerte):
    return """
    SELECT
            '1'                      cd_unidade,
            '9249'                   cd_operacao,
            tl.p1||substr(tl.p2,1, INSTR(tl.p2,'.', 1, 1)-1  ) || substr(tl.p2,INSTR(vw.tal,'.', 1, 1)+1,1   )||vw.safra cd_ordem_servico,
            tl.p1                   cd_fazenda,
            tl.p2                   cd_zona,
            tl.p3                    cd_talhao,
            vw.data_ultcol           dt_inicial,
            vw.data_ultcol           dt_final,
            (vw.ton_est ) vl_producao_estimado,
            (vw.ton_mol ) vl_producao_total,
            'I'                      fg_dml
        FROM
        user_carmelita.historia vw
        LEFT JOIN (
            SELECT
                p1,
                p2,
                p3,
                p4
            FROM
                user_carmelita.tab_lq_dados
            WHERE
                codigo = 'CARTO_SOLI'
        )       tl ON tl.p1 = vw.faz
                AND tl.p2 = vw.tal
        WHERE
            vw.data_ultcol between   current_date-60 and current_date
            and vw.faz = :hacienda
            and vw.tal = :suerte
            and tl.p3 is not null
            and vw.ton_mol > 0
    """

def operacion_productividad(hacienda,suerte):
    try:
        connection = connection_db()  
        if not connection:
            raise Exception("No se pudo establecer la conexión a la base de datos.")       
        cursor = connection.cursor()
        query= query_get_productividad(hacienda,suerte)
        cursor.execute(query, {
            'hacienda':hacienda,
            'suerte':suerte
        })
        results = cursor.fetchall()
        if results == []:
            messagebox.showinfo("Información","No hay resultados de 'Productividad en la consulta realizada.")
            return
        else:
            # print("results: ", results)
            return results
    except oracledb.DatabaseError as e:
        messagebox.showerror("Error",f"Error en la base de datos en query final: {e}")
    except oracledb.InterfaceError as e:
        messagebox.showerror("Error",f"No se pudo establecer una conexión con la base de datos. Verifica la configuración de red y el cliente Oracle: {e}")
    except socket.gaierror as e:
        messagebox.showerror("Error",f"Error de red: No se pudo resolver el host {os.getenv('DB_HOST')}. Detalles: {e}")
    except Exception as e:
        messagebox.showerror("Error",f"Ocurrió un error inesperado en la obtencion de la productividad por hacienda y por suerte: {e}")
    finally:
        try:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection_db():
                connection_db().close()
        except Exception as close_error:
            messagebox.showerror("Error",f"Error al cerrar recursos: {close_error}")

def get_productividad():
    """
    propósito: data para insercion solinftec
               data base para insercion en tabla LOG_INTERFACE
    return json
    """
    from src.ui_desktop.ui import hacienda_seleccionada, suerte_seleccionada
    # operacion_productividad(hacienda_seleccionada,suerte_seleccionada)
    data = []
    for row in operacion_productividad(hacienda_seleccionada,suerte_seleccionada):
        # print("row: ", row)
        logs = get_logs_by_fields(int(row[2]),row[5])
        if logs is None:
            set_fg_dml('I')
            record = {
                "cd_unidade" : int(row[0]),
                "cd_operacao" : int(row[1]),
                "cd_ordem_servico": int(row[2]),
                "cd_fazenda": row[3],
                "cd_zona": row[4],
                "cd_talhao": row[5],
                "dt_inicial": row[6].strftime('%d/%m/%Y %H:%M:%S') if row[6] else None,
                "dt_final": (row[7] + timedelta(seconds=60)).strftime('%d/%m/%Y %H:%M:%S') if row[7] else None,
                "vl_producao_estimado": float(row[8]),
                "vl_producao_total": float(row[9]),
                "fg_dml": get_fg_dml() #row[10] #fg_dml='A' de l contrario fg_dml='I'
            }
        else:
            set_fg_dml('A')
            record = {
                "cd_unidade" : int(row[0]),
                "cd_operacao" : int(row[1]),
                "cd_ordem_servico": int(row[2]),
                "cd_fazenda": row[3],
                "cd_zona": row[4],
                "cd_talhao": row[5],
                "dt_inicial": row[6].strftime('%d/%m/%Y %H:%M:%S') if row[6] else None,
                "dt_final": (row[7] + timedelta(seconds=60)).strftime('%d/%m/%Y %H:%M:%S') if row[7] else None,
                "vl_producao_estimado": float(row[8]),
                "vl_producao_total": float(row[9]),
                "fg_dml": get_fg_dml() 
            }
        data.append(record)
    if data:
        response = {
            "identifier": "produtividade",
            "data": data
        }
        json_response = json.dumps(response, ensure_ascii=False)
        return json_response
    else:
        messagebox.showinfo("Información", "No se encontraron resultados para la consulta.")
        return None

