import socket #Librería estándar de Python para trabajar con sockets.

import threading #para manejar multiples hilos

#crear un objeto de un socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket del servidor 

#direccion y puerto
direccion = '127.0.0.1'
puerto = 5001

# enlazar a la direccion y al puerto
s.bind((direccion,puerto))

#ponemos al servidor en escucha
s.listen()
# s.setblocking(0) # 
clientes = []
apodos = []

def transmision(mensaje):  #recorremos la lista de usuarios que estan disponibles para enviar los mensajes
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

        except:
            
            break
    indice = clientes.index(cliente)
    clientes.remove(cliente)
    apodo = apodos[indice]
    apodos.remove(apodo)
    cliente.close()
    transmision(f'{apodo} ha dejado el chat!'.encode("utf-8"))
    print(f'{apodo} ha abandonado la sala del chat: ')


def recibir ():
    while True:
        cliente , direcc = s.accept()
        
        print(f'Se ha unido: {str(direcc)}')

        cliente.send('APODO'.encode('utf-8'))

        apodo = cliente.recv(2048).decode("utf-8")
        apodos.append(apodo)
        clientes.append(cliente)
        print(f'El apodo del cliente es: {apodo}')
        transmision(f'{apodo} se ha unido al chat!'.encode('utf-8'))
        cliente.send('Conectado al servidor'.encode('utf-8'))
        


        hilo = threading.Thread(target=manejar_clientes,args= (cliente,))
        hilo.start()
        
print('Servidor activo...')
recibir()






