import socket
import threading


def crear_cliente(direccion='127.0.0.1', puerto=5001):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((direccion, puerto))
    return cliente


def verificar_msj(mensaje):
    mensaje = mensaje.strip()
    return bool(mensaje)
    
def verificar_apodo(apodo):
    
    apodo = apodo.strip()
    if len(apodo) < 3 or len(apodo) > 20:
            return False
    return True


def recibir(cliente, apodo):
    while True:
        try:
            mensaje = cliente.recv(2048).decode('utf-8')
            if mensaje == 'APODO':
                cliente.send(apodo.encode('utf-8'))
            else:
                print(mensaje)
        except socket.error as e:
            print(f'Se ha producido un error en la conexión: {e}')
            cliente.close()
            break
        except Exception as e:
            print(f'Se ha producido un error inesperado: {e}')
            cliente.close()
            break


def escribir(cliente, apodo):
    while True:
        try:
            msj = f"{input("")}"
            mensaje = f'{apodo}:{msj} '
            if verificar_msj(msj):
                cliente.send(mensaje.encode('utf-8'))
            else:
                print("\033[31mError mensaje vacio\033[0m")
                continue
        except Exception as e:
            print(f"\033[31mError de: {e}\033[0m")


def imput():
    apodo = ""
    while not verificar_apodo(apodo):
        apodo = input('Ingrese su nombre de usuario: ')
        print(apodo)
        if verificar_apodo(apodo):
            return apodo
        if not verificar_apodo(apodo):
            print("\033[31m⚠️  El apodo no puede estar vacío, y debe ser de min 3 letras y max 10. Intenta nuevamente.\033[0m")
         
            
def iniciar_cliente(cliente,apodo):
    try:
        
        if apodo:
            hilo_recibir = threading.Thread(target=recibir, args=(cliente, apodo))
            hilo_recibir.start()

            hilo_escribir = threading.Thread(target=escribir, args=(cliente, apodo))
            hilo_escribir.start()
    except Exception as e:
        return (f"Error iniciando al cliente: {str(e)}")

    
    
if __name__ == "__main__":
    cliente = crear_cliente()
    apodoi = imput()
    iniciar_cliente(cliente,apodoi)
