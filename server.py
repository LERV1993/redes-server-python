import socket
import threading
import sys

# Definimos el tamaño del buffer y las variables globales
TAM_BUFFER = 200  # Lo dejo en 200 para poder aceptar masomenos 150 caracteres
TCP_IP = '127.0.0.1'  # Puedes cambiar la IP por la que necesites
PUERTO = 5000 # Puerto donde funciona el server
clientes = [] # Lista de cliente

# Función para manejar cliente recibe el socket y la dirección de cliente
def manejar_cliente(socket_cliente, direccion_cliente):

    global clientes # Tengo que declararle en el scope la variable global porque es re mamasa python
    datos = bytearray() # Array de bytes para evaluar la recepción de datos y decodificar el mesaje y reenviarlo, tambien lo use para depurar y ver que llegue info

    # Lo encerramos en un try except por cualquier proble de conexión que pueda haber con el cliente o desconexión del mismo
    try:

        # Instanciamos un bucle while para dejar recibiendo mensajes
        while True:

            # Guardamos en una variable los datos recibidos 
            datos_recibidos = socket_cliente.recv(TAM_BUFFER)

            # Levantamos cualquier problema con la recepción de datos y salimos del bucle con break
            if not datos_recibidos:

                # Informamos por pantalla el error y la dirección del cliente al que corresponde
                print(f"[SERVIDOR] Se ha perdido la conexión con el cliente {direccion_cliente}.\n")
                break

            datos += datos_recibidos # Guardo los datos recibidos en el array mutable de bytes
            #print(f"[SERVIDOR] Recibidos {len(datos_recibidos)} bytes del cliente {direccion_cliente}.\n")
            # El print de arriba para verificar que lleguen bytes

            # Evaluo que lleguen datos
            if datos_recibidos:

                # Decodifico el mensaje para salvar acentos y caracteres especiales
                mensaje = datos.decode('utf-8')
                datos = bytearray() # Depuración y para reiniciar el buffer para el próximo mensaje

                #print(repr(mensaje), str(mensaje in "#LOGOUT"))  // Depuración estaba enviando el nick y estaba intentando evaluar mensaje == #LOGOUT

                # Si dentro del mensaje llega un #LOGOUT cierra la conexión
                if "#LOGOUT" in mensaje:

                    # Informa por pantalla la dirección del  cliente que se desconectará y luego usa break para terminar el bucle
                    print(f"[SERVIDOR] El cliente {direccion_cliente} se ha desconectado.\n")
                    break

                # Reenviar el mensaje a todos los clientes conectados
                for cliente in clientes:

                    # Reenvia a todos los clientes menos al que realiza el envío del mensaje
                    if cliente != socket_cliente:
                        
                        # Utilizamos un try except para levantar cualquier posible desconexión de algún usuario en el momento del reenvío del mensaje
                        try:
                            cliente.send(mensaje.encode('utf-8') + b'\n')
                        except Exception as e:
                            # getpeername() para ver el ip y el puerto que esta fallando en caso de que no se reenvie algun mensaje
                            print(f"[SERVIDOR] No se pudo enviar el mensaje a {cliente.getpeername()}: {e}")

    # Levanto las excepciones de conexión por cualquier interrupción que se pueda dar.
    except ConnectionError as error:
        print(f"[SERVIDOR] [CLIENTE] {direccion_cliente} | [ERROR] Socket error: {error}")

    # Fuera del bucle cuando se ejecuta alguna excepción cierro el socket del cliente y lo elimino de la lista para no reenviarle mensajes.
    finally:
        # Cierro el socket del cliente
        socket_cliente.close()

        # Borro de la lista de clientes el socket cerrado
        if socket_cliente in clientes:
            clientes.remove(socket_cliente)

        # Muestro por pantalla las acciones realizadas.
        print(f"[SERVIDOR] Cliente {direccion_cliente} desconectado y eliminado de la lista.\n")

# Función principal
def main():

    global clientes # Tengo que declarar nuevamente la varialbe cliente como global sino no me deja acceder 

    # Muestro por pantalla la información del IP y el puerto donde inicia la sala de chat
    print("[SALA] Iniciando")
    print(f"[SALA] Abriendo socket en el puerto {PUERTO} y escuchando en {TCP_IP}.\n")

    # Creo el socket declarando la familia y el tipo de conexión
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Encierro en un try except el bind por cualquier problema de puertos, es decir, que el puerto este ocupado.
    try:

        # Hago el bind del socket con el ip y el puerto y lo dejo escuchando
        server_socket.bind((TCP_IP, PUERTO))
        server_socket.listen(10)  # 10 conexiones como máximo

        # Muestro por pantalla que la sala inicio
        print(f"[SALA] Iniciando. Escuchando en {TCP_IP}:{PUERTO}")

        # Instancio un bucle para esperar nueva conexiones
        while True:

            # Muestro por pantalla la espera de conexiones
            print("[SALA] Esperando nueva conexión...")

            # Cuando se acepta una conexión guardo en dos variables el socket y el addres del cliente
            socket_cliente, addr = server_socket.accept()

            # Guardo el soccket del cliente en la lista de clientes para poder reutilizarlos
            clientes.append(socket_cliente)

            # Creo el hilo con la función de manejar cliente en daemon true para que en caso de que finalice el programa estos se cierren
            thread = threading.Thread(target=manejar_cliente, args=(socket_cliente, addr), daemon=True)

            # Inicializo el hilo con el socket del cliente que se conecto
            thread.start()

            # Muestro por pantalla el exito de la conexión y el address del usuario
            print(f"[SERVIDOR] Conexión con el cliente realizada. Dirección de conexión: {addr}")

    # Si cuando intento hacer el bind el puerto no está disponible muestro por pantalla el error y cierro el programa
    except socket.error as e:
        print(f"[SERVIDOR] El puerto no se encuentra disponible: {e}\n")
        sys.exit()

    # Por último cierro el socket del server y muestro por pantalla el puerto
    finally:
        server_socket.close()
        print(f"[SERVIDOR] Cerrando socket {PUERTO}")
        print("[SERVIDOR] Finalizando.")

# Se utiliza para verificar si el script está siendo ejecutado directamente.
# Si la condición es verdadera, el código dentro de este bloque se ejecutará. 
# Si el script está siendo importado, el código dentro de este bloque no se ejecutará.
if __name__ == "__main__":
    main()
