import socket
import threading

clientes = []
apodos = []

def transmision(mensaje):  
    for cliente in clientes:
        try:
            cliente.send(mensaje)
        except:
            cliente.close()
            clientes.remove(cliente)

def manejar_clientes(cliente):
    while True:
        try:
            mensaje = cliente.recv(2048)
            if not mensaje:
                break
            transmision(mensaje)
        except Exception as e:
            print(f"Error al manejar el cliente: {e}")
            break
        finally:
            if cliente in clientes:
                indice = clientes.index(cliente)
                apodo = apodos[indice]
                clientes.remove(cliente)
                apodos.remove(apodo)
                cliente.close()
                transmision(f'{apodo} ha dejado el chat!'.encode("utf-8"))
                print(f'{apodo} ha abandonado la sala del chat.')

def recibir(s):
    while True:
        cliente, direcc = s.accept()
        print(f'Se ha unido: {str(direcc)}')

        cliente.send('APODO'.encode('utf-8'))
        apodo = cliente.recv(2048).decode("utf-8")
        apodos.append(apodo)
        clientes.append(cliente)
        print(f'El apodo del cliente es: {apodo}')
        transmision(f'{apodo} se ha unido al chat!'.encode('utf-8'))
        cliente.send('Conectado al servidor'.encode('utf-8'))

        hilo = threading.Thread(target=manejar_clientes, args=(cliente,))
        hilo.start()

def iniciar_servidor(direccion='127.0.0.1', puerto=5001):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((direccion, puerto))
    s.listen()
    print('Servidor activo...')
    recibir(s)

if __name__ == "__main__":
    iniciar_servidor()
