import oracledb
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import sys
import subprocess
from tkinter import messagebox

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
        # print("Oracle Client initialized successfully.")
    except Exception as e:
        messagebox.showerror("Error al inicializar el cliente de Oracle:", e)

def check_server(host):
    try:
        # Intenta hacer un ping al servidor
        response = subprocess.run(
            ["ping", "-n", "1", host],  # Cambiar "-n" por "-c" en sistemas Unix
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return response.returncode == 0
    except Exception as e:
        messagebox.showerror("Error",f"Error ejecutando ping: {e}")
        return False

def connection_db():
    # conexion a servidor
    try:
        host = os.getenv("DB_HOST")
        if not check_server(host):
            messagebox.showinfo("Error:",f"El servidor '{host}' no responde. Puede estar caído o inaccesible.")
            return None
        return oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            sid=os.getenv("DB_SID")
        )
    except oracledb.DatabaseError as db_error:
        error_code, error_message = db_error.args
        messagebox.showerror("Error",f"Error de la base de datos [{error_code}]: {error_message}")
    except oracledb.InterfaceError:
        messagebox.showerror("Error","No se pudo conectar al servidor. Verifique la configuración de red o el estado del servicio.")
    except Exception as e:
        messagebox.showerror("Error",f"Error al inesperado al conectar con la Base de Datos: {e}")
