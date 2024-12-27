import oracledb
from src.utils.coneccion_db import connection_db, configurar_cliente_oracle, parametro_ayer_formateado
# from src.ui_desktop.ui import hacienda_seleccionada

# Variables
# hacienda_seleccionada = "106" #TODO: El valor de esta variable, amarrarlo con un dropdown

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
            vw.data_ultcol BETWEEN TO_DATE(:parametro_ayer_formateado, 'DD/MM/YYYY') - 30 AND TO_DATE(:parametro_ayer_formateado, 'DD/MM/YYYY')
            AND vw.ton_mol > 0
            AND vw.faz = :hacienda
        ORDER BY
            vw.tal
    """
#TODO: Implementar validaciones de get_productividad()
def get_suertes(hacienda):
    try:
        cursor_suertes = connection_db().cursor()
        query_suertes = query_get_suertes(hacienda)
        cursor_suertes.execute(query_suertes, {
            'parametro_ayer_formateado':parametro_ayer_formateado,
            'hacienda':hacienda
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

