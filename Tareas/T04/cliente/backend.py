from PyQt5.QtCore import QSize, QObject, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QLabel

import threading
import time
import csv
import os.path
import hashlib
import pickle

from excepciones import ErrorIngreso, ErrorRegistro


######################### MODIFICABLES ######################################
ruta_imagenes = "./imagenes"
ruta_datos = "./bd"

ruta_fondos = f"{ruta_imagenes}/fondos"
ruta_colores = f"{ruta_imagenes}/colores"
ruta_usuarios = f"{ruta_datos}/usuarios.txt"
ruta_mapa = f"{ruta_imagenes}/mapa.png"
ruta_sprites = f"{ruta_imagenes}/sprites"
ruta_gifs = f"{ruta_imagenes}/gifs"
ruta_iconos = f"{ruta_imagenes}/iconos"



##############################################################################


diccionario_colores = {"color_1": "#A7D18F", "color_2": "#538235",
                       "color_3": "#93D14A", "color_4": "#03AE50",
                       "color_5": "#FCD96A", "color_6": "#FCC200",
                       "color_7": "#FFFF06", "color_8": "#C29300",
                       "color_9": "#9AC4EC", "color_10": "#3274B0",
                       "color_11": "#03AEF4", "color_12": "#0470B8",
                       "color_13": "#F1B382", "color_14": "#C60000",
                       "color_15": "#F70001" , "color_16": "#E66210",
                       "color_17": "#CC99FE", "color_18": "#990099",
                       "color_19": "#FF66FF", "color_20": "#CD0067",
                       "color_21": "#C9C9C9", "color_22": "#333E50",
                       "color_23": "#7C7C7C", "color_24": "#FFFFFF",
                       "color_25": "#03CA67", "color_26": "	#702DA8",
                       "color_27": "#F19B10", "color_28": "	#FFCCFC",
                       "color_29": "#009B97", "color_30": "#F11016",
                       "color_31": "#3A5627", "color_32": "#D0CECF",
                       "color_0": "#00FFFFFF"}

class Etiqueta(QLabel):
    def __init__(self, parent=None):
        super(Etiqueta, self).__init__(parent=parent)
        self.rastro = [[]]

    def paintEvent(self, e):
        paint = QPainter(self)
        paint.setPen(QPen(Qt.black, 3, Qt.SolidLine))

        for n in range(0, len(self.rastro), 2):
            x_prev, y_prev = self.rastro[n][0] if self.rastro[n] else (0, 0)
            for x, y in self.rastro[n]:
                paint.drawLine(x_prev, y_prev, x, y)
                x_prev, y_prev = x, y
        self.update()

class JuegoSignal(QObject):
    """Clase que se encargara de chequear la cuenta
    del contador."""

    avisar_teclas_listas = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()

        # Se conecta la señal check_signal con la función open_window del
        # parent (MainWindow).
        self.parent = parent
        self.avisar_teclas_listas.connect(parent)

class InicioChecker(QObject):
    """Clase que se encargara de chequear la cuenta del contador."""

    check_signal = pyqtSignal(bool)
    check_actualizar = pyqtSignal(tuple)

    def __init__(self, parent):
        super().__init__()

        # Se conecta la señal check_signal con la función open_window del
        # parent (MainWindow).
        self.parent = parent
        self.check_signal.connect(parent.comenzar)
        self.check_actualizar.connect(parent.comenzar)

    def check_ingresar(self, tupla):
        try:
            self.parent.cliente.send({"estado": "inicio_sesion",
                                      "contenido": tupla})

            while not self.parent.mensaje:
                pass
            respuesta = self.parent.mensaje
            self.parent.mensaje = ""
            if respuesta is True:
                '''
                if self.parent.espacio_error_inicio.isHidden():
                    self.parent.espacio_error_inicio.show()
                self.parent.text_error_inicio.setText("Usuario ingresado "
                                                      "con éxito :D")
                '''
                self.check_signal.emit(True)
            else:
                raise ErrorIngreso(respuesta)

        except ErrorIngreso as error:
            if self.parent.espacio_error_inicio.isHidden():
                self.parent.espacio_error_inicio.show()

            self.parent.text_error_inicio.setText(str(error) + "\nLo sentimos, "
                                         "puede intentarlo nuevamente :D")

            self.check_signal.emit(False)

    def check_registrar(self, tupla):
        print("entra a check")
        try:
            self.parent.cliente.send({"estado": "registro",
                                      "contenido": tupla})

            while not self.parent.mensaje:
                pass
            respuesta = self.parent.mensaje
            self.parent.mensaje = ""
            if respuesta is True:
                if self.parent.espacio_error_inicio.isHidden():
                    self.parent.espacio_error_inicio.show()
                self.parent.text_error_inicio.setText("Usuario registrado "
                                                      "con éxito :D")
                self.check_signal.emit(True)
            else:
                raise ErrorRegistro(respuesta)

        except ErrorRegistro as error:
            if self.parent.espacio_error_inicio.isHidden():
                self.parent.espacio_error_inicio.show()

            self.parent.text_error_inicio.setText(str(error) + "\nLo sentimos, "
                                         "puede intentarlo nuevamente :D")

            self.check_signal.emit(False)

    def check_mensaje_enviar(self, tupla):
        self.parent.cliente.send({"estado": "enviar_mensaje", "contenido":
            tupla})

    def check_actualizar_color(self, tupla):
        self.parent.cliente.send({"estado": "actualizar_color", "contenido":
                                  tupla})

    def check_agregar_invitado(self, tupla):
        self.parent.cliente.send({"estado": "agregar_invitado", "contenido":
            tupla})

    def check_iniciar_contador(self, numero):
        self.parent.cliente.send({"estado": "iniciar_contador", "contenido":
            numero})


    def check_seleccionar_partida(self, tupla):
        print("entra a backend")
        usuario, indice = tupla
        self.parent.cliente.send({"estado": "seleccionar_partida",
                                  "contenido": tupla})
        print("envió mensaje")
        while self.parent.mensaje is None:
            pass
        print("mensaje recibido")
        respuesta = self.parent.mensaje
        print(respuesta)
        self.parent.mensaje = None
        self.check_actualizar.emit((False, respuesta, "seleccionar"))

    def check_iniciar_juego(self):
        respuesta = self.parent.mensaje
        self.parent.mensaje = None
        self.check_actualizar.emit((True, True))


    def check_lista_partidas(self, tupla):
        print("backend")
        if tupla[0]:
            print("parte backend")
            self.parent.cliente.send({"estado": "actualizar_lista",
                                      "contenido": ""})
            print("envia3 desde el cliente")
            print("msj", self.parent.mensaje)
            print(self.parent)
            while self.parent.mensaje is None:
                pass
            print("msj", self.parent.mensaje)
            respuesta = self.parent.mensaje
            self.parent.mensaje = None
            print("RESPUESTA:", respuesta)
            self.check_actualizar.emit((True, respuesta))
        else:
            print("2 backend")
            self.parent.cliente.send({"estado": "nueva_partida",
                                      "contenido": tupla[1]})
            print("2 envia3 desde cliente")
            print("msj", self.parent.mensaje)
            while self.parent.mensaje is None:
                pass
            respuesta = self.parent.mensaje
            self.parent.mensaje = None
            self.check_actualizar.emit((False, respuesta, "nueva"))




class NumeroImagen:
    def __init__(self, inicio=1, final=4):
        self._numero = inicio
        self._start = inicio
        self._end = final

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, valor):
        if valor > self._end or valor < self._start:
            self._numero = self._start
        else:
            self._numero = valor




class Fondo(threading.Thread):
    """Este será nuestro nuevo Worker basado en Thread"""

    num = NumeroImagen()

    def __init__(self, window):
        # En el caso de los threads, lo primero es invocar al init original.
        super().__init__()
        self.window = window

        self.daemon = True

    def run(self):
        while self.window.state:
            Fondo.num.numero += 1
            imagen = QImage(f"{ruta_fondos}/imagen_{Fondo.num.numero}.png")
            #print("hola", Fondo.num.numero)
            fondo = imagen.scaled(QSize(640, 360))  # resize
            # Image to widgets size
            palette = QPalette()
            palette.setBrush(10, QBrush(fondo))  # 10 = Windowrole
            self.window.setPalette(palette)
            time.sleep(4)



def completar_numero(numero, maximo=2):
    if type(numero) == int:
        numero = str(numero)
    largo = len(numero)
    ceros = maximo - largo
    a_entregar = numero
    if ceros > 0:
        a_entregar = ("0" * ceros) + a_entregar
    return a_entregar

def extraer_numero(string):
    inicio = string.find("[")
    hasta = string.find("]")
    numero = int(string[inicio + 1: hasta])
    return numero

class Player(QObject):

    def __init__(self, parent, x, y, angulo, color):
        super().__init__()
        self.color = color
        self.direction = 'R'
        self._x = x
        self._y = y
        self.horizontal1 = (160, 621)
        self.vertical1 = (18, 338)
        self.suma = 10
        self.parent = parent
        self._angle = angulo
        self.camino = self.ruta()
        self.cambio_angulo = [False, 0, False]
        self.puntaje = 0


        # Se conecta la señal update_position con el metodo del parent
        # (MainGame.update_position)
        #self.update_position_signal.connect(parent.update_position)
        #avanzanding = Avanzar(self)
        #avanzanding.start()

    def __getstate__(self):
        nueva = {"_x": self.x, "_y": self.y, "_angle": self.angle, "color":
            self.color}
        # esto es lo que será serializado por pickle
        return nueva

    def __setstate__(self, state):
        self.__dict__ = state

    def __str__(self):
        return str(self.x) + str(self.y) + str(angulo) + str(color)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, valor):
        # innecesario, pero para no manejar números taaaaaaaaan grandes si se
        # dan demasiadas vueltas :D
        if valor >= 360:
            self._angle = valor - 360
        elif valor < 0:
            self._angle = 360 + valor
        else:
            self._angle = valor

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        """
        Envía la señal update_position al cambiar la coordenada y.
        :param value: int
        :return: none
        """
        if self.vertical1[0] - self.suma < value < self.vertical1[1] - \
                self.suma:
            self._y = value
            self.update_position_signal.emit({'x': round(self.x),
                                              'y': round(self.y)})

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        """
        Chequea que la coordenada x se encuentre dentro de los parámetros
        y envía la señal
        update_position con las nuevas coordenadas.
        :param value: int
        :return: none
        """
        if self.horizontal1[0] - self.suma < value < self.horizontal1[1] - \
                self.suma:
            self._x = value
            self.update_position_signal.emit({'x': round(self.x),
                                              'y': round(self.y)})

    def move(self, event):
        """
        Función que maneja los eventos de movimiento (L, R) y de salto.
        :param event: str
        :return: none
        """
        if event == 'R':
            # self.camino = puntos_circunferencia(self, 1)
            if self.cambio_angulo != [True, 1, False]:
                self.cambio_angulo = [True, 1, True]

        if event == 'L':
            # self.camino = puntos_circunferencia(self, -1)
            if self.cambio_angulo != [True, -1, False]:
                self.cambio_angulo = [True, -1, True]

        if event == 'U':
            if self.cambio_angulo != [False, 0, False]:
                self.cambio_angulo = [False, 0, True]


                # self.parent.mapa(self.x, self.y).setPixmap(self.rastro)

    def ruta(self, angle=None):
        angulo = angle if angle is not None else self.angle
        avanzar_x = cos(angulo)
        avanzar_y = sen(angulo)
        x_actual = self.x
        y_actual = self.y
        while self.horizontal1[0] <= x_actual <= self.horizontal1[1] and \
                                self.vertical1[0] <= y_actual <= self.vertical1[
                    1]:
            yield x_actual, y_actual
            x_actual += avanzar_x
            y_actual += avanzar_y


class Poder:
    def __init__(self, juego):
        self.x, self.y = random.randint(200, 600), random.randint(38, 310)
        self.tipo = random.sample(juego.poderes, 1)[0]

    def __getstate__(self):
        return {"x": self.x, "y": self.y, "tipo": self.tipo}

    def __setstate__(self, state):
        self.__dict__ = state

