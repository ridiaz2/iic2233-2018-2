import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QListWidget, QScrollBar, \
    QWidget, QListWidgetItem, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, QObject, pyqtSignal, Qt, QTimer

from backend import NumeroImagen, Fondo, InicioChecker, ruta_colores,\
    ruta_imagenes, completar_numero, extraer_numero, ruta_sprites, \
    diccionario_colores, ruta_iconos
import time
from juego import Game, MainWindow2


window_name, base_class = uic.loadUiType("menu.ui")
partida_name, partida_class = uic.loadUiType("partidas.ui")
sala_name, sala_class = uic.loadUiType("sala_espera.ui")



class SalaEspera(sala_name, sala_class):

    signal_botones = pyqtSignal(str)
    signal_enviar_mensaje = pyqtSignal(tuple)
    signal_actualizar_color = pyqtSignal(tuple)
    signal_agregar_invitado = pyqtSignal(tuple)
    signal_iniciar_contador = pyqtSignal(int)

    def __init__(self, usuario, cliente, numero, nombre, nueva=True):
        print("Creando sala de espera")
        super().__init__()
        self.invitado = f"{usuario} (Invitado)"
        self.datos = dict()
        self.color_jugador = 0
        self.color_invitado = 0
        self.color_jugadores = {}
        if nueva:
            self.admin = usuario
            self.jugadores = [usuario]
            self.usuario = usuario
        else:
            self.admin = None
            self.jugadores = []
            self.usuario = usuario
        self.botones_colores = {}
        self.color_marcado = None
        self.oscuro_img = QPixmap(f"{ruta_colores}/oscuro.png")
        self.marcado_img = QPixmap(f"{ruta_colores}/marcador_color.png")
        self.cliente = cliente
        print("pasó ifs y elifs")
        self.mensaje = None
        self.numero = numero
        self.nombre = nombre
        print("viene dicc")
        print("pasó dicc")
        self.cliente.sala_espera = self
        self.state = True
        print("estado listo")
        fondo = Fondo(self)
        fondo.start()
        print("fondo listo")
        self.setupUi(self)
        self.setWindowTitle(f"DCCurve - Sala de Espera {self.numero}: {nombre}")

        print("cambió título :D")

        claro_img = QPixmap(f"{ruta_colores}/claro.png")
        self.text_fondo.setPixmap(claro_img)
        self.text_fondo_2.setPixmap(self.oscuro_img)
        self.text_jugadores = (self.text_jugador_1, self.text_jugador_2,
                               self.text_jugador_3, self.text_jugador_4)

        self.poderes = tuple((self.__dict__[f"check_poder_{n}"] for n in
                              range(1, 10)))

        self.visualizar_jefe = (self.text_velocidad, self.text_puntaje_max,
                                self.text_contador, self.edit_velocidad,
                                self.edit_puntaje_max,
                                self.button_iniciar_partida) + self.poderes
        print("vis jefe")
        self.visualizar_jugador = (self.text_contador_2,
                                   self.text_titulo_contador)
        print("vis jug")
        if nueva:
            self.jefe = True
            for elemento in self.visualizar_jugador:
                elemento.hide()
        else:
            self.jefe = False
            for elemento in self.visualizar_jefe:
                elemento.hide()
        self.mostrar_colores()
        print(1)
        self.button_enviar.clicked.connect(self.enviar_mensaje)
        print(2)
        self.signal_botones.connect(self.opciones_botones)
        print(3)
        print(InicioChecker)
        print(InicioChecker(self))
        self.chequeador = InicioChecker(self)
        print(4)
        self.signal_enviar_mensaje.connect(self.chequeador.check_mensaje_enviar)
        self.lista_chat.addItem("")
        self.button_seleccionar_color.clicked.connect(self.seleccionar_color)
        self.button_seleccionar_color_invitado.hide()
        self.signal_actualizar_color.connect(
            self.chequeador.check_actualizar_color)
        self.button_agregar_invitado.clicked.connect(self.agregar_invitado)
        self.signal_agregar_invitado.connect(
            self.chequeador.check_agregar_invitado)
        self.button_seleccionar_color_invitado.clicked.connect(
            self.seleccionar_color_invitado)
        self.button_iniciar_partida.clicked.connect(self.iniciar_contador)
        self.signal_iniciar_contador.connect(
            self.chequeador.check_iniciar_contador)

    def enviar_datos(self):
        if self.jefe:
            '''https://gis.stackexchange.com/questions/
            201919/find-out-if-checkbox-checked-pyqgis'''
            poderes = tuple([poder.isChecked() for poder in self.poderes])
            print("PODERES:", self.poderes)
            print(poderes)
            velocidad = self.edit_velocidad.text()
            puntaje_max = self.edit_puntaje_max.text()
            self.cliente.send({"estado": "recepcion_datos_jefe",
                                      "contenido": (self.numero, (poderes,
                                                    velocidad, puntaje_max))})

    def actualizar_contador(self, numero):
        for contador in (self.text_contador, self.text_contador_2):
            contador.setText(str(numero))

    @property
    def n_jugador(self):
        print("INGRESO A N_JUGADOR")
        numero = self.datos["jugadores"].index(self.usuario) + 1
        return numero

    @property
    def n_invitado(self):
        try:
            numero = self.datos["jugadores"].index(self.invitado) + 1
        except ValueError:
            numero = 0
        return numero

    def iniciar_contador(self):
        if self.text_contador.text() == "10":
            self.signal_iniciar_contador.emit(self.numero)



    def mostrar_colores(self):
        '''https://stackoverflow.com/questions/20668060/
        pyqt-qpushbutton-background-color'''
        for n in range(1, 33):
            color = diccionario_colores[f"color_{n}"]
            boton = self.__dict__[f"color_{n}"]
            boton.setStyleSheet(f"background-color:"
                                    f"{color}; border: none")
            self.botones_colores[boton] = n
            boton.clicked.connect(self.marcar_color)

    def marcar_color(self):
        boton = self.sender()
        numero = self.botones_colores[boton]
        print("comienzo marcar")

        if self.color_marcado is not None:
            self.boton_color(self.color_marcado, True).clear()
        print("pasa none")
        self.color_marcado = numero
        print("define")
        self.boton_color(numero, True).setPixmap(self.marcado_img)
        print(":D")

    def seleccionar_color(self):
        print("INGRESO SELECCIONAR COLOR")
        print(self.n_jugador)
        n_color = self.color_marcado
        if n_color is not None and self.n_jugador != 0 and \
                n_color not in self.datos["colores"].values():
            print("PASÓ IF")
            color = diccionario_colores[f"color_{n_color}"]
            print("COLOR LISTO")
            print(self.n_jugador)
            cuadro = self.__dict__[f"text_jugador_{self.n_jugador}"]
            print("JUGADOR LISTO")
            cuadro.setStyleSheet(f"background-color: {color}")
            self.signal_actualizar_color.emit((self.usuario, n_color,
                                               self.numero))

    def agregar_invitado(self):
        print("AGREGAR INVITADO")
        if len(self.datos["jugadores"]) <= 4:
            print("PASÖ EL IF")
            self.signal_agregar_invitado.emit((self.usuario, self.numero))
            self.button_agregar_invitado.hide()
            self.button_seleccionar_color_invitado.show()

    def seleccionar_color_invitado(self):
        print("INGRESO COLOR INVITADO")
        n_color = self.color_marcado
        if n_color is not None and self.n_invitado != 0:
            print("PASó if")
            print("PASÖ COLOR")
            cuadro = self.__dict__[f"text_jugador_{self.n_invitado}"]
            print("PASÖ CUADRO")
            print("PASÖ CAMBIAR COLOR")
            self.signal_actualizar_color.emit((self.invitado, n_color,
                                               self.numero))

    def boton_color(self, n, fondo=False):
        if fondo:
            n = str(n) + "_"
        return self.__dict__[f"color_{n}"]

    def enviar_mensaje(self):
        self.signal_botones.emit("enviar_mensaje")

    def opciones_botones(self, tipo):
        if tipo == "enviar_mensaje":
            mensaje = self.edit_chat.text()
            self.signal_enviar_mensaje.emit((self.usuario, mensaje,
                                             self.numero))

    def actualizar_datos(self, diccionario):
        def completar(iterable):
            if type(iterable) == list:
                complemento = ["", "", "", ""][:4 - len(iterable)]
                return iterable + complemento
            else:
                iterable = list(iterable)
                complemento = [0, 0, 0, 0][
                    :4 - len(iterable)]
                return iterable + complemento

        self.datos = diccionario
        print("ACTUALIZAR DATOS:", diccionario)

        if self.datos["jugadores"][0] == self.usuario and not self.jefe:
            self.jefe = True
            for elemento in self.visualizar_jugador:
                elemento.hide()
            for elemento in self.visualizar_jefe:
                elemento.show()

        if diccionario["chat"] and diccionario["actualizar_chat"]:
            '''http://pyqt.sourceforge.net/Docs/PyQt4/qlistwidget.html'''
            #self.lista_chat.addItem(f"{diccionario['chat'][-1][0]}: "
             #                   f"{diccionario['chat'][-1][1]}")
            item_nuevo = QListWidgetItem()
            item_nuevo.setText(f"{diccionario['chat'][-1][0]}: "
                               f"{diccionario['chat'][-1][1]}")
            self.lista_chat.insertItem(self.lista_chat.count() - 1, item_nuevo)
        else:
            for cuadro, nombre, color_ in zip(
                    self.text_jugadores, completar(diccionario["jugadores"]),
                    completar(diccionario["colores"].values())):
                print("CAMBIO:", nombre, color_,
                      self.color_jugadores.get(nombre, -1))
                if color_ != self.color_jugadores.get(nombre, -1) or \
                        color_ == 0:
                    color = diccionario_colores[
                        f"color_{color_}"]
                    cuadro.setStyleSheet(f"background-color: {color}")
                    self.color_jugadores[nombre] = color_
                if cuadro.text != nombre:
                    cuadro.setText(nombre)
          #      color_2 = cuadro.palette().button().color().name()
           #     print("estilo:", nombre, color_2, color, color_2 == color, \
            #        color_2 == color.lower())
        maximo_largo = self.lista_chat.verticalScrollBar().maximum()
        if self.lista_chat.verticalScrollBar().value() in (maximo_largo,
                        maximo_largo - 1, maximo_largo - 2, maximo_largo + 1,
                                                           maximo_largo - 3):
            '''https://stackoverflow.com/questions/4939151/# how-to-program-
            scrollbar-to-jump-to-bottom-top-in-case-of-change-in-qplaintexted'''
        if True:
            self.lista_chat.verticalScrollBar().setValue(maximo_largo)

    def comenzar(self):
        self.hide()
        print("ventana escondida")
        self.state = False
        juego = Game(self.cliente, self)
        print("JUEGO CREADO")
        self.cliente.game = juego
        print("NOMBRE CLIENTE LISTO")
        juego.show()
        print("MOSTRADO")



class PartidasWindow(partida_name, partida_class):

    signal_boton = pyqtSignal(int)
    signal_actualizar = pyqtSignal(tuple)
    signal_seleccionar = pyqtSignal(tuple)

    def __init__(self, usuario, cliente):
        super().__init__()
        self.usuario = usuario
        self.mensaje = None

        print("usuario: ", self.usuario)
        self.cliente = cliente
        self.cliente.ventana_partidas = self
        self.state = True
        fondo = Fondo(self)
        fondo.start()
        self.setupUi(self)

        print("Creando Ventana Partida")

        claro_img = QPixmap(f"{ruta_colores}/claro.png")
        self.espacio_titulo.setPixmap(claro_img)
        self.espacio_bienvenida.setPixmap(claro_img)
        self.text_bienvenida.setText(f"Bienvenid@ {self.usuario}")
        self.espacio_nombre.setPixmap(claro_img)
        self.espacio_nombre.hide()
        self.button_crear.hide()
        self.text_nombre.hide()
        self.edit_nombre.hide()
        self.escondidos = (self.espacio_nombre, self.button_crear, \
                          self.text_nombre, self.edit_nombre)

        print(2)

        self.button_seleccionar.clicked.connect(self.ventana_seleccionar)
        self.button_nueva_partida.clicked.connect(self.ventana_nueva_partida)
        self.button_crear.clicked.connect(self.ventana_crear)
        print(2.5)
        self.button_actualizar.clicked.connect(self.ventana_actualizar)
        print(2.8)
        self.signal_boton.connect(self.abrir_ventana)
        print(3)
        self.chequeador = InicioChecker(self)
        self.signal_actualizar.connect(self.chequeador.check_lista_partidas)
        print(4)
        self.ventana_actualizar()
        self.signal_seleccionar.connect(
            self.chequeador.check_seleccionar_partida)


    def ventana_actualizar(self):
        self.signal_actualizar.emit((True, ""))

    def ventana_nueva_partida(self):
        self.signal_boton.emit(2)

    def ventana_seleccionar(self):
        self.signal_boton.emit(1)

    def ventana_crear(self):
        self.signal_boton.emit(3)

    def abrir_ventana(self, numero):
        if numero == 2:
            for elemento in self.escondidos:
                if elemento.isHidden():
                    elemento.show()

        elif numero == 3:
            nombre = self.edit_nombre.text()
            self.signal_actualizar.emit((False, (nombre, self.usuario)))

        elif numero == 1:
            # https://www.youtube.com/watch?v=f6i3_jYjspQ
            print(self.lista_partidas.selectedItems())
            print(self.lista_partidas.selectedItems()[0].text())
            print(extraer_numero(self.lista_partidas.selectedItems()[0].text()))
            self.signal_seleccionar.emit((extraer_numero(
                self.lista_partidas.selectedItems()[0].text()), self.usuario))


    def comenzar(self, lista):
        num_partida = len(lista[1]) - 1
        if not lista[0]:
            print("Sï lo era :D")
            if lista[2] == "nueva":
                print("nueva :O")
                self.hide()
                self.state = False

                sala = SalaEspera(self.usuario, self.cliente, num_partida,
                                  lista[1][num_partida][0])
                sala.show()
            else:
                print("asig varialbes")
                print(lista[1])
                disponible, nombre_partida, num_partida = lista[1]
                print("variables asignadas")
                if not disponible:
                    pass
                else:
                    self.hide()
                    self.state = False
                    print("vamos a crear la sala")
                    sala = SalaEspera(self.usuario, self.cliente, num_partida,
                                      nombre_partida, nueva=False)
                    sala.show()
        else:
            print("entra a comenzar")
            self.lista_partidas.clear()
            print("limpiado")

            print("saca num")
            for i in range(len(lista[1])):
                self.lista_partidas.addItem(f"[{completar_numero(i)}] "
                                        f"{lista[1][i][0]} ({lista[1][i][1]})")

            print("pasa esto")
            '''
            print(self.lista_partidas.verticalScrollBar)
            print(self.lista_partidas.verticalScrollBar())
            print(self.lista_partidas.verticalScrollBar().setValue)
            print(self.lista_partidas.verticalScrollBar().maximum())
            print(self.lista_partidas.verticalScrollBar().value())
            '''
            maximo_largo = self.lista_partidas.verticalScrollBar().maximum()
            if self.lista_partidas.verticalScrollBar().value() in (maximo_largo,
                                                            maximo_largo - 1):
                '''https://stackoverflow.com/questions/4939151/# how-to-program-
            scrollbar-to-jump-to-bottom-top-in-case-of-change-in-qplaintexted'''

                self.lista_partidas.verticalScrollBar().setValue(maximo_largo)
                print("Nuevo", self.lista_partidas.verticalScrollBar().value())

            print("vamos a ver si es para entrar realmente")









class MainWindow(window_name, base_class):

    signal_boton_inicio = pyqtSignal(int)
    signal_check_ingresar = pyqtSignal(tuple)
    signal_check_registrar = pyqtSignal(tuple)

    def __init__(self, cliente):
        super().__init__()
        self.cliente = cliente
        self.mensaje = ""
        self.usuario = ""

        self.state = True
        self.ventana = 0

        fondo = Fondo(self)
        fondo.start()

        self.setupUi(self)

        logo_img = QPixmap(f'{ruta_iconos}/logo.png')
        self.logo.setPixmap(logo_img)

        claro_img = QPixmap(f"{ruta_colores}/claro.png")
        self.espacio_datos.setPixmap(claro_img)
        self.espacio_datos.hide()
        self.espacio_error_inicio.setPixmap(claro_img)
        self.espacio_error_inicio.hide()

        oscuro_img = QPixmap(f"{ruta_colores}/oscuro.png")
        self.inicio_ingresar_oscuro.setPixmap(oscuro_img)
        self.inicio_registrar_oscuro.setPixmap(oscuro_img)

        self.inicio_ingresar_oscuro.hide()
        self.inicio_registrar_oscuro.hide()


        self.opciones_ingresar = (self.text_user, self.text_password,
                                  self.edit_user, self.edit_password,
                                  self.button_ingresar)

        self.opciones_registrar = (self.text_user, self.text_password,
                                   self.edit_user, self.edit_password,
                                   self.button_registrar,
                                   self.text_password_rep,
                                   self.edit_password_rep)

        for elemento in self.opciones_ingresar + self.opciones_registrar:
            elemento.hide()

        self.inicio_ingresar.clicked.connect(self.ventana_ingresar)

        self.inicio_registrar.clicked.connect(self.ventana_registrar)

        self.signal_boton_inicio.connect(self.abrir_ventana)

        self.button_ingresar.clicked.connect(self.check_ingresar)
        self.button_registrar.clicked.connect(self.check_registrar)

        self.chequeador = InicioChecker(self)
        self.signal_check_ingresar.connect(self.chequeador.check_ingresar)
        self.signal_check_registrar.connect(self.chequeador.check_registrar)


    def ventana_ingresar(self):
        self.signal_boton_inicio.emit(1)

    def ventana_registrar(self):
        self.signal_boton_inicio.emit(2)

    def check_ingresar(self):
        print("apretó el boton jeje")
        hola = str(self.edit_user.text())
        hola2 = str(self.edit_password.text())
        print("hola")
        self.usuario = str(self.edit_user.text())
        self.signal_check_ingresar.emit((str(self.edit_user.text()),
                                         str(self.edit_password.text())))

    def check_registrar(self):
        print("apretó el boton jeje")
        hola = str(self.edit_user.text())
        hola2 = str(self.edit_password.text())
        print("hola2")
        print(hola, hola2, str(self.edit_password_rep.text()))
        self.signal_check_registrar.emit((str(self.edit_user.text()),
                                         str(self.edit_password.text()),
                                         str(self.edit_password_rep.text())))


    def abrir_ventana(self, numero):
        if self.espacio_datos.isHidden():
            self.espacio_datos.show()

        if numero == 1:
            if not self.inicio_registrar_oscuro.isHidden():
                self.inicio_registrar_oscuro.hide()
            if self.inicio_ingresar_oscuro.isHidden():
                self.inicio_ingresar_oscuro.show()
            self.ventana = 1
            if not self.text_bienvenida.isHidden():
                self.text_bienvenida.hide()
            for elemento in self.opciones_registrar:
                if not elemento.isHidden():
                    elemento.hide()
            for elemento in self.opciones_ingresar:
                if elemento.isHidden():
                    elemento.show()

        elif numero == 2:
            if not self.inicio_ingresar_oscuro.isHidden():
                self.inicio_ingresar_oscuro.hide()
            if self.inicio_registrar_oscuro.isHidden():
                self.inicio_registrar_oscuro.show()
            self.ventana = 2
            if not self.text_bienvenida.isHidden():
                self.text_bienvenida.hide()
            for elemento in self.opciones_ingresar:
                if not elemento.isHidden():
                    elemento.hide()
            for elemento in self.opciones_registrar:
                if elemento.isHidden():
                    elemento.show()
        objeto = QLabel(self)
        objeto.move(100, 100)
        objeto.resize(100, 100)
        objeto.setPixmap(QPixmap("map1.png"))
        if objeto.isHidden():
            objeto.show()

        objeto = QLabel(self)
        objeto.move(100, 100)
        objeto.resize(200, 200)
        objeto.setPixmap(QPixmap("map1.png"))
        if objeto.isHidden():
            objeto.show()

    def comenzar(self, estado):
        if estado and self.usuario:
            print("estado True")
            self.hide()
            print("ventana escondida")
            self.state = False
            partida = PartidasWindow(self.usuario, self.cliente)
            partida.show()
        else:
            self.usuario = ""

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

if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())