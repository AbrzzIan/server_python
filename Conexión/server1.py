import threading
import socket

TCP_IP = ''
TCP_PORT = 5664
BUFFER_SIZE = 20  # default 1024 a menor mas velocidad



## redirgir el puerto 5666 a la ip priv donde estes corriendo el server


conn_list = []

def main():

    print ("[SERVIDOR] Iniciando")
    print ("[SERVIDOR] Abriendo socket " + str(TCP_PORT) + " y escuchando")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.close()
    server_socket.bind((TCP_IP, TCP_PORT))
    server_socket.listen(5)
    

    try:
        while True:
            print ("[SERVIDOR] Esperando conexion")
            client_connection, addr = server_socket.accept()

            #Agrega la conexion del cliente al array de conexiones
            conn_list.append(client_connection)
            client_thread = threading.Thread(target=atiende_cliente,
                                    args=[client_connection, addr],
                                    daemon=True)
            client_thread.start()

            print ("[SERVIDOR ", addr, "] Conexion con el cliente realizada. Direccion de conexion:", addr)
            print("[SERVIDOR ", addr, "] Conectados:", len(conn_list))

    except KeyboardInterrupt:
        server_socket.close()





def cerrarConexion(client_connection):
    print ("[SERVIDOR] Desconectando cliente...")
    client_connection.close()
    conn_list.remove(client_connection)
    print ("[SERVIDOR] Cliente desconectado.")


def atiende_cliente(client_connection, addr):
    while 1:
        msg = ''
        datos = bytearray()
        print ("[SERVIDOR ", addr, "] Esperando datos del cliente")
        fin_msg = False
        try:
            while not fin_msg:
                recvd = client_connection.recv(BUFFER_SIZE)
                if not recvd:
                    break
                datos += recvd
                if b'\n' in recvd:
                    msg = datos.rstrip(b'\n').decode('utf-8')
                    fin_msg = True
            print ("[SERVIDOR ", addr, "] Datos recibidos del cliente: \"" + msg + "\"")
            #Si el primer caracter del mensaje es # hace un send a todos los clientes conectados.
            if msg[0] == "#":
                for client_connection in conn_list:
                    client_connection.send(datos)  # echo
            else:
                client_connection.send(datos)
            print ("[SERVIDOR ", addr, "] Respuesta enviada: \"" + msg + "\"")
            if msg=="logout":
                cerrarConexion(client_connection)
                return 0
        except BaseException as error:
            print ("[SERVIDOR ", addr, "] [ERROR] Socket error: ", error)
            break


if __name__ == "__main__":
    main()
    

