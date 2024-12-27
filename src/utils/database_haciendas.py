import oracledb
from src.utils.coneccion_db import connection_db, configurar_cliente_oracle, parametro_ayer_formateado

"""
Nota: Trayecto de la DATA:
data importada
parametro_ayer_formateado: date que viene de connecion_db.py
"""
configurar_cliente_oracle()
def query_get_haciendas(fecha_referencia):
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
            vw.data_ultcol BETWEEN TO_DATE(:fecha_referencia, 'DD/MM/YYYY') - 30 AND TO_DATE(:fecha_referencia, 'DD/MM/YYYY')
            AND tl.p3 IS NOT NULL
            AND vw.ton_mol > 0
        ORDER BY
            vw.faz

    """
#TODO: Implementar validaciones de get_productividad()
def get_haciendas():
    try:         
        cursor_haciendas = connection_db().cursor()
        query_haciendas = query_get_haciendas(parametro_ayer_formateado)
        cursor_haciendas.execute(
            query_haciendas,
            {'fecha_referencia':parametro_ayer_formateado}
        )
        haciendas = cursor_haciendas.fetchall()
        return haciendas
    except oracledb.DatabaseError as e:
        print(f"Error en la base de datos en haciendas: {e}")