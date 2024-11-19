import socket
import threading


def crear_cliente(direccion='127.0.0.1', puerto=5001):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((direccion, puerto))
    return cliente


def verificar_msj(mensaje):
    if mensaje == "":
        return False
    else:
        return True


def recibir(cliente, apodo):
    while True:
        try:
            mensaje = cliente.recv(2048).decode('utf-8')
            if mensaje == 'APODO':
                cliente.send(apodo.encode('utf-8'))
            else:
                print(mensaje)
        except Exception as e:
            print(f'Se ha producido un error: {e}')
            cliente.close()
            break


def escribir(cliente, apodo):
    while True:
        try:
            mensaje = f'{apodo}: {input("")}'
            if verificar_msj(mensaje):
                cliente.send(mensaje.encode('utf-8'))
            else:
                print("\033[31mError mensaje vacio\033[0m")
                continue
        except Exception as e:
            print(f"\033[31mError de: {e}\033[0m")


def iniciar_cliente():
    cliente = crear_cliente()
    apodo = ""
    
    while not verificar_msj(apodo):
        apodo = input('Ingrese su nombre de usuario: ')
        if not apodo:
            print("\033[31m⚠️  El apodo no puede estar vacío. Intenta nuevamente.\033[0m")
            
    hilo_recibir = threading.Thread(target=recibir, args=(cliente, apodo))
    hilo_recibir.start()

    hilo_escribir = threading.Thread(target=escribir, args=(cliente, apodo))
    hilo_escribir.start()

    


if __name__ == "__main__":
    iniciar_cliente()
