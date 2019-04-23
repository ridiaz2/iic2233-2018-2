
from itertools import count
from random import randint, triangular, uniform, normalvariate, random
from random import choice as choice_func
from datetime import datetime, timedelta
from parameters import parametros as par
from gui.entities import Entity, Human, Game, Building, _PATH
from collections import deque, defaultdict
import gui
import os


########################### FUNCIONES ##########################################

def normal(mu, sigma, entero=True):
    if entero:
        funcion = int
    else:
        funcion = float
    return funcion(abs(normalvariate(mu, sigma)))

def normales(mu, sigma):
    while True:
        yield normal(mu, sigma)

def choice(lista):
    if not lista:
        return ""
    return choice_func(lista)


def prob_valor(probabilidad):
    numero = random()
    if numero <= probabilidad:
        return True
    return False


def intervalo(lista, numero):

    lista2 = lista.copy()
    lista2.insert(0, 0)
    intervalos = tuple((lista2[i-1], lista2[i]) for i in range(1, len(lista2)))
    for i in range(len(intervalos)):
        if intervalos[i][0] < numero <= intervalos[i][1]:
            return i
    if not numero:
        return 0

def medio(minimo, valor, maximo):
    return sorted([minimo, valor, maximo])[1]

def mayus(texto):
    return texto[0].upper() + texto[1:]

id_clientes, id_personal, id_juegos, id_instalaciones = [count(start=0)
                                                        for ides in range(4)]

listado_nombres = []

dicc_personalidades = {"ludopata": (1, 1, 2, 1, 1, 2, 1),
                           "kibitzer": (0, 1, 0, 1, 2, 0, 1),
                           "dieciochero": (1, 0, 2, 1, 2, 1, 0),
                           "ganador": (1, 1, 1, 2, 2, 2, 2),
                           "millonario": (2, 1, 1, 1, 1, 2, 1)}

with open("first-names.txt", encoding="utf-8") as nombres:
    for linea in nombres:
        listado_nombres.append(linea.strip())

def nombre_random():
    return choice(listado_nombres)

def edad_random():
    return int(triangular(17, 130, 38))

def direccion(valor):
    if valor:
        return int(valor / int(abs(valor)))
    return 0


############################## CLASES ##########################################

class Pixel(Entity):
    path = _PATH + os.sep + "assets" + os.sep + "decoration" + os.sep

    def __init__(self, x=0, y=0, parent=None):
        super().__init__(self.path + f"white.png", parent=parent)
        self.x = x
        self.y = y



class Casino:
    def __init__(self):
        self.clientes = dict()
        self.personal = dict()
        self.juegos = dict()
        self.instalaciones = dict()
        self.espacios_ocupados = []
        self.centro_x = 387
        self.centro_y = 243
        self.pixeles = []
        self._dinero = 0
        self.dinero_por_dia = 0
        self.conversador = []
        self.clientes_fuera = dict()
        self.ganancias = []
        self.jugadores = defaultdict(list)

    @property
    def dinero(self):
        return self._dinero

    @dinero.setter
    def dinero(self, valor):
        ganancia = valor - self.dinero
        self.dinero_por_dia += ganancia
        self._dinero = max([0, valor])

    def go_retirar(self, cliente):
        cliente.destino = (0, 0)
        cliente.camino = deque()
        cliente.accion = "retirar"
        cliente.transportandose = True
        #self.mover_cliente(cliente, self.casino.camino(cliente))


    def go_jugar(self, cliente):
        tipo_juego = choice(["ruleta", "tragamonedas"])
        juego = choice([i for i in self.juegos.values() if
                        i.tipo == tipo_juego])
        cliente.destino = juego.ubicacion
        cliente.lugar = juego
        cliente.camino = deque()
        cliente.accion = "jugar"
        cliente.transportandose = True


    def go_actividad(self, cliente):
        lista_opciones = ["conversar", "tini"]
        if cliente.personalidad == "kibitzer" and cliente.hablado:
            lista_opciones.append("predecir")
        tipo_actividad = choice(lista_opciones)
        if tipo_actividad == "conversar":
            cliente.add_decoration(None)
            cliente.add_decoration("gui/assets/decoration/yellow.png")
            if self.conversador:
                cliente.destino = (self.conversador.x, self.conversador.y)
                cliente.lugar = self.conversador
                cliente.camino = deque()
                cliente.accion = "hablar"
                cliente.transportandose = True
                cliente.lugar.lugar = cliente
                cliente.lugar.lugar.accion = "hablar"
                self.conversador = []
            else:
                cliente.accion = "esperar"
                cliente.lugar = "esperando_hablar"
                cliente.transportandose = False
        elif tipo_actividad == "tini":
            cliente.add_decoration(None)
            cliente.add_decoration("gui/assets/decoration/blue.png")
            cliente.accion = ""
            cliente.transportandose = False
            cliente.stamina -= par.n
            cliente.mafia = True
        elif tipo_actividad == "predecir":
            juego = choice([i for i in self.juegos.values() if
                            i.tipo == "ruleta"])
            cliente.destino = juego.ubicacion
            cliente.lugar = juego
            cliente.camino = deque()
            cliente.accion = "jugar_predecir"
            cliente.contar = True
            cliente.transportandose = True




    def go_instalacion(self, cliente):
        tipo_instalacion = choice(["tarot", "restobar", "baños"])
        instalacion = choice([i for i in self.instalaciones.values()
                              if i.tipo == tipo_instalacion])
        cliente.destino = instalacion.ubicacion
        cliente.lugar = instalacion
        cliente.camino = deque()
        cliente.accion = "instalacion"
        cliente.transportandose = True

    def siguiente_accion(self, cliente):
        if cliente.accion:
            return
        cliente.ya_realizado = False
        dicc_funciones = {"retirarse": self.go_retirar, "jugar": self.go_jugar,
                          "actividad": self.go_actividad,
                          "instalacion": self.go_instalacion}
        accion = cliente.siguiente_accion()
        if accion == "retirarse":
            cliente.accion_retirada = "retiro"
        funcion = dicc_funciones[accion]
        funcion(cliente)
        return

    def realizar_accion(self, cliente):
        if cliente.transportandose:
            return
        elif cliente.accion == "jugar":
            if not cliente.ya_realizado:
                if cliente.lugar.cumple(cliente):
                    ganancia = cliente.lugar.jugar(cliente)
                    self.dinero += ganancia
                else:
                    cliente.tiempo_accion = 0
                cliente.ya_realizado = True
            cliente.tiempo_accion -= 1
            if not cliente.tiempo_accion:
                cliente.accion = ""
        elif cliente.accion == "jugar_predecir":
            if not cliente.ya_realizado:
                if cliente.lugar.cumple(cliente):
                    descubrir = False
                    for veces in range(par.v):
                        ganancia = cliente.lugar.jugar(cliente, predecir=True)
                        self.dinero += ganancia[0]
                        if not descubrir:
                            descubrir = ganancio[1]
                    if descubrir:
                        cliente.tiempo_accion = 0
                        cliente.ya_realizado = True
                        self.go_retirar(cliente)
                else:
                    cliente.tiempo_accion = 0
                cliente.ya_realizado = True
            cliente.tiempo_accion -= 1
            if not cliente.tiempo_accion:
                cliente.accion = ""

        elif cliente.accion == "instalacion":
            if not cliente.ya_realizado:
                if cliente.lugar.cumple(cliente):
                    ganancia = cliente.lugar.usar(cliente)
                    self.dinero += ganancia
                else:
                    cliente.tiempo_accion = 0
                cliente.ya_realizado = True
            cliente.tiempo_accion -= 1
            if not cliente.tiempo_accion:
                cliente.accion = ""
        elif cliente.accion == "hablar":
            if not cliente.ya_realizado:
                cliente.hablar()
                cliente.ya_realizado = True
            cliente.tiempo_accion -= 1
            if not cliente.tiempo_accion:
                cliente.add_decoration(None)
                cliente.add_decoration("gui/assets/decoration/transparent.png")
                cliente.accion = ""
        elif cliente.accion == "esperar":
            cliente.tiempo_accion -= 1
            if not cliente.tiempo_accion:
                cliente.add_decoration(None)
                cliente.add_decoration("gui/assets/decoration/transparent.png")
                cliente.accion = ""








    def bordes(self, x1, x2, y1, y2, mapa=False):
        borde = []
        if not mapa:
            x1 -= 1
            x2 += 1
            y1 -= 1
            y2 += 1
        for i in range(x2, x1, -1):
            if (i, y1) not in self.espacios_ocupados:
                borde.append((i, y1))
        for i in range(y1, y2):
            if (x1, i) not in self.espacios_ocupados:
                borde.append((x1, i))
        for i in range(x1, x2):
            if (i, y2) not in self.espacios_ocupados:
                borde.append((i, y2))
        for i in range(y2, y1, -1):
            if (x1, i) not in self.espacios_ocupados:
                borde.append((x2, i))
        return borde

    def agregar_juego(self, tipo, x=0, y=0):
        if tipo == "tragamonedas":
            clase_juego = Tragamonedas
        else:
            clase_juego = Ruleta
        juego = clase_juego(x, y)
        self.juegos[juego.id] = juego
        return juego

    def agregar_instalacion(self, tipo, x=0, y=0):
        instalacion = Instalacion(tipo, x, y)
        self.instalaciones[instalacion.id] = instalacion
        return instalacion

    def agregar_personal(self, tipo, x=0, y=0):
        personal = Personal(tipo, x, y)
        self.personal[personal.id] = personal
        return personal

    def agregar_cliente(self, personalidad=choice(
                        list(dicc_personalidades)), x=30, y=10):
        cliente = Cliente(personalidad, x, y)
        self.clientes[cliente.id] = cliente
        return cliente


    def ubicacion_posible(self, x, y, ancho, alto):
        if len(set([(x, y), (x + ancho, y), (x, y + alto),
                   (x + ancho, y + alto)]) &
                       set(self.espacios_ocupados)) > 0:
            return False
        return True

    def ubicacion_posible_1d(self, eje, otro, medida, otra_medida, direccion):
        if not direccion:
            eje, otro, medida, otra_medida = otro, eje, otra_medida, medida
        if len(set([(eje, otro), (eje + medida, otro), (eje, otro +
            otra_medida), (eje + medida, otro + otra_medida)]) & set(
                    self.espacios_ocupados)) > 0:
            return False
        return True

    def mover_cliente(self, cliente, camino):
        if not camino:
            camino.append((0, 0))
        for i in range(min(par.h, len(camino))):
            movimiento = camino.popleft()
            cliente.x += movimiento[0]
            cliente.y += movimiento[1]
        if cliente.accion == "retirar" and not camino:
            cliente.accion = ""
            cliente.transportandose = False
            cliente.fuera = True
        elif not camino:
            cliente.transportandose = False
            if not cliente.tiempo_accion:
                if cliente.lugar == "esperando_hablar":
                    cliente.tiempo_accion = par.d
                elif type(cliente.lugar) == Cliente and not cliente.accion ==\
                        "esperar":
                    cliente.tiempo_accion = max([cliente.duracion_hablar,
                                                cliente.lugar.duracion_hablar])
                elif cliente.lugar.tipo in ("tragamonedas", "ruleta"):
                    cliente.tiempo_accion = cliente.lugar.duracion
                else:
                    cliente.tiempo_accion = cliente.lugar.duracion(cliente)


    def camino(self, cliente, historial=deque()):
        historial = deque()
        if cliente.camino:
            return cliente.camino
        cliente.camino = self.encontrar_camino(cliente.x, cliente.y,
                    cliente.ancho, cliente.alto, cliente.destino, historial)
        return cliente.camino

    def encontrar_camino(self, x, y, ancho, alto, destino,
                         historial=deque()):
        # direccion = 0 -> vertical, direccion = 1 -> horizontal
        #n = 0
        if (x, y) == destino:
            return historial
        while not (x, y) == destino:
            #print(n)
            #print((x, y), historial)
            #n += 1
            # primera fase, mover por eje x:
            x2 = x + ancho
            y2 = y + alto
            dif_x = destino[0] - x
            dif_y = destino[1] - y
            dif_centro_y = self.centro_y - y
            dif_centro_x = self.centro_x - x
            dir_x = direccion(dif_x)
            dir_y = direccion(dif_y)

            for i in range(int(abs(dif_x))):
                if self.ubicacion_posible(x + dir_x, y, ancho, alto):
                    x += dir_x
                    historial.append((dir_x, 0))
                    if (x, y) == destino:
                        return historial
                else:
                    dif_mayor = max([dif_y, dif_centro_y])
                    if dif_mayor == 0:
                        dif_mayor = 0
                    dir_mayor = direccion(dif_mayor)
                    while not self.ubicacion_posible(x + dir_x, y + dir_mayor,
                                                     ancho, alto):
                        y += dir_mayor
                        historial.append((0, dir_mayor))
                        if (x, y) == destino:
                            return historial
                    y += dir_mayor
                    historial.append((0, dir_mayor))
                    if (x, y) == destino:
                        return historial
                    x += dir_x
                    historial.append((dir_x, 0))
                    if (x, y) == destino:
                        return historial
            #print(n)
            #print((x, y), historial)
            #n += 1
            # segunda fase: desplazamiento en y:
            x2 = x + ancho
            y2 = y + alto
            dif_x = destino[0] - x
            dif_y = destino[1] - y
            dif_centro_y = self.centro_y - y
            dif_centro_x = self.centro_x - x
            dir_x = direccion(dif_x)
            dir_y = direccion(dif_y)

            for i in range(int(abs(dif_y))):
                if self.ubicacion_posible(x, y + dir_y, ancho, alto):
                    y += dir_y
                    historial.append((0, dir_y))
                    if (x, y) == destino:
                        return historial
                else:
                    dif_mayor = max([dif_x, dif_centro_x])
                    if dif_mayor == 0:
                        dif_mayor = 0
                    dir_mayor = direccion(dif_mayor)
                    while not self.ubicacion_posible(x + dir_mayor, y + dir_y,
                                                     ancho, alto):
                        x += dir_mayor
                        historial.append((dir_mayor, 0))
                        if (x, y) == destino:
                            return historial
                    x += dir_mayor
                    historial.append((dir_mayor, 0))
                    if (x, y) == destino:
                        return historial
                    y += dir_y
                    historial.append((0, dir_y))
                    if (x, y) == destino:
                        return historial
        return historial





    def encontrar_camino3(self, x, y, ancho, alto, destino, direccion=0,
                         historial=deque()):
        # direccion = 0 -> vertical, direccion = 1 -> horizontal
        if not historial:
            historial = deque()
        if (x, y) == destino:
            return historial
        elif x == destino[0] and direccion:
            direccion = int(abs(direccion - 1))
        elif y == destino[1] and not direccion:
            direccion = int(abs(direccion - 1))
        if direccion:
            eje = x
            otro = y
            medida = ancho
            otra_medida = alto
            des = destino[0]
        else:
            eje = y
            otro = x
            medida = alto
            otra_medida = ancho
            des = destino[1]

        signo = 0
        dif = des - eje
        if dif:
            signo = int(dif / abs(dif))
        nuevo = eje + signo
        if self.ubicacion_posible_1d(nuevo, otro, medida, otra_medida,
                                   direccion):
            if direccion:
                historial.append((nuevo - x, 0))
                return self.encontrar_camino(nuevo, y, ancho, alto, destino,
                                      direccion, historial)
            else:
                historial.append((0, nuevo - y))
                return self.encontrar_camino(x, nuevo, ancho, alto, destino,
                                      direccion, historial)
        else:
            return self.encontrar_camino(nuevo, y, ancho, alto, destino,
                            int(abs(direccion - 1)), historial)







    def encontrar_camino2(self, x, y, ancho, alto, destino, historial=[]):
        if (x, y) == destino:
            return historial
        x2 = x
        y2 = y
        #if type(cliente) == int:
         #   cliente = self.clientes[cliente]
        dif_x = destino - x
        dif_y = destino - y
        if dif_x > 0:
            x2 = x + 1
        elif dif_x < 0:
            x2 = x - 1
        if dif_y > 0:
            y2 = y + 1
        elif dif_y < 0:
            y2 = y - 1
        if self.ubicacion_posible(x2, y2, ancho, alto):
            historial.append((x2 - x, y2 - y))
            return encontrar_camino(x2, y2, ancho, alto, destino, historial)
        else:
            for i in (x, x2, -x2):
                for y in (y, y2, -y2):
                    pass




    def mapeo(self):
        #for i in list(self.instalaciones.values()) + list(
        # self.juegos.values()):
         #   print(repr(i), i.x, i.y, i.ancho, i.alto)
        for lugar in list(self.instalaciones.values()) + list(
                self.juegos.values()):
            x1, x2, y1, y2 = lugar.x, lugar.x + lugar.ancho, lugar.y, lugar.y\
                             + lugar. alto
            for i in range(x2, x1, -1):
                if (i, y1) not in self.espacios_ocupados:
                    self.espacios_ocupados.append((i, y1))
            for i in range(y1, y2):
                if (x1, i) not in self.espacios_ocupados:
                    self.espacios_ocupados.append((x1, i))
            for i in range(x1, x2):
                if (i, y2) not in self.espacios_ocupados:
                    self.espacios_ocupados.append((i, y2))
            for i in range(y2, y1, -1):
                if (x2, i) not in self.espacios_ocupados:
                    self.espacios_ocupados.append((x2, i))
            #for ancho in range(lugar.x, lugar.x + lugar.ancho):
             #   for alto in range(lugar.y, lugar.y + lugar.alto):
              #      self.espacios_ocupados.append((ancho, alto))


    def agregar_bordes(self):
        for i in list(self.instalaciones.values()) + list(self.juegos.values()):
            i.bordes = self.bordes(i.x, i.x + i.ancho, i.y, i.y + i.alto)



    def tick(self):
        if prob_valor(par.p):
            self.agregar_cliente()



class Individuo:
    def __init__(self):
        if self.__class__ == Cliente:
            id_individuo = id_clientes
        else:
            id_individuo = id_personal

        self.id = next(id_individuo)
        self.nombre = nombre_random()
        self.edad = edad_random()


class Cliente(Individuo, Human):
    dicc_personalidades = dicc_personalidades


    def __init__(self, personality, x=0, y=0):

        Individuo.__init__(self)
        Human.__init__(self, personality, x, y)
        self._dinero_inicial,self._lucidez, self._ansiedad, self._suerte, \
            self._sociabilidad, self._stamina, self._deshonestidad = \
            self.valores(personality)
        self.ansiedad_aumentada = False
        self.personalidad = personality
        self._dinero = 200 * self._dinero_inicial
        self.ancho = 36
        self.alto = 36
        self.destino = (x, y)
        self.camino = deque()
        self.accion = ""
        self.transportandose = False
        self.add_decoration("gui/assets/decoration/transparent.png")
        self._tiempo_accion = 0
        self.ya_realizado = False
        self.hablado = False
        self.fuera = False
        self.mafia = False
        self.contar = False
        self.estadia = 0
        self.razon_retirada = ""

    @property
    def duracion_hablar(self):
        return max([self.lucidez + self.sociabilidad - self.ansiedad, 0.1]) *\
               (par.pi ** 2)

    def apuesta(self, lugar):
        return (1 + par.o * self.ansiedad) + lugar.apuesta_minima

    def hablar(self):
        cliente.hablado = True
        cliente.ansiedad -= (par.e / 100) * cliente.ansiedad
        cliente.deshonestidad += par.x


    def __repr__(self):
        return f"{str(self)}\nDinero: {round(self.dinero, 2)}"\
               f" | Lucidez: {round(self.lucidez, 2)}" \
               f" | Ansiedad: {round(self.ansiedad, 2)}" \
               f" | Suerte: {round(self.suerte, 2)}" \
               f" | Sociabilidad: {round(self.sociabilidad, 2)}" \
               f" | Stamina: {round(self.stamina, 2)}" \
               f" | Desshonestidad: {round(self.deshonestidad, 2)}"

    def __str__(self):
        return f"[Cliente {self.id}] {self.nombre}: {self.edad} años (" \
               f"{self.personality})"


    def tick(self):
        self.estadia += 1

    def siguiente_accion(self):
        prob_retirarse = 1 - self.stamina
        prob_jugar = min([self.ansiedad, 1 - prob_retirarse])
        prob_actividad = min([self.sociabilidad, 1 - prob_retirarse -
                              prob_jugar])
        prob_instalacion = 1 - (prob_retirarse + prob_actividad + prob_jugar)
        dicc_prob = {prob_retirarse: "retirarse", prob_jugar: "jugar" ,
                     prob_actividad: "actividad",
                     prob_instalacion: "instalacion"}
        lista = sorted(list(dicc_prob))
        if len(lista) < 4:
            for i in range(4 - len(lista)):
                lista.insert(0, 0.0)
        probabilidades = [lista[0], lista[0]+lista[1], sum(lista)-lista[3],
                          sum(lista)]
        prob = random()
        return dicc_prob[lista[intervalo(probabilidades, prob)]]

    def mover(self, destino):
        pass




    def valores(self, personalidad):
        tupla = Cliente.dicc_personalidades[personalidad]
        return tuple(self.valor(i) for i in tupla)

    def valor(self, nivel):
        if nivel == 0:
            numero = uniform(0, 0.3)
            while numero == 0.3:
                numero = uniform(0, 0.3)
        elif nivel == 1:
            numero = uniform(0.3, 0.7)
            while numero == 0.7:
                numero = uniform(0.3, 0.7)
        elif nivel == 2:
            numero = uniform(0.7, 1)
        return numero

    @property
    def dinero(self):
        return self._dinero

    @dinero.setter
    def dinero(self, valor):
        self._dinero = max(0, valor)
        if (self._dinero > (2 * (200 * self._dinero_inicial)) or self._dinero
                < ((self._dinero_inicial * 200) / 5))\
                and not self.ansiedad_aumentada:
            self.ansiedad += (self.ansiedad) * 0.25
            self.ansiedad_aumentada = True

    @property
    def lucidez(self):
        return self._lucidez

    @lucidez.setter
    def lucidez(self, valor):
        self._dinero = medio(0, valor, 1)

    @property
    def ansiedad(self):
        return self._ansiedad

    @ansiedad.setter
    def ansiedad(self, valor):
        self._ansiedad = medio(0, valor, 1)

    @property
    def suerte(self):
        return self._suerte

    @suerte.setter
    def suerte(self, valor):
        self._suerte = medio(0, valor, 1)

    @property
    def sociabilidad(self):
        return self._sociabilidad

    @sociabilidad.setter
    def sociabilidad(self, valor):
        self._sociabilidad = medio(0, valor, 1)

    @property
    def stamina(self):
        return self._stamina

    @stamina.setter
    def stamina(self, valor):
        self._stamina = medio(0, valor, 1)

    @property
    def deshonestidad(self):
        return self._deshonestidad

    @deshonestidad.setter
    def deshonestidad(self, valor):
        self._deshonestidad = medio(0, valor, 1)

    @property
    def tiempo_accion(self):
        return self._tiempo_accion

    @tiempo_accion.setter
    def tiempo_accion(self, valor):
        self._tiempo_accion = max(0, valor)


class Personal(Individuo, Human):
    dicc_personal = dict()

    def __init__(self, tipo, x=0, y=0, hora_inicio=datetime(1, 1, 1)):

        Individuo.__init__(self)
        Human.__init__(self, choice(list(Cliente.dicc_personalidades)), x, y)
        self.tipo = tipo
        self._tiempo_trabajo = timedelta(minutes=0)

        self.ancho = 36
        self.alto = 36

        self._tiempo_descanso = timedelta(hours = int(normalvariate(14, 5)))
        self._tiempo_diario_trabajado = timedelta(minutes=0)
        self._tiempo_diario_restante = timedelta(days=1)
        self.add_decoration("gui/assets/decoration/red.png")
        self.trabajo = 0 #hasta qué hora es el trabajo
        self.descanso = 0 #hasta qué hora es el descanso
        self.descanso = hora_inicio + timedelta(
            hours=randint(1, 18))
        self.calcular_tiempo_trabajo(self.descanso)
        self.mafia = False

    @property
    def tiempo_diario_restante(self):
        return self._tiempo_diario_restante

    @tiempo_diario_restante.setter
    def tiempo_diario_restante(self, valor):
        if valor == timedelta(minutes=0):
            self._tiempo_diario_restante = timedelta(days=1)
        else:
            self._tiempo_diario_restante = valor

    @property
    def tiempo_diario_trabajado(self):
        return self._tiempo_diario_trabajado

    @tiempo_diario_trabajado.setter
    def tiempo_diario_trabajado(self, valor):
        if self.tiempo_diario_restante in (timedelta(minutes=0), timedelta(
                days=1)):
            self._tiempo_diario_trabajado = timedelta(minutes=0)
        else:
            self._tiempo_diario_trabajado = valor

    @property
    def tiempo_trabajo(self):
        return self._tiempo_trabajo

    @tiempo_trabajo.setter
    def tiempo_trabajo(self, valor):
        if False:
            self._tiempo_trabajo = valor
        else:
            if self.tiempo_diario_trabajado + min(valor,
                                self.tiempo_diario_restante) > timedelta(hours=9):
                self._tiempo_trabajo = timedelta(hours=9) - \
                                       self.tiempo_diario_trabajado
            else:
                self._tiempo_trabajo = valor

    @property
    def tiempo_descanso(self):
        return self._tiempo_descanso

    @tiempo_descanso.setter
    def tiempo_descanso(self, valor):
        self._tiempo_descanso = medio(timedelta(hours=8), valor, timedelta(
            hours=20))

    def calcular_tiempo_trabajo(self, hora_actual):
        if self.tipo == "bartender":
            self.tiempo_trabajo = timedelta(minutes=int(triangular(360, 540,
                                                                  490)))
        elif self.tipo == "dealer":
            self.tiempo_trabajo = timedelta(minutes=int(triangular(360, 540,
                                                                  540)))
        else:
            self.tiempo_trabajo = timedelta(minutes=int(triangular(360, 500,
                                                                  420)))
        self.trabajo = hora_actual + self.tiempo_trabajo

    def calcular_tiempo_descanso(self, hora_actual):
        hora = hora_actual + self.tiempo_descanso
        minutos = hora.minute
        if minutos > 0:
            hora += (timedelta(hours=1) - timedelta(minutes=minutos))
        self.descanso = hora


    def activo(self, hora_actual):
        return self.descanso < hora_actual <= self.trabajo




    def tick(self, hora_actual):
        self.tiempo_diario_restante -= timedelta(minutes=1)
        if self.activo(hora_actual):
            self.tiempo_diario_trabajado += timedelta(minutes=1)
        if hora_actual == self.trabajo:
            self.add_decoration(None)
            self.add_decoration("gui/assets/decoration/red.png")
            self.calcular_tiempo_descanso(hora_actual)


        elif hora_actual == self.descanso:
            if not self.mafia:
                self.add_decoration(None)
                self.add_decoration("gui/assets/decoration/green.png")
            else:
                self.add_decoration(None)
                self.add_decoration("gui/assets/decoration/blue.png")
            self.calcular_tiempo_trabajo(hora_actual)

    def __repr__(self):
        return f"[PER {self.id}] {self.nombre}: {self.edad} años (" \
               f"{mayus(self.tipo)})"

class Juego:
    def __init__(self):
        self.apuesta_minima = 1
        self.id = next(id_juegos)
        self.probabilidad = 0
        self.personal = dict()
        self.duracion = randint(10, 20)
        self.pozo = 0
        self.premio = 0
        self.ganancia = 0
        self.jugadores_por_dia = 0

    def agregar_personal(self, personal):
        self.personal[personal.id] = personal

    def __repr__(self):
        return f"[JUE {self.id}] {mayus(self.__class__.__name__)}"

    @property
    def disponible(self):
        personal_activo = sum([1 for i in self.personal.values() if i.activo])
        if self.tipo == "tragamonedas":
            if personal_activo < 2:
                return False
        else:
            if personal_activo < 1:
                return False
        return True

    def cumple(self, cliente):
        apuesta = cliente.apuesta(self)
        if cliente.dinero >= apuesta and self.disponible:
            return True
        return False

class Ruleta(Juego, Game):
    colores = {0: "rojo", 1: "negro"}

    def __init__(self, x=0, y=0):
        Juego.__init__(self)
        Game.__init__(self, "ruleta", x, y)
        self.tipo = "ruleta"
        self.probabilidad = par.a
        self.ancho = 102
        self.alto = 53
        self.ubicacion = (x - 40, y + 20)


    def prob_ruleta(self, probabilidad, predecir=False, mafia=False):
        if predecir:
            return probabilidad + ((par.q / 100) * probabilidad)
        elif mafia:
            return probabilidad + ((par.k / 100) * probabilidad)
        else:
            return probabilidad


    def jugar(self, cliente, predecir=False, mafia=False):
        self.jugadores_por_dia += 1
        if sum([1 for i in self.personal.values() if i.mafia and i.activo]) >\
                0 and cliente.mafia:
            mafia = True
        apuesta = cliente.apuesta(self)
        cliente.dinero -= apuesta
        numero = choice(list(range(par.y + 1)))
        if numero:
            color = Ruleta.colores[int(numero % 2)]
        else:
            color = "verde"
        tipo_eleccion = choice(["color", "numero"])
        if tipo_eleccion == "color":
            if color == "verde":
                ganancia = apuesta * 5
                probabilidad = self.prob_ruleta((1 / (par.y + 1)), predecir,
                                                mafia)
            else:
                ganancia = apuesta * 1.5
                probabilidad = self.prob_ruleta((par.y / (2 * (par.y + 1))),
                                           predecir, mafia)
        else:
            ganancia = apuesta * 5
            probabilidad = self.prob_ruleta((1 / (par.y + 1)), predecir)
        if prob_valor(probabilidad):
            cliente.dinero += ganancia
            self.premio += (ganancia - apuesta)
            if not predecir:
                return - (ganancia - apuesta)
            else:
                if prob_valor(par.w):
                    descubrir = True
                    cliente.razon_retirada = "descubierto"
                else:
                    descubrir = False
                return (- (ganancia - apuesta), descubrir)
        else:
            self.ganancia += apuesta
            if not predecir:
                return apuesta
            else:
                if prob_valor(par.w):
                    descubrir = True
                    cliente.razon_retirada = "descubierto"
                else:
                    descubrir = False
                return (- (ganancia - apuesta), descubrir)






class Tragamonedas(Juego, Game):
    def __init__(self, x=0, y=0):
        Juego.__init__(self)
        Game.__init__(self, "tragamonedas", x, y)
        self.tipo = "tragamonedas"
        self.ancho = 148
        self.alto = 124
        self.ubicacion = (x + 52, y - 40)

    def jugar(self, cliente):
        self.jugadores_por_dia += 1
        apuesta = cliente.apuesta(self)
        if prob_valor(par.a):
            cliente.dinero += self.pozo
            self.premio += self.pozo
            self.pozo = 0
            return 0
        else:
            cliente.dinero -= apuesta
            ganancia_casino = int(0.1 * apuesta)
            self.ganancia += ganancia_casino
            ganancia_pozo = apuesta - ganancia_casino
            self.pozo += ganancia_pozo
            return ganancia_casino

class Instalacion(Building):

    def __init__(self, tipo, x=0, y=0):
        self.id = next(id_instalaciones)
        super().__init__(tipo, x, y)
        self.personal = dict()
        self._duracion = 0
        self.tipo = tipo
        self.add_decoration("gui/assets/decoration/transparent.png")
        self.clientes = deque()
        self.tiempo_sin_funcionar = 0
        self.add_decoration("gui/assets/decoration/transparent.png")
        if self.tipo == "restobar":
            self.ancho = 158
            self.alto = 170
            if x < 332:
                self.ubicacion = (x + 160, y + 70)
            else:
                self.ubicacion = (x - 40, y + 60)
            self.capacidad_maxima = 20
            self.costo = 2
        elif self.tipo == "baños":
            self.ancho = 62
            self.alto = 42
            if x < 330 and y < 200:
                self.ubicacion = (x + 15, y + 44)
            elif x < 330 and y >= 200:
                self.ubicacion = (x + 70, y + 0)
            elif x >= 330 and y < 200:
                self.ubicacion = (x + 0, y + 44)
            elif x >= 330 and y >= 200:
                self.ubicacion = (x + 10, y - 44)
            self.capacidad_maxima = 20
            self.costo = 0.2
        else:
            self.capacidad_maxima = 1
            self.ubicacion = (x - 38, y + 10)
            self.ancho = 78
            self.alto = 78
            self.costo = 10

    def duracion(self, cliente):
        if self.tipo == "restobar":
            return int(10 + ((40 / (len(self.personal) - 1)) * (
                self.personal_activo - 1)))
        elif self.tipo == "baños":
            return normal(3 * (1 - cliente.lucidez), 2)
        else:
            return normal(3, 5)

    @property
    def personal_activo(self):
        return sum([i for i in self.personal if i.activo])

    @property
    def disponible(self):
        if self.tipo in ("restobar", "tarot"):
            personal_activo = sum([1 for i in self.personal.values() if
                                   i.activo])
            if self.tipo == "restobar":
                if personal_activo < 2:
                    return False
            else:
                if personal_activo < 1:
                    return False
        return True

    def agregar_personal(self, personal):
        self.personal[personal.id] = personal

    def cumple(self, cliente):
        if len(self.clientes) < self.capacidad_maxima and self.disponible:
            return True
        return False

    def usar(self, cliente):
        if self.tipo == "restobar":
            if cliente.lucidez > cliente.ansiedad: #elige bebida
                cliente.lucidez -= 0.2
                cliente.ansiedad -= 0.15
                cliente.stamina += 0.3
            else: #elige comida
                cliente.lucidez += 0.1
                cliente.ansiedad += 0.2
        elif self.tipo == "baños":
            cliente.ansiedad -= 0.1
        else:
            respuesta = choice([False, True])
            if respuesta:
                cliente.suerte += 0.2
            else:
                cliente.stamina -= 0.1
        return self.costo

    @property
    def personal_activo(self):
        return sum([1 for i in self.personal if self.personal[i].activo])

    def tick(self, hora_actual):
        print("error en Instalación")
        if not self.disponible:
            self.tiempo_sin_funcionar += 1
        print("bien primero")
        if self.tipo == "tarot":
            for i in self.personal.values():
                if hora_actual == i.trabajo:
                    self.add_decoration(None)
                    self.add_decoration("gui/assets/decoration/transparent.png")
                elif hora_actual == i.descanso:
                    self.add_decoration(None)
                    self.add_decoration("gui/assets/decoration/green2.png")

    def __repr__(self):
        return f"[INS {self.id}] {mayus(self.tipo)}"



