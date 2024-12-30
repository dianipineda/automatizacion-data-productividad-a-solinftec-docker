import oracledb
from src.utils.coneccion_db import connection_db, configurar_cliente_oracle

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
            vw.data_ultcol between current_date-20 AND current_date
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
        # print("query_suertes: ", query_suertes)
        cursor_suertes.execute(query_suertes, {
            'hacienda':hacienda
        })
        suertes = cursor_suertes.fetchall()
        if suertes == []:
            print("No hay resultados de la consulta realizada. Consultando suertes")
            return
        else:
            return suertes
    except oracledb.DatabaseError as e:
        print(f"Error en la base de datos en suertes: {e}")

