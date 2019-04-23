__author__ = "jnhasard & pnheinsohn"

import threading as th
import socket
import json
import os
import csv

import os.path
import hashlib
import pickle
import time
import random
from PyQt5.QtCore import QObject, pyqtSignal
from backend import ruta, Player, Avanzar, EnviarMapa



from PyQt5.QtCore import QTimer

HOST = "localhost"
PORT = 8083
ruta_datos = "./bd"
ruta_usuarios = f"{ruta_datos}/usuarios.txt"

def str_a_bytes(string):
    print("AAAH", string)
    return bytes(string[2:-1], "utf-8")

class Servidor:

    def __init__(self):

        self.host = HOST
        self.port = PORT

        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen(5)
        print(f"Servidor escuchando en {self.host}:{self.port}...")

        thread = th.Thread(target=self.aceptar_conexiones_thread, daemon=True)
        thread.start()
        self.sockets = {}
        self.nombres = {}
        print("Servidor aceptando conexiones...")

        self.partidas = []
        self.partidas_sockets = dict()
        self.juegos = []
        self.juegos_sockets = dict()


    def aceptar_conexiones_thread(self):
        '''
        Este método es utilizado en el thread para ir aceptando conexiones de
        manera asíncrona al programa principal
        :return:
        '''

        while True:
            client_socket, _ = self.socket_servidor.accept()
            self.sockets[client_socket] = None
            self.nombres[client_socket] = None
            print("Servidor conectado a un nuevo cliente...")

            listening_client_thread = th.Thread(
                target=self.escuchar_cliente_thread,
                args=(client_socket,),
                daemon=True
            )
            listening_client_thread.start()
            if len(self.sockets) == 5:
                break


    def escuchar_cliente_thread(self, client_socket):
        '''
        Este método va a ser usado múltiples veces en threads pero cada vez con
        sockets de clientes distintos.
        :param client_socket: objeto socket correspondiente a algún cliente
        :return:
        '''


        while True:
            print("ESCUCHANDO A CLIENTE")
            try:
                print("entró a try")
                # Primero recibimos los 4 bytes del largo
                response_bytes_length = client_socket.recv(4)
                # Los decodificamos
                response_length = int.from_bytes(response_bytes_length,
                                                 byteorder="big")

                # Luego, creamos un bytearray vacío para juntar el mensaje
                response = bytearray()

                # Recibimos datos hasta que alcancemos la totalidad de los datos
                # indicados en los primeros 4 bytes recibidos.
                print("entrando a while")
                response += client_socket.recv(response_length)
              #  while len(response) < response_length:
               #     response += client_socket.recv(256)
                print("salió while")
                # Una vez que tenemos todos los bytes, entonces ahí decodificamos
                try:
                    print("¿es json?")
                    response_decodificado = response.decode()

                    # Luego, debemos cargar lo anterior utilizando json
                    decoded = json.loads(response_decodificado)
                    print("sí :D")
                except (UnicodeDecodeError):
                    print("no :O")
                    decoded = pickle.loads(response)

                print("recibido de escuchar", decoded)
                # Para evitar hacer muy largo este método, el manejo del mensaje se
                # realizará en otro método
                self.manejar_comando(decoded, client_socket)
            except ConnectionResetError:
                print("entró a except")
                decoded_message = {"estado": "cerrar_sesion", "contenido":
                    client_socket}
                self.manejar_comando(decoded_message, client_socket)
                break

    def revisar_inicio(self, actual_user, actual_password):

        with open(ruta_usuarios, "rb") as archivo:
            diccionario = pickle.load(archivo)

        bytes_usuario = actual_user.encode()
        bytes_password = actual_password.encode()
        if bytes_usuario not in diccionario:
            return "usuario"

        bytes_sal = diccionario[bytes_usuario][0]
        bytes_hash_pass = diccionario[bytes_usuario][1]
        bytes_hash = hashlib.sha256(bytes_sal + bytes_password).digest()

        if bytes_hash != bytes_hash_pass:
            return "contraseña"
        if actual_user in self.nombres.values():
                return "usuario_rep"
            #if actual_user in partida.jugadores:
             #   return "usuario_rep"

        return True

    def revisar_registro(self, actual_user, actual_password,
                         actual_password_rep):

        if not os.path.isfile(ruta_usuarios):
            with open(ruta_usuarios, "wb") as archivo:
                pickle.dump(dict(), archivo)

        #https://www.tutorialspoint.com/How-to-check-
        # if-a-string-is-alphanumeric-in-Python
        if not actual_user.isalnum():
            return "usuario"

        elif actual_password != actual_password_rep:
            return "contraseña"

        bytes_sal = os.urandom(8)
        bytes_password = actual_password.encode()

        bytes_hash = hashlib.sha256(bytes_sal + bytes_password).digest()
        bytes_usuario = actual_user.encode()

        with open(ruta_usuarios, "rb") as archivo:
            diccionario = pickle.load(archivo)
        if bytes_usuario in diccionario:
            return "usuario_rep"

        with open(ruta_usuarios, "wb") as archivo:
            diccionario[bytes_usuario] = (bytes_sal, bytes_hash)
            pickle.dump(diccionario, archivo)
        return True

    def revisar_listado_partidas(self):
        return [(i.nombre, len(i.jugadores)) for i in self.partidas]

    def obtener_color_random(self, partida):
        numero = random.randint(1, 32)
        while numero in partida.colores:
            numero = random.randint(1, 32)
        return numero



    def manejar_comando(self, recibido, socket_cliente=""):
        '''
        Este método toma lo recibido por el cliente correspondiente al socket pasado
        como argumento.
        :param recibido: diccionario de la forma: {"status": tipo, "data": información}
        :param client_socket: socket correspondiente al cliente que envió el mensaje
        :return:
        '''


        # Podemos imprimir para verificar que toodo anda bien
        print("Mensaje Recibido: {}".format(recibido))

        if recibido["estado"] == "inicio_sesion":
            respuesta = self.revisar_inicio(*recibido["contenido"])
            diccionario = {"estado": "inicio_sesion", "contenido": respuesta}
            self.send(diccionario, socket_cliente)
            print("respuestaaaaaaaaaaaa")
            if respuesta:
                print("nombreeee", recibido["contenido"][0])
                self.nombres[socket_cliente] = recibido["contenido"][0]

        elif recibido["estado"] == "mover":
            mensaje = recibido["contenido"]
            print("MOvienDO JUGADOR", mensaje)
            juego = self.juegos_sockets[socket_cliente]
            if mensaje == "E":
                juego.pausa = False if juego.pausa else True
            else:
                nombre = juego.jugadores_sockets[socket_cliente]
                player = juego.players[nombre]
                player.move(mensaje)

        elif recibido["estado"] == "mover_invitado":
            mensaje = recibido["contenido"]
            print("MOvienDO INVITADO", mensaje)
            juego = self.juegos_sockets[socket_cliente]
            nombre = juego.jugadores_sockets[socket_cliente]
            player = juego.players[f"{nombre} (Invitado)"]
            player.move(mensaje)

        elif recibido["estado"] == "registro":
            print("entra a server")
            respuesta = self.revisar_registro(*recibido["contenido"])
            diccionario = {"estado": "registro", "contenido": respuesta}
            self.send(diccionario, socket_cliente)

        elif recibido["estado"] == "actualizar_lista":
            print("llega a server")
            respuesta = self.revisar_listado_partidas()
            print(respuesta)
            diccionario = {"estado": "actualizar_lista", "contenido": respuesta}
            self.send(diccionario, socket_cliente)

        elif recibido["estado"] == "nueva_partida":
            print("recibido server")
            print(recibido)
            nombre, usuario = recibido["contenido"]
            partida = Partida(nombre, usuario)
            partida.jugadores_sockets[socket_cliente] = usuario
            partida.jugadores.append(usuario)
            partida.colores[usuario] = self.obtener_color_random(partida)
            self.partidas.append(partida)
            self.partidas_sockets[socket_cliente] = partida

            respuesta = self.revisar_listado_partidas()
            diccionario = {"estado": "nueva_partida", "contenido": respuesta}
            self.send(diccionario, socket_cliente)
            time.sleep(2)
            partida_dicc = partida.datos()
            diccionario_ = {"estado": "actualizar_partida", "contenido":
                partida_dicc}
            self.send(diccionario_, socket_cliente)

        elif recibido["estado"] == "seleccionar_partida":
            indice, nombre = recibido["contenido"]
            print(nombre, indice)
            print("en server")
            if len(self.partidas[indice].jugadores) <= 4:
                print("está disponible :D")
                self.partidas_sockets[socket_cliente] = self.partidas[indice]
                self.partidas[indice].jugadores_sockets[socket_cliente] = nombre
                self.partidas[indice].jugadores.append(nombre)
                self.partidas[indice].colores[nombre] \
                    = self.obtener_color_random(self.partidas[indice])
                diccionario = {"estado": "seleccionar_partida",
                               "contenido": (True, self.partidas[
                                   indice].nombre, indice)}
                self.send(diccionario, socket_cliente)
                time.sleep(2)
                partida_dicc = self.partidas[indice].datos()
                diccionario_ = {"estado": "actualizar_partida", "contenido":
                    partida_dicc}
                for _socket in self.partidas[indice].jugadores_sockets.keys():
                    print("enviado a", self.partidas[indice].jugadores_sockets[
                        _socket])
                    self.send(diccionario_, _socket)
            else:
                diccionario = {"estado": "seleccionar_partida",
                               "contenido": (False, self.partidas[
                                   indice].nombre, indice, self.partidas[
                                   indice].jugadores)}
                self.send(diccionario, socket_cliente)

        elif recibido["estado"] == "enviar_mensaje":
            nombre, mensaje, indice = recibido["contenido"]
            self.partidas[indice].chat.append((nombre, mensaje))
            self.partidas[indice].actualizar_chat = True
            partida_dicc = self.partidas[indice].datos()
            self.partidas[indice].actualizar_chat = False
            diccionario_ = {"estado": "actualizar_partida", "contenido":
                partida_dicc}
            for _socket in self.partidas[indice].jugadores_sockets.keys():
                print("enviado a", self.partidas[indice].jugadores_sockets[
                    _socket])
                self.send(diccionario_, _socket)

        elif recibido["estado"] == "actualizar_color":
            nombre_usuario, n_color, indice = recibido["contenido"]
            partida = self.partidas[indice]
            if n_color not in partida.colores.values():
                partida.colores[nombre_usuario] = n_color
                diccionario_ = {"estado": "actualizar_partida", "contenido":
                    partida.datos()}
                for _socket in self.partidas[indice].jugadores_sockets.keys():
                    self.send(diccionario_, _socket)

        elif recibido["estado"] == "agregar_invitado":
            usuario, indice = recibido["contenido"]
            nombre = f"{usuario} (Invitado)"
            partida = self.partidas[indice]
            partida.jugadores.append(nombre)
            partida.colores[nombre] = self.obtener_color_random(partida)
            diccionario_ = {"estado": "actualizar_partida", "contenido":
                partida.datos()}
            for _socket in self.partidas[indice].jugadores_sockets.keys():
                self.send(diccionario_, _socket)

        elif recibido["estado"] == "iniciar_contador":
            '''https://stackoverflow.com/questions/
            40994187/pyqt-showing-countdown-timer'''
            indice = recibido["contenido"]
            partida = self.partidas[indice]

            cuenta_regresiva = Contador(self, partida)
            cuenta_regresiva.start()



        elif recibido["estado"] == "actualizar_contador":
            partida = recibido["contenido"]
            diccionario_ = {"estado": "actualizar_contador", "contenido":
                partida.contador}
            for _socket in partida.jugadores_sockets.keys():
                print("enviado a", partida.jugadores_sockets[
                    _socket])
                self.send(diccionario_, _socket)

        elif recibido["estado"] == "recepcion_datos_jefe":
            indice, datos = recibido["contenido"]
            print("Estos son los datos que recopilamos --->", datos)
            partida = self.partidas[indice]
            juego = Juego(self, partida, datos)
            print("juego agregado", juego)
            self.juegos.append(juego)
            self.partidas[indice] = juego
            self.partidas_sockets[socket_cliente] = juego
            self.juegos_sockets[socket_cliente] = juego
            diccionario_ = {"estado": "comenzar_juego", "contenido": juego}
            for _socket in partida.jugadores_sockets:
                self.juegos_sockets[_socket] = juego
                self.send_pickle(diccionario_, _socket)
     #       self.servidor.manejar_comando({"estado": "comenzar_juego",
      #                                     "contenido": self.partida})

        elif recibido["estado"] == "teclas_listas":
            listas = list(recibido["contenido"])
            juego = self.juegos_sockets[socket_cliente]
            juego.jugadores_listos += listas
            if len(juego.jugadores_listos) == len(juego.jugadores):
                diccionario_ = {"estado": "pasar_a_juego", "contenido": juego}
                for _socket in juego.jugadores_sockets:
                    self.send_pickle(diccionario_, _socket)
                time.sleep(4)
                for jugador in juego.players.values():
                    jugador.avanzanding.start()
                juego.actualizar.start()

        elif recibido["estado"] == "comenzar_juego":
            partida = recibido["contenido"]
            diccionario_ = {"estado": "actualizar_contador", "contenido":
                partida}
            for _socket in partida.jugadores_sockets.keys():
                print("enviado a", partida.jugadores_sockets[
                    _socket])
                self.send(diccionario_, _socket)




        elif recibido["estado"] == "cerrar_sesion":
            client_socket = recibido["contenido"]
            self.nombres.pop(socket_cliente)
            if socket_cliente in self.partidas_sockets:
                partida = self.partidas_sockets.pop(socket_cliente)
                nombre_usuario = partida.jugadores_sockets.pop(socket_cliente)
                partida.jugadores.remove(nombre_usuario)
                partida.colores.pop(nombre_usuario)
                if f"{nombre_usuario} (Invitado)" in partida.jugadores:
                    partida.jugadores.remove(f"{nombre_usuario} (Invitado)")
                    partida.colores.pop(f"{nombre_usuario} (Invitado)")
            if socket_cliente in self.juegos_sockets:
                self.juegos_sockets.pop(socket_cliente)

            del self.sockets[socket_cliente]
            diccionario_ = {"estado": "actualizar_partida", "contenido":
                partida.datos()}
            for _socket in partida.jugadores_sockets.keys():
                print("enviado a", partida.jugadores_sockets[
                    _socket])
                self.send(diccionario_, _socket)


        '''
        if recibido["status"] == "mensaje":
            msj = {"status": "mensaje",
                   "data": {"usuario": self.sockets[client_socket],
                            "contenido": recibido["data"]["contenido"]}}
            for skt in self.sockets.keys():
                self.send(msj, skt)

        elif recibido["status"] == "nuevo_usuario":
            self.sockets[client_socket] = recibido["data"]

        elif recibido["status"] == "cerrar_sesion":
            del self.sockets[client_socket]
            
        '''

    @staticmethod
    def send(valor, socket):
        '''
        Este método envía la información al cliente correspondiente al socket.
        :param msg: diccionario del tipo {"status": tipo del mensaje, "data": información}
        :param socket: socket del cliente al cual se le enviará el mensaje
        :return:
        '''

        # Le hacemos json.dumps y luego lo transformamos a bytes
        msg_json = json.dumps(valor)
        msg_bytes = msg_json.encode()

        # Luego tomamos el largo de los bytes y creamos 4 bytes de esto
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")

        # Finalmente, los enviamos al servidor
        socket.send(msg_length + msg_bytes)

    @staticmethod
    def send_pickle(valor, socket):
        # Le hacemos json.dumps y luego lo transformamos a bytes
        mensaje_codificado = pickle.dumps(valor)

        # Luego tomamos el largo de los bytes y creamos 4 bytes de esto
        largo_mensaje = len(mensaje_codificado).to_bytes(4, byteorder="big")

        # Finalmente, los enviamos al servidor
        socket.send(largo_mensaje + mensaje_codificado)


class Partida:
    def __init__(self, nombre, jugador):
        self.nombre = nombre
        self.jugadores_sockets = dict()
        self.admin = jugador
        self.chat = []
        self.actualizar_chat = False
        self.colores = dict()
        self.jugadores = []
        self.contador = 10


    def datos(self):
        diccionario = self.__dict__.copy()
        diccionario.pop("jugadores_sockets")
        return diccionario

class Juego:
    def __init__(self, servidor, partida, datos_jefe):

        self.actualizar = EnviarMapa(servidor, self)
        self.nombre = partida.nombre
        self.poderes, self.velocidad, self.puntaje_max = datos_jefe
        self.poderes = list([n + 1 for n in range(len(self.poderes)) if
                        self.poderes[n]])
        self.jugadores_sockets = partida.jugadores_sockets
        self.marcados = []
        self.colores = partida.colores
        self.jugadores = partida.jugadores
        self.jugadores_listos = []
        self.horizontal, self.vertical = (160, 621), (18, 338)
        self.players = dict()
        self.servidor = servidor
        self.agregar_jugadores()
        self.pausa = False
        self._lista_poderes = []

    @property
    def lista_poderes(self):
        self._lista_poderes = list([i for i in self._lista_poderes if
                                    i.habilitado])
        return self._lista_poderes

    @property
    def posiciones_poderes(self):
        return dict({(i.x, i.y): i for i in
                     self._lista_poderes if i.habilitado})



    def agregar_jugadores(self):
        posiciones_guardadas = []

        for jugador in self.jugadores:
            aprueba = False
            while not aprueba:
                x, y = random.randint(200, 600), random.randint(38, 310)
                angulo = random.randint(0, 359)
                color = self.colores[jugador]
                ruta_actual = list(ruta(x, y, angulo,
                     self.horizontal, self.vertical, posiciones_guardadas))
                aprueba = (len(ruta_actual) > 100)
            player = Player(self, x, y, angulo, color)
            self.players[jugador] = player



    def __getstate__(self):
        nueva = self.__dict__.copy()
        nueva["jugadores_sockets"] = dict({str(i): j for i, j in nueva[
            "jugadores_sockets"].items()})
        nueva["actualizar"] = None
        nueva["servidor"] = None
        nueva["lista_poderes"] = self.lista_poderes

        print(nueva)
        # esto es lo que será serializado por pickle
        return nueva

    def __setstate__(self, state):
        self.__dict__ = state

    def datos(self):
        diccionario = self.__dict__.copy()
        diccionario.pop("jugadores_sockets")
        return diccionario

    def __str__(self):
        return str(self.nombre) + str([str(i) for i in self.players.values()])



class Contador(th.Thread):
    """Este será nuestro nuevo Worker basado en Thread"""

    def __init__(self, servidor, partida):
        # En el caso de los threads, lo primero es invocar al init original.
        super().__init__()
        self.partida = partida
        self.servidor = servidor
        self.daemon = True

    def run(self):
        for n in range(10, 0, -1):
            self.servidor.manejar_comando({"estado": "actualizar_contador",
                                           "contenido": self.partida})
            print("CONTADOR:", n)
            time.sleep(1)
            self.partida.contador -= 1
        print("LLEGAMOS AL CONTADOR :D")
        diccionario_ = {"estado": "solicitud_datos_jefe", "contenido": ""}
        print(list(self.partida.jugadores_sockets.keys())[0])
        print(self.partida.jugadores_sockets[
                  list(self.partida.jugadores_sockets.keys())[0]])
        self.servidor.send(diccionario_, list(
            self.partida.jugadores_sockets.keys())[0])


if __name__ == "__main__":


    server = Servidor()

    # Mantenemos al server corriendo
    while True:
        pass
