import oracledb
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import sys
import subprocess

# Variables
# parametro_ayer = datetime.today() + timedelta(days=-1)
# parametro_ayer_formateado =  parametro_ayer.strftime('%d/%m/%Y')

# Funciones
def configurar_cliente_oracle():
    """
    Determina la ruta base del programa dependiendo de si se está ejecutando
    como un script normal o como un ejecutable empaquetado (por ejemplo, con PyInstaller).
    """
    if getattr(sys, 'frozen', False):  # Si es ejecutable empaquetado
        base_path = sys._MEIPASS
    else:  # Si es un script normal
        base_path = os.path.dirname(os.path.abspath(__file__))
    """
    Obtiene el valor de la variable de entorno ORACLE_CLIENT_PATH que se cargó desde el archivo .env
    """
    env_path = os.path.join(base_path, '.env')
    load_dotenv(dotenv_path=env_path)
    oracle_client_path = os.getenv("ORACLE_CLIENT_PATH")
    try:
        oracledb.init_oracle_client(lib_dir=oracle_client_path)
        print("Oracle Client initialized successfully.")
    except Exception as e:
        print("Error initializing Oracle Client:", e)

#TODO Funciones sobre ping (aun no usadas, TODO: probar su utilidad)
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

def connection_db():
    # conexion a servidor
    try:
        return oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            sid=os.getenv("DB_SID")
        )
    except Exception as e:
        print(f"Error al conectar: {e}")
