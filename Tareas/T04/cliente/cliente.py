__author__ = "jnhasard & pnheinsohn"

import sys
import threading as th
import socket
import json
import pickle
from frontend import MainWindow
from PyQt5.QtWidgets import QApplication
from datetime import datetime
from juego import Game
from PyQt5.QtWidgets import QWidget, QApplication
from backend import Player


HOST = "localhost"
PORT = 8083

class Cliente:

    '''
    Esta es la clase encargada de conectarse con el servidor e intercambiar información
    '''

    def __init__(self):
        print("Inicializando cliente...")
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = HOST
        self.port = PORT

        self.frontend = MainWindow(self)
        self.frontend.show()
        self.sala_espera = []

        try:
            self.socket_cliente.connect((self.host, self.port))
            print("Cliente conectado exitosamente al servidor")

            self.conectado = True

            escuchar_servidor = th.Thread(target=self.escuchar, daemon=True)
            escuchar_servidor.start()
            print("Escuchando al servidor...")

        except ConnectionRefusedError:
            self.terminar_conexion()

    def restart(self):
        self.conectado = False
        print("Inicializando cliente...")
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = HOST
        self.port = PORT

        self.frontend = MainWindow(self)
        self.frontend.show()
        self.sala_espera = []

        try:
            self.socket_cliente.connect((self.host, self.port))
            print("Cliente conectado exitosamente al servidor")

            self.conectado = True

            escuchar_servidor = th.Thread(target=self.escuchar, daemon=True)
            escuchar_servidor.start()
            print("Escuchando al servidor...")

        except ConnectionRefusedError:
            self.terminar_conexion()

    def escuchar(self):
        '''
        Este método es usado en el thread y la idea es que reciba lo que
        envía el servidor. Implementa el protocolo de agregar los primeros
        4 bytes, que indican el largo del mensaje
        '''

        while self.conectado:
            try:
                # Recibimos los 4 bytes del largo
                tamano_mensaje_bytes = self.socket_cliente.recv(4)
                tamano_mensaje = int.from_bytes(tamano_mensaje_bytes, byteorder="big")
                
                contenido_mensaje_bytes = bytearray()

                # Recibimos el resto de los datos
                #contenido_mensaje_bytes += self.socket_cliente.recv(
                #    tamano_mensaje)
                while len(contenido_mensaje_bytes) < tamano_mensaje:
                    contenido_mensaje_bytes += self.socket_cliente.recv(1024)

                # Decodificamos y pasamos a JSON el mensaje
                try:
                    contenido_mensaje = contenido_mensaje_bytes.decode("utf-8")
                    mensaje_decodificado = json.loads(contenido_mensaje)
                except UnicodeDecodeError:
                    mensaje_decodificado = pickle.loads(contenido_mensaje_bytes)

                # Manejamos el mensaje
                self.manejar_comando(mensaje_decodificado)
            
            except ConnectionResetError:
                self.terminar_conexion()

    def manejar_comando(self, diccionario):
        '''
        Este método toma el mensaje decodificado de la forma:
        {"status": tipo del mensaje, "data": información}
        '''

     #   print(f"Mensaje recibido: {diccionario}")

        if diccionario["estado"] == "inicio_sesion":
            self.frontend.mensaje = diccionario["contenido"]

        elif diccionario["estado"] == "registro":
            self.frontend.mensaje = diccionario["contenido"]

        elif diccionario["estado"] == "actualizar_lista":
            self.ventana_partidas.mensaje = diccionario["contenido"]
            print(self.ventana_partidas)
            print(self.ventana_partidas.mensaje)

        elif diccionario["estado"] == "nueva_partida":
            self.ventana_partidas.mensaje = diccionario["contenido"]

        elif diccionario["estado"] == "seleccionar_partida":
            self.ventana_partidas.mensaje = diccionario["contenido"]

        elif diccionario["estado"] == "actualizar_partida":
            print("SALA ESPERA:", self.sala_espera)
            self.sala_espera.actualizar_datos(diccionario["contenido"])

        elif diccionario["estado"] == "actualizar_contador":
            self.sala_espera.actualizar_contador(diccionario["contenido"])

        elif diccionario["estado"] == "solicitud_datos_jefe":
            self.sala_espera.enviar_datos()


        elif diccionario["estado"] == "comenzar_juego":
            self.sala_espera.mensaje = diccionario["contenido"]
            self.sala_espera.chequeador.check_iniciar_juego()

        elif diccionario["estado"] == "pasar_a_juego":
            print("PASAR A JUEGO")
            self.juego = diccionario["contenido"]
            print("JUWGO GUARDADO")
            self.game.comenzar_juego()
            print("JUEGO COMENZADO")
            self.game.mostrar_jugadores(self.juego)
            print("MOSTRAR JUGADORES")

        elif diccionario["estado"] == "actualizar_mapa":
 #           print("recibiendo actualizar")
            self.game.actualizar_mapa(diccionario["contenido"])

        if diccionario["estado"] == "mensaje":
            data = diccionario["data"]
            usuario = data["usuario"]
            contenido = data["contenido"]
            usuario = f"({datetime.now().hour}:{datetime.now().minute})" \
                      f"{usuario}"
            self.frontend.ventana_chat.actualizar_chat(f"{usuario}: "
                                                       f"{contenido}")

    @staticmethod
    def send_pickle(valor, socket):
        # Le hacemos json.dumps y luego lo transformamos a bytes
        mensaje_codificado = pickle.dumps(valor)

        # Luego tomamos el largo de los bytes y creamos 4 bytes de esto
        largo_mensaje = len(mensaje_codificado).to_bytes(4, byteorder="big")

        # Finalmente, los enviamos al servidor
        socket.send(largo_mensaje + mensaje_codificado)

    def send(self, mensaje):
        '''
        Este método envía la información al servidor. Recibe un mensaje del tipo:
        {"status": tipo del mensaje, "data": información}
        '''

        # Codificamos y pasamos a bytes
        mensaje_codificado = json.dumps(mensaje)
        contenido_mensaje_bytes = mensaje_codificado.encode("utf-8")

        # Tomamos el largo del mensaje y creamos 4 bytes de esto
        tamano_mensaje_bytes = len(contenido_mensaje_bytes).to_bytes(4, byteorder="big")

        # Enviamos al servidor
        self.socket_cliente.send(tamano_mensaje_bytes + contenido_mensaje_bytes)

    def terminar_conexion(self):
        print("Conexión terminada")
        self.connected = False
        self.socket_cliente.close()
        for i in (self.frontend, self.ventana_partidas):
            i.status = False
        exit()

class Juego:
    def __init__(self, partida, datos_jefe):
        self.poderes, self.velocidad, self.puntaje_max = datos_jefe
        self.jugadores_sockets = partida.jugadores_sockets
        self.colores = partida.colores
        self.jugadores = partida.jugadores
        self.jugadores_listos = []

    def __getstate__(self):
        nueva = self.__dict__.copy()
        nueva["jugadores_sockets"] = dict({str(i): j for i, j in nueva[
            "jugadores_sockets"].items()})
        # esto es lo que será serializado por pickle
        return nueva

    def __setstate__(self, state):
        self.__dict__ = state

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()

        # Definimos la geometría de la ventana.
        # Parámetros: (x_top_left, y_top_left, width, height)
        self.setGeometry(200, 100, 300, 300)

        # Podemos dar nombre a la ventana (Opcional)
        self.setWindowTitle('Mi Primera Ventana')

if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication(sys.argv)
    cliente = Cliente()


    sys.exit(app.exec_())
    print("saliendo :D gracias c:")
