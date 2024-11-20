from clientet import verificar_msj,crear_cliente, iniciar_cliente
from unittest.mock import patch, MagicMock 

def test_msj_vacio():
    mensaje = ""
    assert not verificar_msj(mensaje)
 

def test_crear_cliente_mock():  

    with patch('socket.socket') as MockSocket:
        # Creamos una instancia simulada del socket
        mock_instance = MagicMock()
        
        MockSocket.return_value = mock_instance 

        mock_instance.connect.return_value = None  # Simula una conexión exitosa
        
        direccion = '127.0.0.1'
        puerto = 5001
        cliente = crear_cliente(direccion, puerto)
        
        mock_instance.connect.assert_called_with((direccion, puerto))
        
        assert cliente is mock_instance

# def test_iniciar_cliente():
#     cliente = 