import threading
import socket

TCP_IP = '127.0.0.1'  # Escucha solo conexiones locales
PUERTO = 5500
TAM_BUFFER = 20   # Para mayor velocidad de conexión

def manejar_cliente(socket_cliente, direccion_cliente):
    print(f"Conexión recibida desde {direccion_cliente}.\n")

    datos = bytearray()
    print(f"[Servidor] Esperando datos del cliente {direccion_cliente}.\n")

    try:
        mensaje = ""
        while True:
            datos_recibidos = socket_cliente.recv(TAM_BUFFER)

            if not datos_recibidos:
                print(f"[SERVIDOR] Se ha perdido la conexión con el cliente {direccion_cliente}.\n")
                break
            
            datos += datos_recibidos
            print(f"[Servidor] Recibidos {len(datos_recibidos)} bytes del cliente {direccion_cliente}.\n")
            if b'\n' in datos_recibidos:
                mensaje = datos.rstrip(b'\n').decode('utf-8')
                break
        
        # Unifico los prints en una función para mayor legibilidad
        datos_recibidos_respuesta(direccion_cliente, mensaje, datos_recibidos)
        socket_cliente.send(datos_recibidos)
        print(f"[SERVIDOR] Respuesta enviada \"{mensaje}\" al cliente {direccion_cliente} \n")
    
    except ConnectionError as error:
        print(f"[SERVIDOR] [CLIENTE] {direccion_cliente} | [ERROR] Socket error: {error}")

    finally:
        socket_cliente.close()

def datos_recibidos_respuesta(direccion_cliente, mensaje, datos_recibidos):
    print(f"[Servidor] Recibidos en total {len(datos_recibidos)} bytes del cliente {direccion_cliente}.\n")
    print(f"[SERVIDOR] Datos recibidos del cliente con éxito: \"{mensaje}\". \n")
    print(f"[Servidor] Enviando respuesta al cliente {direccion_cliente}.\n")

def main():
    print("[SERVIDOR] iniciando")
    print(f"[SERVIDOR] abriendo socket {str(PUERTO)} y escuchando en {TCP_IP}.\n")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, PUERTO))
    server_socket.listen(5) # 5 conexiones como máximo

    print(f"[SERVIDOR] Iniciando. Escuchando en {TCP_IP}:{PUERTO}")

    while 1:
        print("[SERVIDOR] Esperando conexión...")
        conn, addr = server_socket.accept()

        thread = threading.Thread(target=manejar_cliente,
                              args=[conn, addr],
                              daemon=True)
        thread.start()
        print (F"[SERVIDOR] Conexion con el cliente realizada. Direccion de conexion: {addr}")

    print (f"[SERVIDOR] Cerrando socket {str(PUERTO)}")
    server_socket.close()
    print ("[SERVIDOR] Finalizando.")


if __name__ == "__main__":
    main()
