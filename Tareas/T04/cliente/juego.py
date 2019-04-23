import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QListWidget, QScrollBar, \
    QWidget, QListWidgetItem, QPushButton, QMainWindow, QFrame
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush, QMovie, \
    QPainter, QTransform, QPen, QColor
from PyQt5.QtCore import QSize, QObject, pyqtSignal, Qt, QTimer

from backend import NumeroImagen, Fondo, InicioChecker, ruta_colores,\
    ruta_imagenes, completar_numero, extraer_numero, ruta_sprites, \
    diccionario_colores, ruta_fondos, ruta_gifs, Poder
import time
from excepciones import VolverMenu
import itertools

class Etiqueta(QLabel):
    def __init__(self, parent=None):
        super(Etiqueta, self).__init__(parent=parent)
        self.rastro = [[]]
        self.pen = QPen(QColor("#FFFFFF"), 3, Qt.SolidLine)
        self.cuadro = QPixmap()


    def paintEvent(self, e):
        paint = QPainter(self)
        paint.setPen(self.pen)

        for n in range(0, len(self.rastro), 2):
            x_prev, y_prev = self.rastro[n][0] if self.rastro[n] else (0, 0)
            for x, y in self.rastro[n]:
                paint.drawLine(x_prev + 14, y_prev + 14, x + 14, y + 14)
                x_prev, y_prev = x, y
        self.update()

class Juego:
    def __init__(self, partida, datos_jefe):
        self.partida = partida.datos()
        self.datos_jefe = datos_jefe

game_name, game_class = uic.loadUiType("game.ui")

class Game(game_name, game_class):
    move_character_signal = pyqtSignal(str)
    move_guest_signal = pyqtSignal(str)

    def __init__(self, cliente="", sala_espera=""):
        super().__init__()

        self.cliente = cliente
        self.sala = sala_espera

        self.jugador_nombre = self.sala.usuario
        self.invitado_nombre = self.sala.invitado

        self.setupUi(self)
        self.game_zone.setPixmap(QPixmap(f"{ruta_fondos}/mapa_black.png"))
        self.mostrar_botones_elegir()
        self.boton_marcado = None
        self.keyPressEvent = self.elegir_teclas
        self.text_esperando.hide()
        self.fondo_elegir_teclas.setPixmap(QPixmap(f"{ruta_colores}/claro.png"))
        self.button_listo_teclas.clicked.connect(self.teclas_listas)
        imagen = QImage(f"{ruta_fondos}/fondo_juego.png")
        fondo = imagen.scaled(QSize(640, 360))  # resize
        palette = QPalette()
        palette.setBrush(10, QBrush(fondo))  # 10 = Windowrole
        self.setPalette(palette)
        self.cargando = QMovie(f"{ruta_gifs}/Nyancat.gif")
        self.cargando.setScaledSize(QSize(200, 200))
        self.paintEvent = self.mostrar_gif
        self.cargando.frameChanged.connect(self.repaint)
        self.nombres_puntajes = [(self.text_jugador_1, self.text_puntaje_1),
                                 (self.text_jugador_2, self.text_puntaje_2),
                                 (self.text_jugador_3, self.text_puntaje_3),
                                 (self.text_jugador_4, self.text_puntaje_4)]
        


        self.grupo_juego.hide()
        print("MOSTRADO GAME")
        self.juego = None
        self.jugadores_label = dict()
        print("jugadores labels listos")
        self.lista_labels = [self.label_1, self.label_2, self.label_3,
                             self.label_4]
        print("labels listos")
     #   self.lista_etiquetas = [Etiqueta(self), Etiqueta(self), Etiqueta(
      #      self), Etiqueta(self)]
        print("jeje")
        self.jugadores_etiquetas = dict()
     #   for etiqueta in self.lista_etiquetas:
      #      etiqueta.resize(630, 350)
       #     etiqueta.hide()
        print("etiquetas listas")
        self._mapa = dict()
        for x in range(150, 640, 3):
            for y in range(21, 360, 3):
                label = QLabel(self)
                label.move(x, y)
                label.resize(3 * 2, 3 * 2)
                self._mapa[(x + 1, y + 1)] = label
                self._mapa[(x + 1, y + 1)].hide()
                print("agregado:", x+1, y+1)
        self.button_pausa.clicked.connect(self.pausar)

        self.button_salir.clicked.connect(self.volver_menu)

        self.label_poderes = {self.label_poder_1: False, self.label_poder_2:
            False, self.label_poder_3: False, self.label_poder_4: False}

    def pausar(self):
        self.move_character_signal.emit('E')

    def volver_menu(self):
        self.hide()
        self.cliente.restart()

    def mapa(self, x, y):
        grupo_pixeles = 3
        tamaño_pixeles = 6
        x_new = ((x // grupo_pixeles) * grupo_pixeles) + grupo_pixeles // 2
        y_new = ((y // grupo_pixeles) * grupo_pixeles) + grupo_pixeles // 2
        return self._mapa[(int(x_new), int(y_new))]

    def pintar(self, x, y, color):
        a_pintar = self.mapa(x, y)
        a_pintar.setStyleSheet(f"background-color:{color}")
        if a_pintar.isHidden():
            a_pintar.show()


    def mover(self, event):
        self.cliente.send({"estado": "mover", "contenido": event})

    def mover_invitado(self, event):
        self.cliente.send({"estado": "mover_invitado", "contenido": event})

    def _keyPressEvent(self, e):
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
        if e.key() == self.botones_elegidos["JR"]:
            self.move_character_signal.emit("R")
        if e.key() == self.botones_elegidos["JL"]:
            self.move_character_signal.emit("L")
        if e.key() == self.botones_elegidos["IR"]:
            self.move_guest_signal.emit("R")
        if e.key() == self.botones_elegidos["IL"]:
            self.move_guest_signal.emit("L")
        if e.key() == Qt.Key_Space:
            self.move_character_signal.emit('E')

    def _keyReleaseEvent(self, e):
        if e.key() == self.botones_elegidos["JR"] and not e.isAutoRepeat():
            self.move_character_signal.emit('U')
        if e.key() == self.botones_elegidos["JL"] and not e.isAutoRepeat():
            self.move_character_signal.emit('U')
        if e.key() == self.botones_elegidos["IR"] and not e.isAutoRepeat():
            self.move_character_signal.emit('U')
        if e.key() == self.botones_elegidos["IL"] and not e.isAutoRepeat():
            self.move_character_signal.emit('U')

    def mostrar(self):
        self.show()



    def comenzar_juego(self):
        self.grupo_elegir_teclas.hide()
        self.fondo_elegir_teclas.hide()
        self.text_esperando.hide()
        self.grupo_juego.show()

    def mostrar_jugadores(self, juego):
        self.juego = juego
        self.text_puntaje_max.setText(f"Puntaje Máximo: "
                                      f"{self.juego.puntaje_max}")
        for jugadores, casillas in zip(self.juego.players.items(),
                                  self.nombres_puntajes):
            nombre, player = jugadores
            cuadro, cuadro_puntaje = casillas
            if nombre == self.jugador_nombre:
                self.jugador = player
            elif nombre == self.invitado_nombre:
                self.invitado = player
            label = self.lista_labels.pop(0)
            label.setPixmap(QPixmap(f"{ruta_sprites}/color_"
                                    f"{player.color}.png").scaledToWidth(
                                    6).scaledToHeight(6).transformed(
                                    QTransform().rotate(player.angle)))
            label.move(player.x, player.y)
      #      self.jugadores_etiquetas[nombre] = self.lista_etiquetas.pop(0)
       #     self.jugadores_etiquetas[nombre].pen = QPen(QColor(
        #        diccionario_colores[f"color_{player.color}"]), 3, Qt.SolidLine)
         #   self.jugadores_etiquetas[nombre].show()
            self.jugadores_label[nombre] = label
            self.keyPressEvent = self._keyPressEvent
            self.keyReleaseEvent = self._keyReleaseEvent

            self.move_character_signal.connect(self.mover)
            self.move_guest_signal.connect(self.mover_invitado)
            cuadro.setText(nombre)
            color = diccionario_colores[f"color_{player.color}"]
            cuadro.setStyleSheet(f"background-color: {color}")
            cuadro_puntaje.setText(str(player.puntaje))


    def actualizar_mapa(self, juego):
        self.juego = juego
        for nombre, player in self.juego.players.items():
            label = self.jugadores_label[nombre]
            if player.choco:
                label.hide()
            else:
                label.setPixmap(QPixmap(f"{ruta_sprites}/color_"
                                    f"{player.color}.png").scaledToWidth(
                                    6).scaledToHeight(6).transformed(
                                    QTransform().rotate(player.angle)))
            label.move(player.x, player.y)
            if len(player.rastro) % 2:
                self.pintar(player.x, player.y, diccionario_colores[
                                                f"color_{player.color}"])

        for poder, label_poder in itertools.zip_longest(
                self.juego.lista_poderes, self.label_poderes):
            if poder is not None:
                label_poder.move(poder.x, poder.y)
                label_poder.setPixmap(QPixmap(f"{ruta_sprites}/poder_"
                                    f"{poder.tipo}.png").scaledToWidth(
                                    12).scaledToHeight(12))
                if label_poder.isHidden():
                    label_poder.show()
            else:
                if not label_poder.isHidden():
                    label_poder.hide()


            #self.jugadores_etiquetas[nombre].rastro = player.rastro




    def _paintEvent(self, event):
        currentFrame = self.cargando.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    def mostrar_gif(self, event):
        '''https://stackoverflow.com/questions/
        41709464/python-pyqt-add-background-gif'''

        currentFrame = self.cargando.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(220, 90, currentFrame)


    def teclas_listas(self):
        self.grupo_elegir_teclas.hide()
        self.text_esperando.show()
        if self.sala.n_invitado:
            self.cliente.send({"estado": "teclas_listas", "contenido": (
                self.sala.usuario, self.sala.invitado)})
        else:
            self.cliente.send({"estado": "teclas_listas", "contenido": (
                self.sala.usuario,)})

        self.cargando.start()


    def eventFilter(self, source, event):
        return super(Game, self).eventFilter(source, event)

    def mostrar_botones_elegir(self):
        botones_elegir = (self.button_izquierda_jugador,
                          self.button_derecha_jugador,
                          self.button_izquierda_invitado,
                          self.button_derecha_invitado)
        botones_elegir_nombres = ("JL", "JR", "IL", "IR")
        self.botones_elegir = dict({boton: nombre for boton, nombre in zip(
            botones_elegir, botones_elegir_nombres)})
        self.botones_elegidos = {"JL": 16777234, "JR": 16777236,
                                "IL": 65, "IR": 68}
        for boton in botones_elegir:
            '''https://stackoverflow.com/questions/
            24925631/disable-pyqt-arrow-key-focus'''
            boton.setFocusPolicy(Qt.NoFocus)
            boton.clicked.connect(self.marcar_boton_elegir)
        self.button_listo_teclas.setFocusPolicy(Qt.NoFocus)


    def marcar_boton_elegir(self):
        boton = self.sender()
        self.boton_marcado = boton

    def elegir_teclas(self, e):
        '''http://www.naturalprogramming.com/pythonqt/KeyboardInputDemoQt.py'''
        if self.boton_marcado is not None and e.key() not in \
                self.botones_elegidos.values():
            numero_tecla = e.key()
            if numero_tecla < 256:
                string_tecla = "%c" % numero_tecla
            elif e.key() == Qt.Key_Up:
                string_tecla = "Up"
            elif e.key() == Qt.Key_Down:
                string_tecla = "Down"
            elif e.key() == Qt.Key_Left:
                string_tecla = "Left"
            elif e.key() == Qt.Key_Right:
                string_tecla = "Right"
            else:
                return
            self.botones_elegidos[
                self.botones_elegir[self.boton_marcado]] = e.key()
            self.boton_marcado.setText(string_tecla)



class MainWindow2(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow2, self).__init__(parent)
        self.setGeometry(50, 50, 600, 750)
        self.setFixedSize(600, 750)
        '''
        self.movie = QMovie("imagenes/gifs/rafita.gif")
        self.paintEvent = self._paintEvent
        print(self.repaint, QMainWindow.repaint)
        self.movie.frameChanged.connect(self.repaint)
        
        '''
        self.startUIWindow()

    def startUIWindow(self):
        self.Window = UIWindow(self)
        self.setWindowTitle("My Program")
        self.show()

    def _paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

class UIWindow(QWidget):

    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        self.resize(QSize(600, 750))
        self.ToolsBTN = QPushButton('tab', self)
        self.ToolsBTN.resize(100, 40)
        self.ToolsBTN.move(60, 300)

        self.CPS = QPushButton('tab1', self)
        self.CPS.resize(100, 40)
        self.CPS.move(130, 600)

        self.Creator = QPushButton('tab2', self)
        self.Creator.resize(100, 40)
        self.Creator.move(260, 50)


if __name__ == "__main__":
    app = QApplication([])
    juego = Game()
    juego.show()
    sys.exit(app.exec_())

    print("saliendo :D gracias c:")

