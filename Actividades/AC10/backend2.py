# Acá va lo relacionado con el procesamiento de datos

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.Qt import QTest
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, \
        QLineEdit, QVBoxLayout


from random import randint
import math
import threading
import time

from PyQt5.QtGui import QPixmap, QTransform, QPainter, QBrush, QPen


p = 30  #radio


def cos(angulo):
    return math.cos(angulo * math.pi / 180)


def sen(angulo):
    return math.sin(angulo * math.pi / 180)


def puntos_circunferencia(jugador, orientacion):
    # izquierda -> angulo + 90 (centro)
    # derecha -> angulo - 90 (centro=
    angulo, x, y = jugador.angle, jugador.x, jugador.y
    angulo_centro = angulo - (90 * orientacion)
    print("ANGULOCENtRO", angulo_centro)
    centro = (x - (p * cos(angulo_centro)), y - (p * sen(angulo_centro)))
    print("CENTRO", centro, x, y)
    angle = angulo_centro + (1 * orientacion)

    print("ANGLE", angulo_centro, angle, angle - (90 * orientacion), x, y,
          centro)
    while angle != angulo_centro:
        x_new = centro[0] + (p * cos(angle))
        y_new = centro[1] + (p * sen(angle))
        yield x_new, y_new, angle + (90 * orientacion)
        angle += (1 * orientacion)
        print("ANGLE", angulo_centro, angle, angle - (90 * orientacion), x_new,
              y_new)



class UserChecker(QObject):
    """Clase que se encargara de chequear la cuenta del contador."""

    check_signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()

        # Se conecta la señal check_signal con la función open_window del
        # parent (MainWindow).
        self.check_signal.connect(parent.open_window)

    def check(self, booleano):

        """
        Función que chequea que la cuenta no supere 5. en el caso de superarlo,
         envia una señal
        True al frontend.
        :param count: str
        :return: none
        """
        if booleano:
            self.check_signal.emit(True)
        else:
            self.check_signal.emit(False)


class Objeto(QObject):
    def __init__(self,  parent, x, y):
        super().__init__()

class Character(QObject):

    update_position_signal = pyqtSignal(dict)

    def __init__(self,  parent, x, y):
        super().__init__()
        self.jumping = False
        self.direction = 'R'
        self._x = x
        self._y = y
        self.horizontal1 = (13, 550)
        self.vertical1 = (8, 603)
        self.suma = 10
        self.parent = parent
        self._angle = 0
        self.camino = self.ruta()
        self.rastro = QPixmap("verde.png").scaledToHeight(3).scaledToWidth(3)
        self.cambio_angulo = [False, 0, False]



        # Se conecta la señal update_position con el metodo del parent
        # (MainGame.update_position)
        self.update_position_signal.connect(parent.update_position)
        avanzanding = Avanzar(self)
        avanzanding.start()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, valor):
        #innecesario, pero para no manejar números taaaaaaaaan grandes si se
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
        print(event)
        if event == 'R':
            #self.camino = puntos_circunferencia(self, 1)
            if self.cambio_angulo != [True, 1, False]:
                print("AAAAH 0REINICIO", self.cambio_angulo)
                self.cambio_angulo = [True, 1, True]

        if event == 'L':
            #self.camino = puntos_circunferencia(self, -1)
            if self.cambio_angulo != [True, -1, False]:
                self.cambio_angulo = [True, -1, True]


        if event == 'U':
            if self.cambio_angulo != [False, 0, False]:
                self.cambio_angulo = [False, 0, True]


        #self.parent.mapa(self.x, self.y).setPixmap(self.rastro)

    def ruta(self, angle=None):
        print("ingreso a ruta")
        angulo = angle if angle is not None else self.angle
        avanzar_x = cos(angulo)
        avanzar_y = sen(angulo)
        x_actual = self.x
        y_actual = self.y
        print("listo")
        while self.horizontal1[0] <= x_actual <= self.horizontal1[1] and \
                self.vertical1[0] <= y_actual <= self.vertical1[1]:
            print(f"ang {angulo}, x {int(x_actual)}, y {int(y_actual)}, "
                  f"a_x {avanzar_x}, a_y {avanzar_y}")
            print()
            yield x_actual, y_actual
            x_actual += avanzar_x
            y_actual += avanzar_y


    def jump(self):
        """
        Función que ejecuta el salto del personaje.
        :return: none
        """
        if self.y > 484:
            for i in range(10):
                self.y -= (i * 5)
                QTest.qWait(30)
            for i in range(10):
                self.y += (i * 5)
                QTest.qWait(30)


class Avanzar(threading.Thread):
    """Este será nuestro nuevo Worker basado en Thread"""

    def __init__(self, player, orientacion=0):
        # En el caso de los threads, lo primero es invocar al init original.
        super().__init__()
        self.player = player
        self.n = orientacion

        self.daemon = True

    def run(self):
        while True:
            if not self.player.cambio_angulo[0]:
                print("ENTRAMOS A EL OTRO JEJE")
                if self.player.cambio_angulo[2]:
                    print("VA A EMPEZaR RUtA")
                    self.player.camino = self.player.ruta()
                    self.player.cambio_angulo[2] = False
                print(self.player.parent)
                self.player.parent.frame += 1
                self.player.parent.front_character.setPixmap(QPixmap(
                    f'sprites/pacman_R_{self.player.parent.frame}.png').transformed(
                    QTransform().rotate(self.player.angle)))
                self.player.x, self.player.y = next(self.player.camino)
                bloque = self.player.parent.mapa(self.player.x, self.player.y)
                '''
                if bloque[0].isHidden():
                    print(bloque[0])
                    print(bloque[0].isHidden())
                    print(bloque[0].pixmap())
                    print(self.player.x, self.player.y)
                    print(bloque[0].x(), bloque[0].y())
                    print(bloque[0].width(), bloque[0].height())
    
                    label = QLabel(self.player.parent)
                    label.setPixmap(QPixmap("claro.png"))
                    label.move(30, 30)
                    label.resize(20, 20)
                    print("a_mostrado")
                    print("mostrado")
    
    
                    print("jeje")
                '''

                time.sleep(0.01)
            elif self.player.cambio_angulo[0]:
                if self.player.cambio_angulo[2]:
                    print("reinicio")
                    self.player.camino = puntos_circunferencia(self.player,
                                    self.player.cambio_angulo[1])
                    self.player.cambio_angulo[2] = False
                self.player.parent.frame += 1

                self.player.x, self.player.y, self.player.angle = next(
                    self.player.camino)
                print("NUEVO", self.player.x, self.player.y, self.player.angle)
                self.player.parent.front_character.setPixmap(QPixmap(
                    f'sprites/pacman_R_{self.player.parent.frame}.png').transformed(
                    QTransform().rotate(self.player.angle)))
                bloque = self.player.parent.mapa(self.player.x, self.player.y)

                '''
                self.player.angle += (10 * self.player.cambio_angulo[1])
                self.player.camino = self.player.ruta()
                self.player.parent.frame += 1
                self.player.parent.front_character.setPixmap(QPixmap(
                    f'sprites/pacman_R_{self.player.parent.frame}.png').transformed(
                    QTransform().rotate(self.player.angle)))
                for i in range(1):
                    print("AAAAAAAH", self.player.x, self.player.y)
                    next(self.player.camino)
                    self.player.x, self.player.y = next(self.player.camino)
                    print("AAAAAAAH", self.player.x, self.player.y)
                    bloque = self.player.parent.mapa(self.player.x,
                                                     self.player.y)
                '''
                time.sleep(0.001)

                # rango 10 y timesleep 0.01, 1 grado -> diametro = 818.267717
                # radio = 409,1338585
                # rango 10 y timesleep 0.01, 2 grados -> diametro = 442.204724
                # radio = 221.102362
                # 3 grados -> diametro = 326.551181
                # radio = 163.2755905
            else:
                pass



class CambiarAngulo(threading.Thread):
    def __init__(self, player, orientacion):
        super().__init__()
        self.player = player
        self.n = orientacion

        self.daemon = True

    def run(self):
        while self.player.cambio_angulo:
            self.player.angle += (1 * self.n)
            self.player.camino = self.player.ruta()
            self.player.parent.frame += 1
            self.player.parent.front_character.setPixmap(QPixmap(
                f'sprites/pacman_R_{self.player.parent.frame}.png').transformed(
                QTransform().rotate(self.player.angle)))
            for i in range(3):
                self.player.x, self.player.y = next(self.player.camino)

