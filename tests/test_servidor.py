import unittest
import socket
import threading
import time
from servidor import recibir

DIRECCION = '127.0.0.1'
PUERTO = 5001

def cliente_simulado_carga(apodo, mensajes, tiempo_conexion=2):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((DIRECCION, PUERTO))

        # Recibir solicitud de apodo del servidor
        cliente.recv(2048)

        # Enviar apodo
        cliente.send(apodo.encode('utf-8'))

        # Enviar mensajes
        for mensaje in mensajes:
            cliente.send(mensaje.encode('utf-8'))
            time.sleep(0.5)  # Simula un retraso entre mensajes

        # Espera antes de desconectarse
        time.sleep(tiempo_conexion)
        cliente.close()
    except Exception as e:
        print(f"Error en cliente simulado: {e}")

class TestCargaServidor(unittest.TestCase):
    def test_carga_masiva_con_desconexion(self):
        """Prueba que el servidor maneje múltiples clientes que envían mensajes y se desconectan."""
        # Crear el socket del servidor
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((DIRECCION, PUERTO))
        s.listen()

        # Inicia el servidor en un hilo aparte
        servidor = threading.Thread(target=recibir, args=(s,), daemon=True)
        servidor.start()

        time.sleep(1)  # Espera a que el servidor esté activo

        # Crea 10 clientes simulados
        clientes = [
            threading.Thread(
                target=cliente_simulado_carga,
                args=(f"Cliente{i}", [f"Mensaje {i}-{j}" for j in range(3)], 2)
            )
            for i in range(10)
        ]

        # Inicia los clientes
        for cliente in clientes:
            cliente.start()

        # Espera a que los clientes terminen
        for cliente in clientes:
            cliente.join()

        time.sleep(2)  # Espera a que el servidor procese todos los eventos
        print("Prueba de carga con desconexión completada.")

        # Limpia el socket del servidor
        s.close()

if __name__ == "__main__":
    unittest.main()
