import requests
import unittest
from unittest.mock import MagicMock, patch

from src.controllers.ins_productividad import ins_productividad

class TestInsProductividad(unittest.TestCase):

    #TODO: hacer una prueba con mi ip deshabilitada a internet para ver si esta excepcion se genera correctamente
    #!Nota: actualmente cuando desactivo el internet, segun la explicación de Juan Jose, lo que estoy haciendo es apagar el adaptador que me da red tanto para internet como para la red interna (lo comprobé cuando apague el internet e intente realizar ping con la maquina de Vivi, entonces el servidor biosalc con el que inicialmente hago conexion se desactiva y no me deja pasar a la siguiente parte del codigo que es entrar en las excepciones)
    @patch('requests.post')
    def test_connection_error(self, mock_post):
        # Simula un error de conexión
        mock_post.side_effect = requests.exceptions.ConnectionError("Simulado: No se pudo conectar al servidor")
        with self.assertRaises(requests.exceptions.ConnectionError):
            ins_productividad()
    #!Nota: el test de error http no funciona, sin embargo si hago una pruba manual si funciona la excepcion. Ejm probado: error 400
    @patch('requests.post')
    def test_http_error(self, mock_post):
        # Simula un error HTTP
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {'token': 'mock_token'}
        mock_response.status_code = 400
        mock_response.text = "Recurso no encontrado"
        mock_post.return_value = mock_response
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("Error 400")
        
        with self.assertRaises(requests.exceptions.HTTPError):
            ins_productividad()

    @patch('requests.post')
    def test_unexpected_error(self, mock_post):
        # Simula un error inesperado
        mock_post.side_effect = requests.exceptions.RequestException("Error inesperado")
        with self.assertRaises(requests.exceptions.RequestException):
            ins_productividad()

if __name__ == '__main__':
    unittest.main()
