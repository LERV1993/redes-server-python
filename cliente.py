import sys
import socket
import threading

TCP_IP = '127.0.0.1'  # Para que quede en localhost y evitar ingresos o tipeados erróneos
PUERTO = '' # Lo define el usuario por input
BUFFER_SIZE = 200  # Aproximadamente 150 caracteres por si hay algún carácter especial que rompa todo en el programa lo limitamos a 150 pero le damos un margen extra
NAME = '' # El nick visible

# Ingreso manual de puerto
while not PUERTO:
    
	# Mostramos por pantalla lo que debe realizar el usuario ....
    print('[CONFIG] Para salir escriba "salir". \n')
    print('[CONFIG] Ingrese el puerto que desea utilizar (entre 0 y 5500): \n')
    input_user = input()

	# Lower por si lo escribe sin querer con una mayúscula
    # Cierra el programa y le avisamos por pantalla
    if input_user.lower() == 'salir':
        print('[CONFIG] Programa finalizado.')
        sys.exit()

	# Para evitar usar regex lo evaluamos pasandolo a int si hay un valor no numerico saldra en el ValueError y lo levantamos por ahí
    try:
        PUERTO = int(input_user)
        
        # Se deben respetar los valores detallados al inicios del programa en cuanto a rangos 0 a 5500.
        if PUERTO <= 0 or PUERTO >= 5500:
            print('[CONFIG] El valor ingresado no se encuentra en el rango esperado (0 - 5500).\n')
            PUERTO = '' # Si ingresa un valor fuera de los rangos borramos el dato para que caiga de nuevo en el bucle
            
    except ValueError:
        print('[CONFIG] Por favor ingrese solo valores numéricos. \n')
        PUERTO = '' # Si hubo un ingreso no correspondiente a los valores esperados de puerto también lo reinstanciamos a '' para que vuelva a caer en el bucle.

# Ingreso manual de nombre de usuario
while not NAME:
    
	# Le damos las pautas al usuario para que termine haciendo lo que se le cante.
    print('[CONFIG] Ingrese su nombre de usuario (entre 3 y 10 caracteres). \n')
    nombre_ingresado = input()
    
	# Lower por si lo escribe sin querer con una mayúscula
    # Acá también le dejamos salir del programa
    if input_user.lower() == 'salir':
        print('[CONFIG] Programa finalizado.')
        sys.exit()

	# Evaluamos si el largo del string ingresado está dentro de los rangos establecidos.
    if 3 <= len(nombre_ingresado) <= 10:
        NAME = nombre_ingresado # Si está todo ok asignamos el valor a la variable NAME ( NICK )
        
	# Si hizo todo mal no asignamos nada a la variable mostramos el error por pantalla y vuelve a iniciarse el bucle
    else:
        print('[CONFIG] Ha ingresado un nombre de usuario no válido. \n')

# Todo ok la configuración del usuario resta iniciar la conexión 
print(f"[{NAME}] Iniciando sala de chat. \n")

try:
    # Creamos el socket del cliente
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Un print fantasmagorico
    print(f"[{NAME}] Conectando... \n")
    
    # Creamos la conexión al server
    socket_cliente.connect((TCP_IP, PUERTO))
    
# Por si se cayo el server o ingresamos un dato mal
except socket.error as msg:
    
    # Mostramos el numero y el detalle del error
    print(f"Fallo en la conexión del socket. Código de Error: {msg.errno} , Mensaje de Error: {msg.strerror}")
    sys.exit()

# Otro de esos print que hacen creer que pasa algo
print(f"[{NAME}] Iniciando sesión. \n")

# Función para recibir mensajes
def recibir_mensaje():
    
	# Bucle para recibir mensajes
    while True:
        
		# Encerrado en except para detectar la perdida de conexión o la finalización de la misma por caso #LOGOUT
        try:
            # Recibir el mensaje que devuelve el server
            mensaje = socket_cliente.recv(BUFFER_SIZE)
            
			# Si no hay mensaje genero una excepción de manera intencionada quiere decir que el mensaje que recibi esta incompleto o paso algo
            if not mensaje:
                raise ConnectionError
            
			# Mensaje en UTF-8 para respetar signos y acentos
            print(mensaje.decode('utf-8'))
        
		# El error de conexión por caida del server o por #LOGOUT
        except ConnectionError:
            
			# Muestra por pantalla que se ha cerrado la conexión cierra el socket y finaliza el programa para cerrar los hilos.
            print(f"[SISTEMA] Se ha cerrado la conexión. \n")
            print("[SISTEMA] Programa finalizado. \n")
            socket_cliente.close()
            sys.exit()

# Función para enviar mensajes
def enviar_mensaje():
    
	# Bucle para enviar mensajes
    while True:
        
		# Lo encerramos en un try except por si se pierde la conexión
        try:
            
			# Levantamos el mensaje y le agregamos el nick para no tener que tratarlo en el server que nos va a representar mas laburo *El futuro es hoy*
            mensaje_usuario = input()
            mensaje = f"[{NAME}] {mensaje_usuario}"

			# Si el mensaje posee mas de 150 caracteres le decimos que no exceda ese valor y usamos continue para volver a caer en el bucle sin ejecutar lo que sigue
            if len(mensaje) > 150:
                
                print(f"[SISTEMA] Por favor no exceda los 150 caracteres.")
                continue
            
			# Si todo está ok enviamos el mensaje
            socket_cliente.send(mensaje.encode('utf-8'))
        
		# La excepción levanta errores de envío posiblemente causados por caida del server
        except:
            
			# Mostramos por pantalla que ha ocurrido un error, cerramos el socket y finalizamos el programa
            print("[SISTEMA] Ha ocurrido un error en el envío del mensaje. \n")
            print("[SISTEMA] Programa finalizado. \n")
            socket_cliente.close()
            sys.exit()

# Configuramos los hilos en variables y los dejamos en daemon true asi si se termina el programa ellos tambien se terminan de ejecutar.
hilo_enviar = threading.Thread(target=enviar_mensaje, daemon=True)
hilo_recibir = threading.Thread(target=recibir_mensaje, daemon=True)

# Inicio de las instancias de las funciones enviar y recibir en hilos
hilo_enviar.start()
hilo_recibir.start()

# Para mantener el programa activo porque sino me tira [WinError 10054] supongo que es por el daemon true
# y que al ser estructurado al finalizar da por sentado que debe finalizar la ejecución mas alla de que haya whiles dentro de los hilos 
# Seguramente debí haber creado una función main y ejecutarla como dios manda
try:
    while True:
        pass
    
# En caso de que apriete un ctrl + c para interrumpir la ejecución, cierra todo.
except KeyboardInterrupt:
    print("\n[SISTEMA] Programa finalizado por el usuario.")
    socket_cliente.close()
    sys.exit()
