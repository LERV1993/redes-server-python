
# Comunicación cliente servidor

Existen dos archivos para cada una de las funcionalidades `cliente.py` y `server.py`, cada uno de ellos sirve para operar como su nombre lo indica.

El servidor sirve para abrir una instancia en un ip y un puerto que permita al cliente conectarse a la sala de chat y enviar mensajes.

Cada cliente conectado es manejado desde una funcion que se deriva a un hilo para que el servidor permita concurrencia.

### Server

Se utilizan las librerias `threading` y `socket`.

La configuración del server es la siguiente:

- TCP_IP = '127.0.0.1' `IP local asignado donde está funcionando`
- PUERTO = 5000  `Puerto en el que funciona`
- TAM_BUFFER = 200   `Para masomenos manejar mensajes de 150 caracteres`

El servidor inicia y verifica que el puerto esté disponible.
Una vez iniciado queda escuchando en la función main hasta que acepta una conexión por parte del cliente, guarda el socket del cliente en un array global de clientes 
y luego inicia un hilo con la funcion de manejar cliente que se encarga de recibir los mensajes y devolverlos a todos los clientes menos al que envía el mensaje.

### Cliente 

- Configuración:
Se solicita el número de puerto al que desea conectarse que debe estar entre los valores `0 | 5000`.
Se solicita el nick o nombre de usuario.

Durante la configuración si el usuario ingresa salir el programa se finaliza.

- Ingreso a la sala:

El cliente crea dos hilos hijos para mandar y recibir mensajes.
Se ejecuta una función try con un while pass para mantener el programa en ejecución y que los hilos se sigan ejecutando.

Para cerrar la sessión se debe enviar un mensaje que contenga `#LOGOUT`.

## Información y agradecimientos

Este proyecto nace de la cursada de la matería de programación sobre redes del último año de la Tecnicatura en desarrollo de software. Impartido por el docente [Javier Juan Carlos Blanco](https://github.com/jjcblanco).


## Authors

- [Gabriel Pettinari](https://github.com/GabrielPetty)
- [Gastón Murua](https://github.com/JGastonMurua)
- [Lucas Ruiz](https://github.com/LERV1993)

