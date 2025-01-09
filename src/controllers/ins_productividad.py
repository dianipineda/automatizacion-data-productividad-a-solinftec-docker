from src.controllers.auth import auth_token
from src.utils.database_productividad import get_productividad, del_productividad
import requests
import json
from urllib3.exceptions import InsecureRequestWarning, MaxRetryError
from urllib3 import disable_warnings
from urllib3 import disable_warnings
from tkinter import messagebox
# from src.utils.database_productividad import get_fg_dml

disable_warnings(InsecureRequestWarning)

def handle_request_error(error, url=None):
    """Maneja los errores de solicitudes."""
    if isinstance(error, MaxRetryError):
        mensaje = "Max retries exceeded"
        return {
            "error": "max_retries",
            "details": str(error),
            "url": url or "No disponible"
        }
    elif isinstance(error, requests.exceptions.ConnectionError):
        mensaje = (
            "No se pudo establecer conexión con el servidor. "
            "Por favor, verifica tu conexión a internet y la accesibilidad del servidor."
        )
        return {
            "error": "connection",
            "details": mensaje,
            "url": url or "No disponible"
        }
    elif isinstance(error, requests.exceptions.Timeout):
        return {
            "error": "timeout",
            "details": str(error),
            "url": url or "No disponible"
        }
    elif isinstance(error, requests.exceptions.HTTPError):
        return {
            "error": "http",
            "details": str(error),
            "status_code": getattr(error.response, "status_code", "No disponible"),
            "url": url or "No disponible"
        }
    else:
        return {
            "error": "unexpected",
            "details": str(error),
            "url": url or "No disponible"
        }

def get_headers():
    return {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'X-Auth-Token': auth_token()
    }

def ins_productividad():
    try:
        # auth_token()
        cabeceras = get_headers()
        try:
            res =  requests.post(
                'https://scdi.saas-solinftec.com/push', 
                data = get_productividad(),
                headers=cabeceras, verify=False
            )
            # print(f"el estado es: {res.status_code}")
            # print(f"el envio es: {res.json()}")
            # print(f"codigo: {(res.json()).get('code')}")
            #? Si el estado es 200 entonces que ejecute la funcion get_productividad
            res.raise_for_status()  # Este método lanza la excepción
            obtener_productividad((res.json()).get('code'))
            return {
                "status_code":res.status_code,
                "response": res.json(),
                "get_response":(obtener_productividad((res.json()).get('code'))).get('status'),
                "data": get_productividad()
            }
        except (requests.exceptions.RequestException, MaxRetryError) as e:
            return handle_request_error(e, getattr(e.request, "url", "No disponible"))
    except (requests.exceptions.RequestException, MaxRetryError) as e:
       return handle_request_error(e, getattr(e.request, "url", "No disponible"))
        
def obtener_productividad(codigo_envio):
    try:
        cabeceras = get_headers()
        try:
            res = requests.get(
                f'https://scdi.saas-solinftec.com/push_status/{codigo_envio}',
                headers=cabeceras,
                verify=False
            )
            res.raise_for_status()  # Este método lanza la excepción
            return {"get: status_code":res.status_code, "response": res.json(), "status":(res.json()).get('status')}
        except (requests.exceptions.RequestException, MaxRetryError) as e:
            return handle_request_error(e, getattr(e.request, "url", "No disponible"))
    except (requests.exceptions.RequestException, MaxRetryError) as e:
       return handle_request_error(e, getattr(e.request, "url", "No disponible"))
    
def delete_productividad():
    try:
        # auth_token()
        cabeceras = get_headers()
        try:
            res =  requests.post(
                'https://scdi.saas-solinftec.com/push', 
                data = del_productividad(),
                headers=cabeceras, verify=False
            )
            #? Si el estado es 200 entonces que ejecute la funcion get_productividad
            res.raise_for_status()  # Este método lanza la excepción
            obtener_productividad((res.json()).get('code'))
            return {
                "status_code":res.status_code,
                "response": res.json(),
                "get_response":(obtener_productividad((res.json()).get('code'))).get('status'),
                "data": del_productividad()
            }
        except (requests.exceptions.RequestException, MaxRetryError) as e:
            return handle_request_error(e, getattr(e.request, "url", "No disponible"))
    except (requests.exceptions.RequestException, MaxRetryError) as e:
       return handle_request_error(e, getattr(e.request, "url", "No disponible"))