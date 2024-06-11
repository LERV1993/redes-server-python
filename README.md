
# Comunicación cliente servidor

Existen dos archivos para cada una de las funcionalidades `cliente.py` y `server.py`, cada uno de ellos sirve para operar como su nombre lo indica.

El servidor sirve para abrir una instancia en un ip y un puerto que permita al cliente conectarse enviar un mensaje.

Cada cliente conectado es manejado desde una funcion que se deriva a un hilo para que el servidor permita concurrencia.

### Server

Se utilizan las librerias `threading` y `socket`.

La configuración del server es la siguiente:

- TCP_IP = '127.0.0.1' `IP local asignado donde está funcionando`
- PUERTO = 5500  `Puerto en el que funciona`
- TAM_BUFFER = 20 `Se utiliza esta configuración por motivos de velocidad`

Dentro de server se encontrarán 3 funciones definidas `manejar_cliente | datos_recibidos_respuesta | main`.

* Manejar Cliente
Recibe por parametro el socket del cliente y la dirección de este.
Se crea un arreglo de bytes mutables y se asigna a la variable `datos`. 

Luego se utiliza `try | catch` para poder levantar una excepción de conexión.

Se reciben datos del cliente y se evalua que correspondan con el tamaño de buffer prestablecido en `TAM_BUFFER`.
Si no se reciben datos se devuelve un mensaje por consola informando que se ha perdido la conexión y se sale del bucle para escapar posibles errores.

Se agregan los datos recibidos al arreglo de bytes mutables.
Se muestra por consola información correspondiente a los datos recibidos y la dirección del cliente.

Se busca el salto de linea en los datos recibidos (que es un mensaje) para saber donde termina y se lo restructura el mensaje sacando el salto de linea `"/n"` y se lo configura para `utf-8` para aceptar acentos y la letra ñ.

Se hace uso de la función `datos_recibidos_respuesta` y luego se envía una respuesta al cliente.

Se muestra por consola el mensaje enviado y la dirección del cliente a la que se envío y luego se cierra la conexión con el cliente.

- Datos recibidos respuesta

Recibe por parametro `direccion_cliente | mensaje | datos_recibidos` e imprime por consola información relativa a las actividades realizadas con esta información.

- Main

Se crea el socket especificando la familia `socket.AF_INET` indicando que se trabajará con direcciones IP y números de puerto de la familia IPv4 y `SOCK_STREAM` indicando que se va a crear un socket de tipo de flujo de datos TCP.

Se hace el bind del socket con los valores especificados en `TCP_IP | PUERTO`.

Luego se define el socket en listen con 5, lo cual indica el número máximo de conexiones que acepta. El server se quedará escuchando en el IP y el puerto configurados.

Cuando el socket recibe una conexión es crea un hilo con la función `manejar cliente` e inicializa el hilo para seguir escuchando.

### Cliente 
Este proyecto implementa un cliente TCP simple en Python diseñado para conectarse a un servidor TCP multihilo. El cliente envía un mensaje `MESSAGE = "Hola Server!"` al servidor y espera una respuesta, la cual se muestra en la consola.


- Conexión al Servidor
El cliente se conecta a un servidor TCP especificado en la dirección IP 127.0.0.1 y el puerto 5500, los mismos que el servidor utiliza para aceptar conexiones.

- Envío de Datos
El cliente envía un mensaje al servidor. El mensaje termina con un carácter de nueva línea (\n), que el servidor usa para determinar el final del mensaje.

- Recepción de Datos
El cliente espera la respuesta del servidor y la muestra en la consola. El servidor, en este caso, responde con los mismos datos que recibió del cliente (eco).

- Manejo de Errores
El cliente maneja posibles errores de conexión e imprime mensajes de error en la consola si ocurre algún problema durante la comunicación con el servidor.








## Información y agradecimientos

Este proyecto nace de la cursada de la matería de programación sobre redes del último año de la Tecnicatura en desarrollo de software. Impartido por el docente [Javier Juan Carlos Blanco](https://github.com/jjcblanco).


## Authors

- [Gabriel Pettinari](https://github.com/GabrielPetty)
- [Gastón Murua](https://github.com/JGastonMurua)
- [Lucas Ruiz](https://github.com/LERV1993)

