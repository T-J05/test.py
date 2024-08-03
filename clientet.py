import socket #Librería estándar de Python para trabajar con sockets.
import threading #para manejar multiples hilos

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
direccion = '127.0.0.1'
puerto = 5001
#conectamos al servidor
cliente.connect((direccion,puerto)) 
apodo = input('Ingrese su nombre de usuario: ')



def recibir ():
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


def escribir():
    while True:
        mensaje = f'{apodo}:{input("")}'
        cliente.send(mensaje.encode('utf-8'))



hilo_recibir = threading.Thread(target= recibir)
hilo_recibir.start()

hilo_escribir = threading.Thread(target= escribir)
hilo_escribir.start()
