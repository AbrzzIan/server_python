import socket
import threading

from dotenv import load_dotenv
import os
load_dotenv()

TCP_IP = '186.130.7.151'
TCP_PORT = int(os.environ.get("TCP_PORT"))
BUFFER_SIZE = 20




def main():

    #Crea el socket y se conecta
    print ("[CLIENTE] Iniciando")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print ("[CLIENTE] Conectando")
    client_socket.connect((TCP_IP, TCP_PORT))
    print ("[CLIENTE] Conectado satisfactoriamente.")

    #Crea un thread para poder recibir mensajes sin tener que mandar algo anteriormente.
    receive_thread = threading.Thread(target=recibirDatos,
                                args=[client_socket],
                                daemon=True)
    receive_thread.start()
    enviarMensaje(client_socket)

def enviarMensaje(client_socket):

    msg = ""
    while msg != "logout":
        msg = input("Mensaje a enviar: ")
        if msg != "":
            print ("[CLIENTE] Enviando datos: \"" + msg + "\"")
            #Se envía datos hasta que el mensaje sea logout.
            client_socket.send((msg + '\n').encode('utf-8'))

    print ("[CLIENTE] Cerrando conexion con el SERVIDOR")
    client_socket.close()
    print("[CLIENTE] Hasta luego.")

    


def recibirDatos(client_socket):
    while True:
        msg = ''
        fin_msg = False
        datos = bytearray()
        while not fin_msg:
            recvd = client_socket.recv(BUFFER_SIZE)
            datos += recvd
            if b'\n' in recvd:
                msg = datos.rstrip(b'\n').decode('utf-8')
                fin_msg = True

        if msg[0] == "#":
            print ("[CLIENTE] Datos recibidos: \"" + msg[1:] + "\"")
        else:
            print ("[CLIENTE] Datos recibidos: \"" + msg + "\"")

        if msg == "logout":
            break

if __name__ == "__main__":
    main()