# Acá va lo relacionado con el procesamiento de datos

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.Qt import QTest
from random import randint




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

        # Se conecta la señal update_position con el metodo del parent
        # (MainGame.update_position)
        self.update_position_signal.connect(parent.update_position)

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
            self.update_position_signal.emit({'x': self.x, 'y': self.y})

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
            self.update_position_signal.emit({'x': self.x, 'y': self.y})

    def move(self, event):
        """
        Función que maneja los eventos de movimiento (L, R) y de salto.
        :param event: str
        :return: none
        """
        if event == 'R':
            self.x += 10
            self.direction = 'R'
        if event == 'L':
            self.x -= 10
            self.direction = 'L'
        if event == 'U':
            self.y -= 10
            self.direction = 'U'
        if event == 'D':
            self.y += 10
        if event == "E":
            self.parent.agregar_guinda()

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


