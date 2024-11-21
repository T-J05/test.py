from clientet import verificar_msj,crear_cliente, iniciar_cliente,imput
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


def test_imput():
    entradas =["", "ab","","usuario_valido"]
    with patch('builtins.input', side_effect=entradas):
        apodo = imput()
        assert apodo == "usuario_valido"


def cliente_generado():
        with patch('socket.socket') as MockSocket:
            # Creamos una instancia simulada del socket
            mock_instance = MagicMock()
            
            MockSocket.return_value = mock_instance 

            mock_instance.connect.return_value = None  # Simula una conexión exitosa
            
            direccion = '127.0.0.1'
            puerto = 5001
            cliente = crear_cliente(direccion, puerto)
            return cliente
        
        
def test_iniciar_cliente_con_hilos_mockeados():
    with patch('threading.Thread') as MockThread:
        
        mock_thread = MagicMock()
        MockThread.return_value = mock_thread  # Hacemos que Thread devuelva nuestro mock

        cliente = cliente_generado()
        apodo = 'usuario_test'


        iniciar_cliente(cliente, apodo)

        mock_thread.start.assert_called()
