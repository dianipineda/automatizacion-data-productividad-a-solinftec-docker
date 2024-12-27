import oracledb
import json
import os
import socket
from src.utils.coneccion_db import connection_db, configurar_cliente_oracle, parametro_ayer_formateado

"""
Nota: Trayecto de la DATA:
data importada
parametro_ayer_formateado: date que viene de connecion_db.py
hacienda_seleccionada, suerte_seleccionada: str que viene de ui.py
"""

# Variables
# hacienda_seleccionada = "106" #TODO: El valor de esta variable, amarrarlo con un dropdown
# suerte_seleccionada = "14" #TODO: El valor de esta variable, debe ser un filtro del valor seleccionado en faz, amarrarlo con un dropdown

configurar_cliente_oracle()
       
#TODO: consulta a tabla log sobre existencia de orden de servicio, si existe  fg_dml='A' de l contrario fg_dml='I'
# Funciones que retornan queries
def query_get_productividad(fecha_referencia, hacienda, suerte):
    return """
    SELECT
        '1'                      cd_unidade,
        '9249'                   cd_operacao,
        TO_NUMBER(vw.faz||vw.tal||tl.p3||to_char(vw.data_ultcol,'ddmmyyyy')) cd_ordem_servico,
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
        vw.data_ultcol between TO_DATE(:fecha_referencia,'DD/MM/YYYY')-30 and TO_DATE(:fecha_referencia,'DD/MM/YYYY')
        AND tl.p3 is not null
        AND vw.ton_mol > 0
        AND vw.faz = :hacienda
        AND vw.tal = :suerte
    ORDER BY
        vw.faz,
        vw.tal,
        vw.data_ultcol,
        tl.p3
    """

def operacion_productividad(fecha_referencia,hacienda,suerte):
    try:
        cursor = connection_db().cursor()
        query= query_get_productividad(fecha_referencia,hacienda,suerte)
        print("suerte:", suerte)
        print("hacienda: ", hacienda)
        cursor.execute(query, {
            'fecha_referencia':fecha_referencia,
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
def get_productividad():
    from src.ui_desktop.ui import hacienda_seleccionada, suerte_seleccionada
    operacion_productividad(parametro_ayer_formateado,hacienda_seleccionada,suerte_seleccionada)
    data = []
    for row in operacion_productividad(parametro_ayer_formateado,hacienda_seleccionada,suerte_seleccionada):
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
            "fg_dml": row[10]
        }
        data.append(record)
    if data:
        response = {
            "identifier": "produtividade",
            "data": data
        }
        json_response = json.dumps(response, ensure_ascii=False)
        print("El número de resultados es: ------------->: ", len(json.loads(json_response)))# imprime el numero de resultados
        return json_response
    #TODO: insercion de registro en tabla log de registro insertado o actualizado con sus campos ID_PROCESO, Orden de servicio y Nuevo(estado A,I)
    else:
        print("No se encontraron resultados para la consulta.")
        return None

