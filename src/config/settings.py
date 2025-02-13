import os
import sys

def resource_path(relative_path:str) -> str:
    """
    Obtiene la ruta absoluta de un recurso, adaptándose a los entornos de ejecución 
    como archivos .exe y ejecución local.

    La función determina el contexto en el que se está ejecutando el programa (si es 
    un ejecutable empaquetado o una ejecución local) y devuelve la ruta completa 
    de un archivo o recurso específico.
    """
    try:
        # Cuando se ejecuta desde un .exe
        base_path = sys._MEIPASS # type: ignore
    except AttributeError:
        # Cuando se ejecuta localmente
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)