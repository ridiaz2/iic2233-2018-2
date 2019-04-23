"""
server.py -- un simple servidor
"""

import pickle
from socket import socket
import os

HOST = '127.0.0.1'


class Server:
    """
    Una clase que representa un servidor.
    """

    def __init__(self, port):
        self.host = HOST
        self.port = port
        self.client = None
        self.socket = socket()

        self.commands = {
            "ls": self.list_filenames,
            "download": self.send_file,
            "upload": self.save_file,
            "logout": self.disconnect,
        }

    def run(self):
        """
        Enciende el servidor que puede conectarse
        y recibir comandos desde un único cliente.
        """

        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Escuchando en {self.host}:{self.port}.")

        while self.client is None:
            self.client, _ = self.socket.accept()
            print("¡Un cliente se ha conectado!")

            while self.client:
                command, args = pickle.loads(self.receive())
                self.commands[command](*args)

        print("Arrivederci.")

    def send(self, message):
        """
        [COMPLETAR]
        Envía datos binarios al cliente conectado por el socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """

        largo = len(message).to_bytes(4, byteorder="big")
        self.client.sendall(largo + message)

    def receive(self):
        """
        [MODIFICAR]
        Recibe datos binarios del cliente, a través del socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """
        # Esta parte del código está basada en la ayudantía :D

        print("Receive de server")

        mensaje_size = int.from_bytes(self.client.recv(4),
                                    byteorder="big")

        mensaje_bytes = bytearray()

        # Recibimos el resto de los datos
        while len(mensaje_bytes) < mensaje_size:
            mensaje_bytes += self.client.recv(4096)

        print("Mensaje:", mensaje_bytes)

        return mensaje_bytes  # maldición, esto es poco.

    def list_filenames(self):
        """
        [COMPLETAR]
        Envía al cliente una lista que contiene los nombres de
        todos los archivos existentes en la carpeta del servidor.
        """

        nombres = pickle.dumps(list([i for i in os.listdir("./") if not
            i.endswith(".py")]))
        self.send(nombres)


    def send_file(self, *args):
        """
        [COMPLETAR]
        Envía al cliente un archivo ubicado en el directorio del servidor.
        """

        diccionario = dict()
        for filename in args:
            with open(filename, "rb") as archivo:
                diccionario[filename] = archivo.read()
        self.send(pickle.dumps(diccionario))

    def save_file(self, *listado):
        """
        [COMPLETAR]
        Guarda un archivo recibido desde el cliente.
        """
        listado = self.receive()
        lista = pickle.loads(listado)
        for nombre, datos in lista.items():
            with open(nombre, "wb") as archivo:
                archivo.write(datos)
        print("guarda3")

    def disconnect(self):
        self.client = None
        print("El cliente se ha desconectado.")


if __name__ == '__main__':
    port_ = input("Escriba el puerto: ")
    server = Server(int(port_))
    server.run()
