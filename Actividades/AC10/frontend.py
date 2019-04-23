# Acá va lo relacionado con la GUI.


'''
Casi toda la actividad está basada en la ayudantía de Interfaces gráficas
del ramo :D
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, \
        QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap, QTransform

from PyQt5.QtGui import QImage, QPalette, QBrush, QPainter, QPen

from PyQt5.QtCore import QObject, pyqtSignal, Qt, QSize
from backend2 import UserChecker, Character




#https://stackoverflow.com/questions/43454882/paint-over-qlabel-with-pyqt
class Etiqueta(QLabel):
    def __init__(self, parent=None):
        super(Etiqueta, self).__init__(parent=parent)
        self.rastro = []

    def paintEvent(self, e):
        paint = QPainter(self)
        paint.setPen(QPen(Qt.black, 3, Qt.SolidLine))

        x_prev, y_prev = 0, 0
        for x, y in self.rastro:
            paint.drawLine(x_prev, y_prev, x, y)
            x_prev, y_prev = x, y
        self.update()



class MainWindow(QWidget):

    check_condiciones_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 300, 200)

        self.aprueba = False

        self.name_label = QLabel('A continuación puede ingresar su nombre de '
                                 'usuario\nRequisistos de nombre:\n*Sólo '
                                 'letras.\n*Largo mayor a 6 :D',
                                 self)

        self.edit = QLineEdit('', self)
        self.edit.setGeometry(10, 80, 280, 20)

        self.mensaje = ""
        self.main_game_button = QPushButton('Ingresar', self)
        self.ingresar_label = QLabel(self.mensaje, self)

        # Se conecta el boton con la función check_count
        self.main_game_button.clicked.connect(self.check_condiciones)

        # Se Instancia el CountChecker.
        self.spell_checker = UserChecker(self)
        self.check_condiciones_signal.connect(self.spell_checker.check)

        vbox = QVBoxLayout()
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.ingresar_label)
        vbox.addWidget(self.main_game_button)
        self.setLayout(vbox)

    def check_condiciones(self):
        """
        Función que incrementa el contador y envía una señal al CheckCount con
        la cuenta.
        También actualiza el label del contador.
        :return: none
        """
        ingresado = str(self.edit.text())


        if len(ingresado) > 6 and not False in [i.isalpha() for i in
                                               ingresado]:
            self.mensaje = "Usuario válido :D ¡Comencemos el juego!"
            self.aprueba = True
        else:
            self.mensaje = "Usuario inválido u.u, lo sentimos :o"
            self.aprueba = False
        self.ingresar_label.setText(str(self.mensaje))
        self.check_condiciones_signal.emit(self.aprueba)

    def open_window(self, state):
        """
        Función que dado un estado, cambia la ventana de inicio por la del
        juego.
        :param state: bool
        :return: none
        """
        if state:
            self.hide()
            self.main_game = MainGame()
            self.main_game.show()


class MainGame(QWidget):

    move_character_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.dimensiones = (560, 615)
        self.ancho = 560
        self.alto = 615
        self.grupo_pixeles = 3
        self.setGeometry(0, 0, 560, 615)
        self.guindas = dict()
        self._frame = 1
        self.ides = 0
        self.x_new = 0
        self.y_new = 0
        self.rastro = []


        # Se setea la imagen de fondo.
    #    self.background = QLabel(self)
     #   self.background.setPixmap(QPixmap('sprites/map.png'))

        print("antes mapa")

        self._mapa = dict()
        #self.pixeles_anteriores = (n for n in range(self.grupo_pixeles // 2))
        #self.pixeles_posteriores = (n for n in range(self.grupo_pixeles // 2))
        for i in range(self.grupo_pixeles // 2, self.ancho, self.grupo_pixeles):
            self._mapa[i] = dict()
            for j in range(self.grupo_pixeles // 2, self.alto,
                                            self.grupo_pixeles):

                self._mapa[i][j] = [None, False]
               # self._mapa[i][j].move(i - self.grupo_pixeles // 2,
                #                      j - self.grupo_pixeles // 2)

        print("después mapa")


        # Se instancia el personaje del backend y se conecta move_character_
        # signal con la función


        self.fondo_jugador = Etiqueta(self)
        self.fondo_jugador.resize(self.alto, self.ancho)


        # Se crea el personaje en el frontend.
        self.front_character = QLabel(self)
        self.front_character.setPixmap(QPixmap('sprites/pacman_R_2.png'))
        self.front_character.move(13, 8)


        # move de Character.
        self.backend_character = Character(self, 13, 8)
        print("crea3")
        self.move_character_signal.connect(self.backend_character.move)

        print("jugador creado")


        print("creado")

    def agregar_guinda(self):
        self.guindas[self.ides] = Objeto(self, randint(50, 500), randint(50,
                                                                        550))

        # Se crea el personaje en el frontend.
        self.guindas[self.ides + 1] = QLabel(self)
        self.guindas[self.ides + 1].setPixmap(QPixmap('sprites/cherry.png'))
        self.ides += 2

    def mapa(self, x, y):
        grupo_pixeles = self.grupo_pixeles
        x_new = ((x // grupo_pixeles) * grupo_pixeles) + grupo_pixeles // 2
        y_new = ((y // grupo_pixeles) * grupo_pixeles) + grupo_pixeles // 2

        bloque = self._mapa[x_new][y_new]

        self.x_new, self.y_new = x_new, y_new
        self.rastro.append((x, y))
        self.fondo_jugador.rastro.append((x, y))
        self.fondo_jugador.update()

        if bloque[1]:
            print("chocó")
        else:
            if bloque[0] is None:
                #print(f"pintando {x_new}, {y_new}")
                '''
                bloque[0] = QLabel(self)

                imagen = QImage("verde.png")
                fondo = imagen.scaled(QSize(10, 10))  # resize
                # Image to widgets size
                palette = QPalette()
                palette.setBrush(10, QBrush(fondo))  # 10 = Windowrole
                bloque[0].setPalette(palette)



                #bloque[0].setPixmap(QPixmap("verde.png"))
                bloque[0].move(x_new - (grupo_pixeles // 2), y_new -
                               (grupo_pixeles // 2))

                bloque[0].resize(grupo_pixeles, grupo_pixeles)
                                  #  .scaledToHeight(10).scaledToWidth(10))
                '''
                '''
                bloque[0] = QPainter(self)
                bloque[0].setPen(QPen(Qt.black, 10, Qt.SolidLine))

                bloque[0].drawLine(0, 0, x_new, y_new)
                self.paintEvent(bloque[0])
                '''




                bloque[1] = True


        return self._mapa[x_new][y_new]


    def ppaintEvent(self, e):
        paint = QPainter(self.fondo_jugador)
        paint.setPen(QPen(Qt.black, 10, Qt.SolidLine))

        x_prev, y_prev = 0, 0
        for x, y in self.rastro:
            paint.drawLine(x_prev, y_prev, x, y)
            x_prev, y_prev = x, y
        self.update()

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value > 3:
            self._frame = 1
        else:
            self._frame = value

    def keyPressEvent(self, e):
        """
        Dada la presión de una tecla se llama a esta función. Al apretarse
        una tecla chequeamos si
        esta dentro de las teclas del control del juego y de ser así, se
        envía una señal al backend
        con la acción además de actualizar el sprite.
        :param e: QKeyEvent
        :return:
        """

        #self.frame += 1
        if e.key() == Qt.Key_D:
            self.front_character.setPixmap(QPixmap(
                f'sprites/pacman_R_{self.frame}.png').transformed(
                QTransform().rotate(self.backend_character.angle + 1)))
            self.move_character_signal.emit('R')
        if e.key() == Qt.Key_A:
            self.front_character.setPixmap(QPixmap(
                f'sprites/pacman_R_{self.frame}.png').transformed(
                QTransform().rotate(self.backend_character.angle - 1)))
            self.move_character_signal.emit('L')
        if e.key() == Qt.Key_Up:
            self.front_character.setPixmap(QPixmap(
                f'sprites/pacman_R_{self.frame}.png').transformed(
                QTransform().rotate(self.backend_character.angle)))
            self.move_character_signal.emit('U')
        if e.key() == Qt.Key_Down:
            self.front_character.setPixmap(QPixmap(
                f'sprites/pacman_D_{self.frame}.png'))
            self.move_character_signal.emit('D')
        if e.key() == Qt.Key_Space:
            self.move_character_signal.emit('E')

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_D and not e.isAutoRepeat():
            self.move_character_signal.emit('U')
        if e.key() == Qt.Key_A and not e.isAutoRepeat():
            self.move_character_signal.emit('U')


    def update_position(self, event):
        """
        Función que recibe un diccionario con las cordenadas del personaje y las actualiza en el
        frontend.
        :param event: dict
        :return: none
        """
        self.front_character.move(event['x'], event['y'])


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()