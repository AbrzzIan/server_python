import threading
import socket

TCP_IP = ''
TCP_PORT = 12345
BUFFER_SIZE = 20  # default 1024 a menor mas velocidad


def cerrarConexion():
    print ("[SERVIDOR] Cerrando socket " + str(TCP_PORT))
    s.close()
    print ("[SERVIDOR] fin_msg")
    return 0

def atiende_cliente(conn, addr):
    while 1:
        msg = ''
        datos = bytearray()
        print ("[SERVIDOR ", addr, "] Esperando datos del cliente")
        fin_msg = False
        try:
            while not fin_msg:
                recvd = conn.recv(BUFFER_SIZE)
                if not recvd:
                    break
                    #raise ConnectionError()
                datos += recvd
                print ("[SERVIDOR ", addr, "] Recibidos ", len(recvd), " bytes")
                if b'\n' in recvd:
                    msg = datos.rstrip(b'\n').decode('utf-8')
                    fin_msg = True
            print ("[SERVIDOR ", addr, "] Recibidos en total ", len(datos), " bytes")
            print ("[SERVIDOR ", addr, "] Datos recibidos del cliente con exito: \"" + msg + "\"")

            print ("[SERVIDOR ", addr, "] Enviando respuesta para el cliente")
            if msg[0] == "#":
                for conn in conn_list:
                    conn.send(datos)  # echo
            else:
                conn.send(datos)

            print ("[SERVIDOR ", addr, "] Respuesta enviada: \"" + msg + "\"")
            if msg=="logout":
                print ("[SERVIDOR ", addr, "] Cliente desconectado")
                i = input("cerrar conexión? (S)")
                if i == "S":
                    cerrarConexion()
                return 0


        except BaseException as error:
            print ("[SERVIDOR ", addr, "] [ERROR] Socket error: ", error)
            break


print ("[SERVIDOR] Iniciando")

print ("[SERVIDOR] Abriendo socket " + str(TCP_PORT) + " y escuchando")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.close()
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn_list = []

while 1:
    print ("[SERVIDOR] Esperando conexion")
    conn, addr = s.accept()
    conn_list.append(conn)
    thread = threading.Thread(target=atiende_cliente,
                              args=[conn, addr],
                              daemon=True)
    thread.start()
    print ("[SERVIDOR ", addr, "] Conexion con el cliente realizada. Direccion de conexion:", addr)
    print("[SERVIDOR ", addr, "] Conectados:", threading.active_count() - 1)

