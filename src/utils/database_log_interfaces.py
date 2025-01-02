import oracledb
import json
import os
import socket
from src.utils.coneccion_db import connection_db, configurar_cliente_oracle
from tkinter import messagebox

configurar_cliente_oracle()

def query_get_logs_by_fields(ordem_servico,tal):
    return """
    SELECT
        vw.proceso             proceso_log,
        vw.clave1              ordem_servico,
        vw.clave4              tal
    FROM
    user_carmelita.LOG_INTERFACE vw
    WHERE
        vw.proceso = 'PROD_SLTIF'
        and vw.clave1 = :ordem_servico
        and vw.clave4 = :tal
    """
def get_logs_by_fields(ordem_servico, tal):
    try:
        connection = connection_db()  
        if not connection:
            raise Exception("No se pudo establecer la conexión a la base de datos.")       
        cursor = connection.cursor() 
        if not connection:
            raise Exception("No se pudo establecer la conexión a la base de datos.")       
        cursor = connection.cursor()
        query= query_get_logs_by_fields(ordem_servico,tal)
        cursor.execute(query, {
            'ordem_servico':ordem_servico,
            'tal':tal
        })
        results = cursor.fetchall()
        # print("results: ", results)
        if results == []:
            messagebox.showinfo("No hay resultados de 'Logs' en la consulta realizada.")
            return
        else:
            return results
    except oracledb.DatabaseError as e:
        messagebox.showerror("Error",f"Error en la base de datos en query final: {e}")
    except oracledb.InterfaceError as e:
        messagebox.showerror("Error",f"No se pudo establecer una conexión con la base de datos. Verifica la configuración de red y el cliente Oracle: {e}")
    except socket.gaierror as e:
        messagebox.showerror("Error",f"Error de red: No se pudo resolver el host {os.getenv('DB_HOST')}. Detalles: {e}")
    except Exception as e:
        messagebox.showerror("Error",f"Ocurrió un error inesperado: {e}")
    finally:
        try:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection_db():
                connection_db().close()
        except Exception as close_error:
            messagebox.showerror("Error",f"Error al cerrar recursos: {close_error}")

# ver en que parte del codigo se llamara esta funcion
def query_ins_logs(secuencia):
    return """
    INSERT INTO USER_CARMELITA.LOG_INTERFACE (PLANTA,PROCESO,SECUENCIA,FECHA,CLAVE1,CLAVE2,CLAVE3,CLAVE4,CLAVE5)
    VALUES ('00050001','PROD_SLTIF',:secuencia,sysdate,:ordem_servico,:fazenda,:zona,:tal,TO_CHAR(SYSDATE, 'YYMMDDHH24MI'))
    """
def get_next_sequence():
    connection = None
    cursor = None
    try:
        connection = connection_db()  
        if not connection:
            raise Exception("No se pudo establecer la conexión a la base de datos.")       
        cursor = connection.cursor()
        
        # Consulta para obtener el valor máximo de SECUENCIA para el PROCESO específico
        cursor.execute("""
        SELECT NVL(MAX(SECUENCIA), 0) AS MAX_SECUENCIA
        FROM USER_CARMELITA.LOG_INTERFACE
        WHERE PROCESO = 'PROD_SLTIF'
        """)
        
        max_secuencia = cursor.fetchone()[0]
        return max_secuencia + 1
    except oracledb.DatabaseError as e:
        messagebox.showerror("Error",f"Error en la base de datos en haciendas: {e}")
    except oracledb.InterfaceError as e:
        messagebox.showerror("Error",f"No se pudo establecer una conexión con la base de datos. Verifica la configuración de red y el cliente Oracle: {e}")
    except socket.gaierror as e:
        messagebox.showerror("Error",f"Error de red: No se pudo resolver el host {os.getenv('DB_HOST')}. Detalles: {e}")
    except Exception as e:
        messagebox.showerror("Error",f"Ocurrió un error inesperado: {e}")
    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except Exception as close_error:
            messagebox.showerror("Error",f"Error al cerrar recursos: {close_error}")

def ins_logs(ordem_servico, fazenda, zona,tal):
    connection = None 
    cursor = None
    try:
        connection = connection_db()  
        if not connection:
            raise Exception("No se pudo establecer la conexión a la base de datos.")       
        cursor = connection.cursor()
        next_secuencia = get_next_sequence()
        query= query_ins_logs(next_secuencia)
        cursor.execute(query, {
            'ordem_servico':ordem_servico,
            'fazenda':fazenda,
            'zona':zona,
            'tal':tal,
            'secuencia':next_secuencia
        })
        connection.commit()
    except oracledb.DatabaseError as e:
        messagebox.showerror("Error",f"Error en la base de datos en haciendas: {e}")
    except oracledb.InterfaceError as e:
        messagebox.showerror("Error",f"No se pudo establecer una conexión con la base de datos. Verifica la configuración de red y el cliente Oracle: {e}")
    except socket.gaierror as e:
        messagebox.showerror("Error",f"Error de red: No se pudo resolver el host {os.getenv('DB_HOST')}. Detalles: {e}")
    except Exception as e:
        messagebox.showerror("Error",f"Ocurrió un error inesperado: {e}")

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except Exception as close_error:
            messagebox.showerror("Error",f"Error al cerrar recursos: {close_error}")

def query_update_logs():
    return """
    UPDATE USER_CARMELITA.LOG_INTERFACE
    SET CLAVE1 = :ordem_servico,
        CLAVE5 = TO_CHAR(SYSDATE, 'YYMMDDHH24MI')
    WHERE CLAVE1 = :ordem_servico
    """
def update_logs(ordem_servico):
    connection = None
    cursor = None
    try:
        connection = connection_db()  
        if not connection:
            raise Exception("No se pudo establecer la conexión a la base de datos.")       
        cursor = connection.cursor()
        query= query_update_logs()
        cursor.execute(query, {
            'ordem_servico':ordem_servico
        })
        connection.commit()
    except oracledb.DatabaseError as e:
        messagebox.showerror("Error",f"Error en la base de datos en haciendas: {e}")
    except oracledb.InterfaceError as e:
        messagebox.showerror("Error",f"No se pudo establecer una conexión con la base de datos. Verifica la configuración de red y el cliente Oracle: {e}")
    except socket.gaierror as e:
        messagebox.showerror("Error",f"Error de red: No se pudo resolver el host {os.getenv('DB_HOST')}. Detalles: {e}")
    except Exception as e:
        messagebox.showerror("Error",f"Ocurrió un error inesperado: {e}")

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except Exception as close_error:
            messagebox.showerror("Error",f"Error al cerrar recursos: {close_error}")