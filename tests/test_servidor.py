import unittest
import socket
import threading
import time
from servidor import recibir

DIRECCION = '127.0.0.1'
PUERTO = 5001

def cliente_simulado(apodo, mensajes, tiempo_conexion=2):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((DIRECCION, PUERTO))

        cliente.recv(2048)

        cliente.send(apodo.encode('utf-8'))

        for mensaje in mensajes:
            cliente.send(mensaje.encode('utf-8'))
            time.sleep(0.5)  
            
        time.sleep(tiempo_conexion)
        cliente.close()
    except Exception as e:
        print(f"Error en cliente simulado: {e}")


class TestCargaServidor(unittest.TestCase):
    def test_carga_masiva_con_desconexion(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((DIRECCION, PUERTO))
        s.listen()
        
        servidor = threading.Thread(target=recibir, args=(s,), daemon=True)
        servidor.start()

        time.sleep(1) 
        clientes = [
            threading.Thread(
                target=cliente_simulado,
                args=(f"Cliente{i}", [f"Mensaje {i}-{j}" for j in range(3)])
            )
            for i in range(10)
        ]

        for cliente in clientes:
            cliente.start()

        for cliente in clientes:
            cliente.join()

        print("Prueba de carga con desconexión completada.")

        s.close()

if __name__ == "__main__":
    unittest.main()
