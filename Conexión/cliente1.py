#import sys
import socket
import threading


TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 20



#if len(sys.argv) >= 2:
#    TCP_IP = sys.argv[1]

#if len(sys.argv) >= 3:
#    MESSAGE = sys.argv[2]


def main():

    print ("[CLIENTE] Iniciando")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print ("[CLIENTE] Conectando")
    s.connect((TCP_IP, TCP_PORT))
    print ("[CLIENTE] soy el cliente: \"" + str(s.getsockname()) + "\"")

    receive_thread = threading.Thread(target=recibirDatos,
                                args=[s],
                                daemon=True)
    
    receive_thread.start()
    enviarMensaje(s)


def enviarMensaje(s):
    continuesend = True
    while continuesend:
        msg = input("Mensaje a enviar: ")
        if msg != "":
            print ("[CLIENTE] Enviando datos: \"" + msg + "\"")
            s.send((msg + '\n').encode('utf-8'))
            continuesend = recibirDatos(s)
    
      

def recibirDatos(s):
    print ("[CLIENTE] Recibiendo datos del SERVIDOR")
    msg = ''
    fin_msg = False
    datos = bytearray()
    while not fin_msg:
        recvd = s.recv(BUFFER_SIZE)
        datos += recvd
        print ("[CLIENTE] Recibidos ", len(recvd), " bytes")
        if b'\n' in recvd:
            msg = datos.rstrip(b'\n').decode('utf-8')
            fin_msg = True
                
    print ("[CLIENTE] Recibidos en total ", len(datos), " bytes")
    print ("[CLIENTE] Datos recibidos en respuesta al CLIENTE: \"" + msg + "\"")

    if msg == "logout" or not msg:
        print ("[CLIENTE] Cerrando conexion con el SERVIDOR")
        s.close()
        print("[CLIENTE] Hasta luego.")
        return False
    return True
if __name__ == "__main__":
    main()