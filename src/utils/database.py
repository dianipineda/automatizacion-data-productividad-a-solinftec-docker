import oracledb
import pandas as pd
import json
from datetime import datetime, timedelta

oracle_client_path = r"/opt/oracle/instantclient_19_23"

try:
    oracledb.init_oracle_client(lib_dir=oracle_client_path)
    print("Oracle Client initialized successfully.")
except Exception as e:
    print("Error initializing Oracle Client:", e)

def establish_connection():
    try:
        # credenciales servidor de produccion
        connection = oracledb.connect(user="SOLINFTEC", password="S0L1NFT3CAgr125*",host='192.168.10.6', port=1521, sid="dbbiosalc")

        cursor = connection.cursor()
        parametro_ayer = datetime.today() + timedelta(days=-1)
        parametro_ayer_formateado =  parametro_ayer.strftime('%d/%m/%Y')
        # parametro_ayer_formateado = '01/11/2024'
        # vw.liberacion            cd_orden_servico,
        #TODO: consulta a tabla log sobre existencia de orden de servicio, si existe  fg_dml='A' de l contrario fg_dml='I'
        query= """
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
            vw.data_ultcol between TO_DATE(:parametro_ayer_formateado,'DD/MM/YYYY')-15 and TO_DATE(:parametro_ayer_formateado,'DD/MM/YYYY')
            and tl.p3 is not null
            and vw.ton_mol > 0
            order BY
            vw.faz,
            vw.tal,
            vw.data_ultcol,
            tl.p3
        """
        cursor.execute(query, {'parametro_ayer_formateado':parametro_ayer_formateado})
        results = cursor.fetchall()
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
        # respuesta:
        if data:
            response = {
                "identifier": "produtividade",
                "data": data
            }
            print("data: ")
            print(data)
            print("-----------------------------")
            # conversion de respuesta a json
            json_response = json.dumps(response, ensure_ascii=False)
            # print(f"json es : {json_response}")
            return json_response
        #TODO: insercion de registro en tabla log de registro insertado o actualizado con sus campos ID_PROCESO, Orden de servicio y Nuevo(estado A,I)
        else:
            print("No se encontraron resultados para la consulta.")
            return None
    except oracledb.DatabaseError as e:
        print(f" Hubo un error en la conexion a la Base de Datos: {e}")
    finally:
        cursor.close()
        connection.close()