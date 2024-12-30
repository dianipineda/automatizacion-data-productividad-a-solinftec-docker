import oracledb
import json
import os
import socket
from src.utils.coneccion_db import connection_db, configurar_cliente_oracle
from src.utils.database_log_interfaces import get_logs_by_fields, ins_logs, update_logs
from datetime import datetime

"""
Nota: Trayecto de la DATA:
data importada
hacienda_seleccionada, suerte_seleccionada: str que viene de ui.py
"""
global fg_dml
configurar_cliente_oracle()
       
# Funciones que retornan queries
def query_get_productividad(hacienda, suerte):
    return """
SELECT
        '1'                      cd_unidade,
        '9249'                   cd_operacao,
        vw.faz||substr(vw.tal,1, INSTR(vw.tal,'.', 1, 1)-1  ) || substr(vw.tal,INSTR(vw.tal,'.', 1, 1)+1,1   )||vw.safra cd_ordem_servico,
        vw.faz                   cd_fazenda,
        vw.tal                   cd_zona,
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
        vw.data_ultcol between current_date-20 and current_date
        and vw.faz = :hacienda
        and vw.tal = :suerte
        and tl.p3 is not null
        and vw.ton_mol > 0
        order BY
        vw.faz,
        vw.tal,
        vw.data_ultcol,
        tl.p3
    """

def operacion_productividad(hacienda,suerte):
    try:
        cursor = connection_db().cursor()
        query= query_get_productividad(hacienda,suerte)
        # print("suerte:", suerte)
        # print("hacienda: ", hacienda)
        cursor.execute(query, {
            'hacienda':hacienda,
            'suerte':suerte
        })
        results = cursor.fetchall()
        if results == []:
            print("No hay resultados de la consulta realizada. Consultando productividad")
            return
        else:
            return results
    except oracledb.DatabaseError as e:
        print(f"Error en la base de datos en query final: {e}")
    except oracledb.InterfaceError as e:
        print(f"No se pudo establecer una conexión con la base de datos. Verifica la configuración de red y el cliente Oracle: {e}")
    except socket.gaierror as e:
        print(f"Error de red: No se pudo resolver el host {os.getenv('DB_HOST')}. Detalles: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        try:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection_db():
                connection_db().close()
        except Exception as close_error:
            print(f"Error al cerrar recursos: {close_error}")
#TODO: la insercion y la actualizacion funcionan. Sin embargo:
# en el caso de hacienda 311 y suerte 2 me actualiza 39 registros de tal = 1, pero no deberia porque la tabla de log_interface solo hay un registro 
# depronto a lo anterior probar con buscar por hacienda, suerte y tal en lugar de los parametros anteriores
def get_productividad():
    """
    propósito: data para insercion solinftec
               data base para insercion en tabla LOG_INTERFACE
    return json
    """
    from src.ui_desktop.ui import hacienda_seleccionada, suerte_seleccionada
    operacion_productividad(hacienda_seleccionada,suerte_seleccionada)
    data = []
    for row in operacion_productividad(hacienda_seleccionada,suerte_seleccionada):
        logs = get_logs_by_fields(int(row[2]),row[5])
        if logs is None:
            fg_dml = 'I'
            record = {
                "cd_unidade" : int(row[0]),
                "cd_operacao" : int(row[1]),
                "cd_ordem_servico": int(row[2]),
                "cd_fazenda": row[3],
                "cd_zona": row[4],
                "cd_talhao": row[5],
                "dt_inicial": row[6].strftime('%d/%m/%Y %H:%M:%S') if row[6] else None,
                "dt_final": row[7].strftime('%d/%m/%Y %H:%M:%S') if row[7] else None,
                "vl_producao_estimado": float(row[8]),
                "vl_producao_total": float(row[9]),
                "fg_dml": fg_dml #row[10] #fg_dml='A' de l contrario fg_dml='I'
            }
        else:
            for item in logs:
                fg_dml = 'A'
                print("item: ",item)
                record = {
                    "cd_unidade" : int(row[0]),
                    "cd_operacao" : int(row[1]),
                    "cd_ordem_servico": int(row[2]),
                    "cd_fazenda": row[3],
                    "cd_zona": row[4],
                    "cd_talhao": row[5],
                    "dt_inicial": row[6].strftime('%d/%m/%Y %H:%M:%S') if row[6] else None,
                    "dt_final": row[7].strftime('%d/%m/%Y %H:%M:%S') if row[7] else None,
                    "vl_producao_estimado": float(row[8]),
                    "vl_producao_total": float(row[9]),
                    "fg_dml": fg_dml #row[10] #fg_dml='A' de l contrario fg_dml='I'
                }
        data.append(record)
        if fg_dml == 'I':
            ins_logs(row[2],row[3],row[4],row[5])
        if fg_dml == 'A':
            update_logs(row[2],row[3],row[4],row[5])
    if data:
        response = {
            "identifier": "produtividade",
            "data": data
        }
        json_response = json.dumps(response, ensure_ascii=False)
        decoded_response = json.loads(json_response)
        # print("El número de resultados es: ------------->: ", len(decoded_response["data"]))
        # print("El valor de los resultados es: ", json_response)
        return json_response
    else:
        print("No se encontraron resultados para la consulta.")
        return None

