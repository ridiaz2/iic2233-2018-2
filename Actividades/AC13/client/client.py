"""
client.py -- un simple cliente
"""

import pickle
from socket import socket, SHUT_RDWR

HOST = '127.0.0.1'


class Client:
    """
    Una clase que representa un cliente.
    """

    def __init__(self, port):
        self.host = HOST
        self.port = port
        self.socket = socket()
        self.connected = False

        # Este diccionario tiene los comandos disponibles.
        # Puedes modificarlo para agregar nuevos comandos.
        self.commands = {
            "help": self.help,
            "logout": self.logout,
            "ls": self.ls,
            "upload": self.upload,
            "download": self.download
        }

    def run(self):
        """
        Enciende el cliente que puede conectarse
        para enviar algunos comandos al servidor.
        """

        self.socket.connect((self.host, self.port))
        self.connected = True

        while self.connected:
            command, *args = input('$ ').split()
            function = self.commands.get(command)

            if function is None:
                print(f"El comando '{command}' no existe.")
                print("Escribe 'help' para obtener ayuda.")
            elif command == 'help':
                self.help()
            else:
                self.send(pickle.dumps((command, args)))
                function(*args)

    def send(self, message):
        """
        [MODIFICAR]
        Envía datos binarios al servidor conectado por el socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """

        if type(message) != bytes:
            message = pickle.dumps(message)
        largo = len(message).to_bytes(4, byteorder="big")

        self.socket.sendall(largo + message)


    def receive(self):
        """
        [COMPLETAR]
        Recibe datos binarios del servidor, a través del socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """

        mensaje_size = int.from_bytes(self.socket.recv(4),
                                      byteorder="big")

        mensaje_bytes = bytearray()

        # Recibimos el resto de los datos
        while len(mensaje_bytes) < mensaje_size:
            mensaje_bytes += self.socket.recv(4096)


        # Decodificamos y pasamos a JSON el mensaje

        return mensaje_bytes

    def help(self):
        print("Esta es la lista de todos los comandos disponibles.")
        print('\n'.join(f"- {command}" for command in self.commands))

    def ls(self):
        """
        [COMPLETAR]
        Este comando recibe una lista con los archivos del servidor.

        Ejemplo:
        $ ls
        - doggo.jpg
        - server.py
        """

        nombres = pickle.loads(self.receive())

        for nombre in nombres:
            print(nombre)

    def upload(self, *args):
        """
        [COMPLETAR]
        Este comando envía un archivo hacia el servidor.
        """
        diccionario = dict()
        for filename in args:
            with open(filename, "rb") as archivo:
                diccionario[filename] = archivo.read()
        self.send(pickle.dumps(diccionario))





    def download(self, *listado):
        """
        [COMPLETAR]
        Este comando recibe un archivo ubicado en el servidor.
        """

        listado = self.receive()
        lista = pickle.loads(listado)
        for nombre, datos in lista.items():
            with open(nombre, "wb") as archivo:
                archivo.write(datos)


    def logout(self):
        self.connected = False
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()
        print("Arrivederci.")


if __name__ == '__main__':
    port_ = input("Escriba el puerto: ")
    client = Client(int(port_))
    client.run()
