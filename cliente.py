import sys
import socket

TCP_IP = '127.0.0.1'
PUERTO = 5500
BUFFER_SIZE = 20
MESSAGE = "Hola Server!"

# Ambos if referencian una entrada en la llamada al archivo pudiendo sobreescribir las constantes python cliente.py TCP_IP MENSSAGE
if len(sys.argv) >= 2:
    TCP_IP = sys.argv[1]

if len(sys.argv) >= 3:
    MESSAGE = sys.argv[2]


print ("[CLIENTE] Iniciando")
# Creamos el socket del cliente
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print ("[CLIENTE] Conectando")
# Creamos la conexión al server
socket_cliente.connect((TCP_IP, PUERTO))

print (f"[CLIENTE] soy el cliente: \"{str(socket_cliente.getsockname())}\"")
print ("[CLIENTE] Enviando datos: \"" + MESSAGE + "\"")

# Envío de datos al server
socket_cliente.send((MESSAGE + '\n').encode('utf-8'))
print ("[CLIENTE] Recibiendo datos del SERVIDOR")
msg = ''
fin_msg = False
datos = bytearray()

# Recibiendo datos del server
while not fin_msg:
	recvd = socket_cliente.recv(BUFFER_SIZE)
	datos += recvd
	print ("[CLIENTE] Recibidos ", len(recvd), " bytes")
	if b'\n' in recvd:
		msg = datos.rstrip(b'\n').decode('utf-8')
		fin_msg = True
            
print ("[CLIENTE] Recibidos en total ", len(datos), " bytes")
print ("[CLIENTE] Dados recibidos en respuesta al CLIENTE: \"" + msg + "\"")
print ("[CLIENTE] Cerrando conexion con el CLIENTE")

# Cierre de socket del cliente
socket_cliente.close()

print ("[CLIENTE] Finalizado.")