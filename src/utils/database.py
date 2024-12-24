import oracledb
import pandas as pd
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import sys
import socket
import subprocess
import time

# Detectar si estamos empaquetados
if getattr(sys, 'frozen', False):  # Si es ejecutable empaquetado
    base_path = sys._MEIPASS
else:  # Si es un script normal
    base_path = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(base_path, '.env')
load_dotenv(dotenv_path=env_path)

# load_dotenv()

# oracle_client_path = r"/opt/oracle/instantclient_19_23"
oracle_client_path = os.getenv("ORACLE_CLIENT_PATH")

try:
    oracledb.init_oracle_client(lib_dir=oracle_client_path)
    print("Oracle Client initialized successfully.")
except Exception as e:
    print("Error initializing Oracle Client:", e)
        
#TODO: consulta a tabla log sobre existencia de orden de servicio, si existe  fg_dml='A' de l contrario fg_dml='I'
def query_get_productividad(parametro_ayer_formateado, haciendas, suertes):
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
        vw.data_ultcol between TO_DATE(:parametro_ayer_formateado,'DD/MM/YYYY')-30 and TO_DATE(:parametro_ayer_formateado,'DD/MM/YYYY')
        AND tl.p3 is not null
        AND vw.ton_mol > 0
        AND vw.faz = :faz
        AND vw.tal = :tal
    ORDER BY
        vw.faz,
        vw.tal,
        vw.data_ultcol,
        tl.p3
    """
def list_haciendas(parametro_ayer_formateado):
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
            vw.data_ultcol BETWEEN TO_DATE(:parametro_ayer_formateado, 'DD/MM/YYYY') - 30 AND TO_DATE(:parametro_ayer_formateado, 'DD/MM/YYYY')
            AND tl.p3 IS NOT NULL
            AND vw.ton_mol > 0
        ORDER BY
            vw.faz

    """
def list_suertes(parametro_ayer_formateado):
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
            vw.data_ultcol BETWEEN TO_DATE(:parametro_ayer_formateado, 'DD/MM/YYYY') - 30 AND TO_DATE(:parametro_ayer_formateado, 'DD/MM/YYYY')
            AND vw.ton_mol > 0
        ORDER BY
            vw.tal
    """
CHECK_INTERVAL = 10  # Tiempo en segundos entre verificaciones
def check_ping(host):
    try:
        # Ejecuta el comando ping
        response = subprocess.run(
            ["ping", "-n", "1", host],  # Usa "-c" en lugar de "-n" si estás en Linux
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return response.returncode == 0
    except Exception as e:
        print(f"Error ejecutando ping: {e}")
        return False

def alert_no_ping(host):
    print(f"ALERTA: No hay conexión al host {host}")

def comprobacion_ping_bbdd():
    while True:
        if not check_ping(os.getenv("DB_HOST")):
            alert_no_ping(os.getenv("DB_HOST"))
        else:
            # print(f'El host {os.getenv("DB_HOST")} es accesible.')
            return
        
def establish_connection():
    try:
        comprobacion_ping_bbdd()
        # conexion a servidor
        try:
            connection = oracledb.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                sid=os.getenv("DB_SID")
            )
            print("conexion exitosa")
        except Exception as e:
            print(f"Error al conectar: {e}")

        parametro_ayer = datetime.today() + timedelta(days=-1)
        parametro_ayer_formateado =  parametro_ayer.strftime('%d/%m/%Y')

        try:        
            print("entra a haciendas")   
            cursor_haciendas = connection.cursor()
            query_haciendas = list_haciendas(parametro_ayer_formateado)
            cursor_haciendas.execute(query_haciendas, {'parametro_ayer_formateado':parametro_ayer_formateado})
            haciendas = cursor_haciendas.fetchall()
        except oracledb.DatabaseError as e:
            print(f"Error en la base de datos en haciendas: {e}")


        try:
            print("entra a suertes")
            cursor_suertes = connection.cursor()
            query_suertes = list_suertes(parametro_ayer_formateado)
            cursor_suertes.execute(query_suertes, {'parametro_ayer_formateado':parametro_ayer_formateado})
            suertes = cursor_suertes.fetchall()
        except oracledb.DatabaseError as e:
            print(f"Error en la base de datos en suertes: {e}")

        try:
            print("entra al query general")
            cursor = connection.cursor()
            query= query_get_productividad(parametro_ayer_formateado, haciendas, suertes)
            cursor.execute(query, {
                'parametro_ayer_formateado':parametro_ayer_formateado,
                'faz':haciendas,
                'tal':suertes
            })
            #TODO: corregir el siguiente error que dispara aqui:
            #! entra al query general
            #! Error en la base de datos en query final: DPY-3002: Python value of type "tuple" is not supported
            #! Ocurrió un error inesperado: local variable 'results' referenced before assignment
            results = cursor.fetchall()
        except oracledb.DatabaseError as e:
            print(f"Error en la base de datos en query final: {e}")

        data = []
        for row in results:
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
            print("El número de resultados es: ------------->: ", len(json.loads(json_response)))
            return json_response
        #TODO: insercion de registro en tabla log de registro insertado o actualizado con sus campos ID_PROCESO, Orden de servicio y Nuevo(estado A,I)
        else:
            print("No se encontraron resultados para la consulta.")
            return None
    except oracledb.DatabaseError as e:
        print(f"Hubo un error en la conexión a la Base de Datos: {e}")
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
            if 'connection' in locals() and connection:
                connection.close()
        except Exception as close_error:
            print(f"Error al cerrar recursos: {close_error}")