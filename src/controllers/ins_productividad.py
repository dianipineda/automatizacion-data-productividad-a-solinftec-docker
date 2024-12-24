from src.controllers.auth import auth_token
from src.utils.database import establish_connection
import requests
import json
from urllib3.exceptions import InsecureRequestWarning, MaxRetryError
from urllib3 import disable_warnings
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

def ins_productividad():
    try:
        auth_token()
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
                data = establish_connection(),
                headers=cabeceras, verify=False
            )
            print(f"el estado es: {res.status_code}")
            # print(f"el envio es: {res.json()}")
            res.raise_for_status()  # Este método lanza la excepción
            return {"status_code":res.status_code, "response": res.json()}
            
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
                    "Por favor, verifica tu conexión a internet y la accesibilidad del servidor."
                )
            print("Error de conexión:", mensaje)
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
        print(f"Max retries exceeded: {e}")
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
                    "Por favor, verifica tu conexión a internet y la accesibilidad del servidor."
                )
            print("Error de conexión:", mensaje)
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
        print(f"Max retries exceeded: {e}")
        return {"error": "max_retries", "details": str(e), "url": getattr(e.request, "url", "No disponible")}
        
