# Acá va lo relacionado con el procesamiento de datos

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.Qt import QTest
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, \
        QLineEdit, QVBoxLayout


from random import randint
import math
import threading
import time
import random
from datetime import datetime, timedelta
from parameters import parametros as par
from excepciones import Choque

from PyQt5.QtGui import QPixmap, QTransform, QPainter, QBrush, QPen

def cos(angulo):
    return math.cos(angulo * math.pi / 180)


def sen(angulo):
    return math.sin(angulo * math.pi / 180)


def puntos_circunferencia(jugador, orientacion):
    # izquierda -> angulo + 90 (centro)
    # derecha -> angulo - 90 (centro=
    angulo, x, y = jugador.angle, jugador.x, jugador.y
    angulo_centro = angulo - (90 * orientacion)
    centro = (x - (p * cos(angulo_centro)), y - (p * sen(angulo_centro)))
    angle = angulo_centro + (1 * orientacion)

    while angle != angulo_centro:
        x_new = centro[0] + (p * cos(angle))
        y_new = centro[1] + (p * sen(angle))
        yield x_new, y_new, angle + (90 * orientacion)
        angle += (1 * orientacion)
p = 30  #radio


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
        self.rastro = [[]]
        self.marcando = True
        self.choco = False
        self.puntaje = 0
        self.avanzanding = Avanzar(self)

    def activar_poder(self, poder):
        if int(poder.tipo) == 1:
            pass
        elif int(poder.tipo) == 2:
            pass


    def __getstate__(self):
        nueva = {"_x": self.x, "_y": self.y, "_angle": self.angle, "color":
            self.color, "rastro": self.rastro, "choco": self.choco,
                 "puntaje": self.puntaje}
        # esto es lo que será serializado por pickle
        return nueva

    def __setstate__(self, state):
        self.__dict__ = state

    def __str__(self):
        return str(self.x) + str(self.y) + str(self.angle) + str(self.color)

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
         #   self.update_position_signal.emit({'x': round(self.x),
          #                                    'y': round(self.y)})

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
        #    self.update_position_signal.emit({'x': round(self.x),
         #                                     'y': round(self.y)})

    def move(self, event):
        """
        Función que maneja los eventos de movimiento (L, R) y de salto.
        :param event: str
        :return: none
        """
        print("CAMBIANDO ANGULO", event)
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



def ruta(x, y, angle, horizontal, vertical, posiciones_guardadas):
    angulo = angle if angle is not None else self.angle
    avanzar_x = cos(angulo)
    avanzar_y = sen(angulo)
    x_actual = x
    y_actual = y
    while horizontal[0] <= x_actual <= horizontal[1] and \
                            vertical[0] <= y_actual <= vertical[1] and (
            x_actual, y_actual) not in posiciones_guardadas:
        yield x_actual, y_actual
        x_actual += avanzar_x
        y_actual += avanzar_y

class Poder:
    def __init__(self, juego):
        self.x, self.y = random.randint(200, 600), random.randint(38, 310)
        self.tipo = random.sample(juego.poderes, 1)[0]
        self.retiro = datetime.now() + timedelta(seconds=6)

    @property
    def habilitado(self):
        return datetime.now() <= self.retiro

    def __getstate__(self):
        return {"x": self.x, "y": self.y, "tipo": self.tipo}

    def __setstate__(self, state):
        self.__dict__ = state


class EnviarMapa(threading.Thread):
    """Este será nuestro nuevo Worker basado en Thread"""

    def __init__(self, servidor, juego):
        # En el caso de los threads, lo primero es invocar al init original.
        super().__init__()
        self.juego = juego
        self.servidor = servidor
        self.daemon = True

        self.mostrar_poder = datetime.now() + timedelta(seconds=random.uniform(
            5, 10))

    def run(self):
        while True:
            if not self.juego.pausa:
                if datetime.now() >= self.mostrar_poder:
                    self.mostrar_poder = datetime.now() + timedelta(
                        seconds=random.uniform(5, 10))
                    poder = Poder(self.juego)
                    self.juego._lista_poderes.append(poder)


                try:
                    for _socket in self.juego.jugadores_sockets:
                        print("enviando señal:")
                        self.servidor.send_pickle({"estado": "actualizar_mapa",
                                            "contenido": self.juego}, _socket)
                        time.sleep(0.01)
                except RuntimeError:
                    pass

class Avanzar(threading.Thread):
    """Este será nuestro nuevo Worker basado en Thread"""

    def __init__(self, player, orientacion=0):
        # En el caso de los threads, lo primero es invocar al init original.
        super().__init__()
        self.player = player
        self.n = orientacion
        self.estado = "inicio"
        self.marcando = 0
        self.no_marcando = 0
        self.marcando_hasta = 0
        self.no_marcando_hasta = 0

        self.daemon = True

    def run(self):
        self.marcando = random.uniform(0, par.t)
        self.estado = "marcando"
        self.marcando_hasta = datetime.now() + timedelta(
            seconds=self.marcando)
        while True:
            if not self.player.parent.pausa:
                try:
                    if self.estado == "marcando" and \
                                    datetime.now() >= self.marcando_hasta:
                        self.no_marcando = random.uniform(0, par.d)
                        self.estado = "no_marcando"
                        self.no_marcando_hasta = datetime.now() + timedelta(
                            seconds=self.no_marcando)
                        self.player.rastro.append([])
                        self.player.marcando = False if self.player.marcando else \
                            True
        #                self.player.fondo.rastro.append([])

                    elif self.estado == "no_marcando" and \
                                    datetime.now() >= self.no_marcando_hasta:
                        self.marcando = random.uniform(0, par.t)
                        self.estado = "marcando"
                        self.marcando_hasta = datetime.now() + timedelta(
                            seconds=self.marcando)
                        self.player.rastro.append([])
                        self.player.marcando = False if self.player.marcando else \
                            True
               #         self.player.fondo.rastro.append([])

                    if not self.player.cambio_angulo[0]:
                        if self.player.cambio_angulo[2]:
                            self.player.camino = self.player.ruta()
                            self.player.cambio_angulo[2] = False

                        self.player.x, self.player.y = next(self.player.camino)
                        if len(set(cuadrado(self.player.x, self.player.y)) &
                                set(primeros(self.player.parent.marcados))):
                            print("CHOCÖ :O")
                            raise Choque(str(self.player.x) + str(self.player.y))
                        diccionario_poderes = \
                            self.player.parent.posiciones_poderes
                        if (self.player.x, self.player.y) in \
                                diccionario_poderes:
                            poder = diccionario_poderes((self.player.x,
                                                         self.player.y))
                            self.player.parent._lista_poderes.remove(poder)
                            self.player.activar_poder(poder)

                        self.player.rastro[-1].append((int(self.player.x),
                                                           int(self.player.y)))
                        if self.player.marcando:
                            self.player.parent.marcados.append((int(self.player.x),
                                                            int(self.player.y)))
        #                bloque = self.player.parent.mapa(self.player.x, self.player.y)

                        time.sleep(0.01)
                    elif self.player.cambio_angulo[0]:
                        if self.player.cambio_angulo[2]:
                            self.player.camino = puntos_circunferencia(self.player,
                                                            self.player.cambio_angulo[
                                                                           1])
                            self.player.cambio_angulo[2] = False


                        self.player.x, self.player.y, self.player.angle = next(
                            self.player.camino)

                        if len(set(cuadrado(self.player.x, self.player.y)) &
                                set(primeros(self.player.parent.marcados))):
                            print("CHOCÖ :O")
                            raise Choque(str(self.player.x) + str(self.player.y))
                        diccionario_poderes = \
                            self.player.parent.posiciones_poderes
                        if (self.player.x, self.player.y) in \
                                diccionario_poderes:
                            poder = diccionario_poderes((self.player.x,
                                                         self.player.y))
                            self.player.parent._lista_poderes.remove(poder)
                            self.player.activar_poder(poder)
                        self.player.rastro[-1].append((int(self.player.x),
                                                       int(self.player.y)))
                        if self.player.marcando:
                            self.player.parent.marcados.append((int(self.player.x),
                                                                int(self.player.y)))

                  #      bloque = self.player.parent.mapa(self.player.x, self.player.y)

                        time.sleep(0.001)

                        # rango 10 y timesleep 0.01, 1 grado -> diametro = 818.267717
                        # radio = 409,1338585
                        # rango 10 y timesleep 0.01, 2 grados -> diametro = 442.204724
                        # radio = 221.102362
                        # 3 grados -> diametro = 326.551181
                        # radio = 163.2755905
                    else:
                        pass
                except StopIteration:
                    self.player.choco = True


def cuadrado(x, y):
    lista = []
    x, y = int(x), int(y)
    for i in (x - 1, x, x + 1):
        for j in (y - 1, y, y + 1):
            lista.append((i, j))
    return lista


def cuadrado2(x, y):
    lista = []
    x, y = int(x), int(y)
    for i in range(28):
        for j in range(28):
            lista.append((x + i, y + j))
    return lista

def primeros(lista, ultimos=10):
    if len(lista) < ultimos:
        return []
    return lista[:-1 * ultimos]

