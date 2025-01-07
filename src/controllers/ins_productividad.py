from src.controllers.auth import auth_token
from src.utils.database_productividad import get_productividad
import requests
import json
from urllib3.exceptions import InsecureRequestWarning, MaxRetryError
from urllib3 import disable_warnings
from urllib3 import disable_warnings
from tkinter import messagebox
# from src.utils.database_productividad import get_fg_dml

disable_warnings(InsecureRequestWarning)

def ins_productividad():
    try:
        # auth_token()
        cabeceras = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-Auth-Token': auth_token()
        }
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
            return {"status_code":res.status_code, "response": res.json(), "get_response":(obtener_productividad((res.json()).get('code'))).get('status')}
            
        except requests.exceptions.ConnectionError as e:
            # Interpretar el error para hacerlo más amigable
            if "Errno 11001" in str(e):
                mensaje = (
                    "No se pudo establecer conexión con el servidor debido a un problema de resolución de nombres. "
                    "Verifica si el dominio 'scdi.saas-solinftec.com' es accesible desde la red."
                )
            else:
                mensaje = (
                    "No se pudo establecer conexión con el servidor. "
                    "Por favor, verifica tu conexión a internet y la accesibilidad del servidor e intenta nuevamente."
                )
            messagebox.showerror("Error de conexión:", mensaje)
            return {"error": "connection", "details": mensaje, "url": getattr(e.request, "url", "No disponible")}

        except requests.exceptions.Timeout as e:
            return {"error": "timeout", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
        except requests.exceptions.HTTPError as e:
            return {
                "error": "http",
                "details": str(e),
                "status_code": getattr(e.response, "status_code", "No disponible")
            }
        except requests.exceptions.RequestException as e:
            return {"error": "unexpected", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
    except MaxRetryError as e:
        messagebox.showerror("Error",f"Max retries exceeded: {e}")
        return {"error": "max_retries", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
    except requests.exceptions.ConnectionError as e:
            # Interpretar el error para hacerlo más amigable
            if "Errno 11001" in str(e):
                mensaje = (
                    "No se pudo establecer conexión con el servidor debido a un problema de resolución de nombres. "
                    "Verifica si el dominio 'scdi.saas-solinftec.com' es accesible desde la red."
                )
            else:
                mensaje = (
                    "No se pudo establecer conexión con el servidor. "
                    "Por favor, verifica tu conexión a internet y la accesibilidad del servidor e intenta nuevamente."
                )
            messagebox.showerror("Error de conexión:", mensaje)
            return {"error": "connection", "details": mensaje, "url": getattr(e.request, "url", "No disponible")}
    except requests.exceptions.Timeout as e:
        return {"error": "timeout", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
    except requests.exceptions.HTTPError as e:
        return {
            "error": "http",
            "details": str(e),
            "status_code": getattr(e.response, "status_code", "No disponible")
        }
    except requests.exceptions.RequestException as e:
        return {"error": "unexpected", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
    except MaxRetryError as e:
        messagebox.showerror("Error",f"Max retries exceeded: {e}")
        return {"error": "max_retries", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
        
def obtener_productividad(codigo_envio):
    try:
        cabeceras = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'X-Auth-Token': auth_token()
        }
        try:
            res = requests.get(
                f'https://scdi.saas-solinftec.com/push_status/{codigo_envio}',
                headers=cabeceras,
                verify=False
            )
            res.raise_for_status()  # Este método lanza la excepción
            return {"get: status_code":res.status_code, "response": res.json(), "status":(res.json()).get('status')}
        except requests.exceptions.ConnectionError as e:
            # Interpretar el error para hacerlo más amigable
            if "Errno 11001" in str(e):
                mensaje = (
                    "No se pudo establecer conexión con el servidor debido a un problema de resolución de nombres. "
                    "Verifica si el dominio 'scdi.saas-solinftec.com' es accesible desde la red."
                )
            else:
                mensaje = (
                    "No se pudo establecer conexión con el servidor. "
                    "Por favor, verifica tu conexión a internet y la accesibilidad del servidor e intenta nuevamente."
                )
            messagebox.showerror("Error de conexión:", mensaje)
            return {"error": "connection", "details": mensaje, "url": getattr(e.request, "url", "No disponible")}

        except requests.exceptions.Timeout as e:
            return {"error": "timeout", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
        except requests.exceptions.HTTPError as e:
            return {
                "error": "http",
                "details": str(e),
                "status_code": getattr(e.response, "status_code", "No disponible")
            }
        except requests.exceptions.RequestException as e:
            return {"error": "unexpected", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
    except MaxRetryError as e:
        messagebox.showerror("Error",f"Max retries exceeded: {e}")
        return {"error": "max_retries", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
    except requests.exceptions.ConnectionError as e:
            # Interpretar el error para hacerlo más amigable
            if "Errno 11001" in str(e):
                mensaje = (
                    "No se pudo establecer conexión con el servidor debido a un problema de resolución de nombres. "
                    "Verifica si el dominio 'scdi.saas-solinftec.com' es accesible desde la red."
                )
            else:
                mensaje = (
                    "No se pudo establecer conexión con el servidor. "
                    "Por favor, verifica tu conexión a internet y la accesibilidad del servidor e intenta nuevamente."
                )
            messagebox.showerror("Error de conexión:", mensaje)
            return {"error": "connection", "details": mensaje, "url": getattr(e.request, "url", "No disponible")}
    except requests.exceptions.Timeout as e:
        return {"error": "timeout", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
    except requests.exceptions.HTTPError as e:
        return {
            "error": "http",
            "details": str(e),
            "status_code": getattr(e.response, "status_code", "No disponible")
        }
    except requests.exceptions.RequestException as e:
        return {"error": "unexpected", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
    except MaxRetryError as e:
        messagebox.showerror("Error",f"Max retries exceeded: {e}")
        return {"error": "max_retries", "details": str(e), "url": getattr(e.request, "url", "No disponible")}