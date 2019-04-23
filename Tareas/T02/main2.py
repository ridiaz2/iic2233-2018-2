from classes2 import *
from gui.entities import Human, Game, _SCALE
from datetime import datetime, timedelta
from parameters import parametros as par
from collections import deque
from statistics import mean as promedio
from os.path import isfile


gui.init()

_PATH = os.path.dirname(os.path.abspath(__file__))

def conservar_angulos(*objetos):
    for i in objetos:
        i.angle = i.angle

def texto(string):
    return string

class Simulacion:

    def __init__(self, casino=Casino()):
        self.casino = casino
        self.hora = datetime(1, 1, 1)


    def add_client(self, x=30, y=10, personalidad=[]):
        if not personalidad:
            personalidad = choice(list(Cliente.dicc_personalidades))
        cliente = self.casino.agregar_cliente(personalidad, x, y)
        gui.add_entity(cliente)
        cliente.setFixedSize(73 * _SCALE, 73 * _SCALE)
        return cliente

    def add_something(self, tipo, x=0, y=0, angulo=0, agregar=True):
        if tipo in ("tragamonedas", "ruleta"):
            funcion = self.casino.agregar_juego
        else:
            funcion = self.casino.agregar_instalacion
        objeto = funcion(tipo, x, y)
        if angulo:
            objeto.angle = angulo
        gui.add_entity(objeto)
        id_ = objeto.id
        if tipo == "ruleta":
            simulacion.add_staff("dealer", x-5, y-30, id_)
            simulacion.add_staff("dealer", x+15, y-40, id_)
            simulacion.add_staff("dealer", x+40, y-40, id_)
            simulacion.add_staff("dealer", x+65, y-40, id_)
            simulacion.add_staff("dealer", x+25, y-20, id_)
            simulacion.add_staff("dealer", x+50, y-20, id_)
            simulacion.add_staff("dealer", x+75, y-20, id_)
            simulacion.add_staff("dealer", x+90, y-40, id_)
            simulacion.add_staff("dealer", x+100, y-20, id_)
        elif tipo == "tragamonedas":
            simulacion.add_staff("dealer", x - 32, (y + 20) + (50 * 2), id_)
            simulacion.add_staff("dealer", x + 140, (y + 20) + (50 * 2), id_)
            for i in range(3):
                simulacion.add_staff("dealer", x - 7, (y + 20) + (50 * i), id_)
                simulacion.add_staff("dealer", x + 18, (y + 20) + (50 * i), id_)
                simulacion.add_staff("dealer", x + 43, (y + 20) + (50 * i), id_)
                simulacion.add_staff("dealer", x + 67, (y + 20) + (50 * i), id_)
                simulacion.add_staff("dealer", x + 91, (y + 20) + (50 * i), id_)
                simulacion.add_staff("dealer", x + 115, (y + 20) + (50 * i),
                                     id_)
                simulacion.add_staff("dealer", x - 32, (y - 5) + (50 * i), id_)
                simulacion.add_staff("dealer", x + 140, (y - 5) + (50 * i), id_)

        elif tipo == "tarot":
            objeto.agregar_personal(self.casino.agregar_personal("mrt", x, y))


        elif tipo == "restobar":
            simulacion.add_staff("bartman", x + 22, y + 20, id_)
            simulacion.add_staff("bartman", x + 47, y + 20, id_)
            simulacion.add_staff("bartman", x + 72, y + 20, id_)
            simulacion.add_staff("bartman", x + 97, y + 20, id_)
            simulacion.add_staff("bartman", x - 10, y + 20, id_)
            simulacion.add_staff("bartman", x + 129, y + 20, id_)
            simulacion.add_staff("bartman", x - 10, y + 50, id_)
            simulacion.add_staff("bartman", x + 129, y + 50, id_)

            if agregar:
                simulacion.add_staff("bartman", x, y + 70, id_)
                simulacion.add_staff("bartman", x + 24, y + 70, id_)
                simulacion.add_staff("bartman", x + 52, y + 110, id_)
                simulacion.add_staff("bartman", x + 74, y + 110, id_)
            else:
                simulacion.add_staff("bartman", x + 119, y + 70, id_)
                simulacion.add_staff("bartman", x + 95, y + 70, id_)
                simulacion.add_staff("bartman", x + 63, y + 110, id_)

            simulacion.add_staff("bartman", x - 10, y + 90, id_)
            simulacion.add_staff("bartman", x + 14, y + 90, id_)
            simulacion.add_staff("bartman", x + 38, y + 90, id_)
            simulacion.add_staff("bartman", x + 105, y + 90, id_)
            simulacion.add_staff("bartman", x + 81, y + 90, id_)
            simulacion.add_staff("bartman", x + 129, y + 90, id_)

            simulacion.add_staff("bartman", x - 10, y + 110, id_)
            simulacion.add_staff("bartman", x + 30, y + 110, id_)
            simulacion.add_staff("bartman", x + 129, y + 110, id_)
            simulacion.add_staff("bartman", x + 96, y + 110, id_)

            simulacion.add_staff("bartman", x - 10, y + 140, id_)
            simulacion.add_staff("bartman", x + 14, y + 140, id_)
            simulacion.add_staff("bartman", x + 38, y + 140, id_)
            simulacion.add_staff("bartman", x + 105, y + 140, id_)
            simulacion.add_staff("bartman", x + 81, y + 140, id_)
            simulacion.add_staff("bartman", x + 129, y + 140, id_)
        return objeto

    def add_staff(self, tipo, x=0, y=0, lugar=-1):
        personal = self.casino.agregar_personal(tipo, x, y)

        if lugar != -1:
            if tipo in ("dealer"):
                objeto = self.casino.juegos[lugar]
            else:
                objeto = self.casino.instalaciones[lugar]
            if type(objeto) == Ruleta:
                if prob_valor(par.j):
                    personal.mafia = True
            objeto.agregar_personal(personal)
        gui.add_entity(personal)
        return personal

    def tick(self):
        self.hora += timedelta(minutes=1)
        print(self.hora)
        if self.hora.hour == 0 and self.hora.day > 1:
            self.casino.ganancias.append(self.casino.dinero_por_dia)
            self.casino.dinero_por_dia = 0
            for instalacion in self.casino.juegos.values():

                self.casino.jugadores[instalacion.id].append(
                    instalacion.jugadores_por_dia)
                instalacion.jugadores_por_dia = 0

        if self.hora.day - 1 == par.duracion:
            self.estadisticas()
            raise SystemExit
        conservar_angulos(*(list(self.casino.juegos.values()) + list(
            self.casino.personal.values()) + list(
            self.casino.clientes.values()) + list(
            self.casino.instalaciones.values())))
        print("agre cliente")
        if prob_valor(par.p):
            self.add_client()
        print("cliente_agrergado")
        for i in self.casino.personal.values():
            i.tick(self.hora)
        print("tick personal listo")
        for i in self.casino.instalaciones.values():
            i.tick(self.hora)
        print("ticks listos :D", self.hora.minute)
        if self.hora.minute == 0:
            print(f"Día {self.hora.day} {str(self.hora)[11:]}")

        for i in self.casino.clientes.values():
            print(i, len(self.casino.clientes))
            if not i.fuera:
                print("fuera")
                i.tick()
                print("tick")
                print("siguiente_accion 0")
                self.casino.siguiente_accion(i)
                print("siguiente_accion 1")
                if i.accion:
                    print("mover_cliente 0")
                    print(i.destino, i.x, i.y, self.casino.camino(i))
                    self.casino.mover_cliente(i, self.casino.camino(i))
                print("mover_cliente 1")
            if not i.fuera and i.accion:
                print("realizar accion 0")
                self.casino.realizar_accion(i)
                print("realizar_accion 1")

    def marcar_mapeo(self):
        for i in range(0, len(self.casino.espacios_ocupados), 2):
            i1 = self.casino.espacios_ocupados[i]
            pixel_ = Pixel(i1[0], i1[1])
            gui.add_entity(pixel_)
            self.casino.pixeles.append(pixel_)

    def estadisticas(self):
        #1. Promedio diferencia dinero por cliente:
        #2. Promedio diferencia dinero por personalidad:
        print("hola")
        din_ludo, din_kibit, din_gan, din_mill, din_dieci = [[] for i in
                                                             range(5)]
        est_ludo, est_kibit, est_gan, est_mill, est_dieci = [[] for i in
                                                             range(5)]
        dicc_perso = {"ludopata": din_ludo, "kibitzer": din_kibit, "ganador":
            din_gan, "millonario": din_mill, "dieciochero": din_dieci}
        dicc_est = {"ludopata": est_ludo, "kibitzer": est_kibit, "ganador":
            est_gan, "millonario": est_mill, "dieciochero": est_dieci}
        estadia = []
        diferencias_dinero = []
        razon_descubierto = 0
        razon_retiro = 0
        for cliente in self.casino.clientes.values():

            diferencias_dinero.append(cliente.dinero - (cliente._dinero_inicial
                                                     * 200))

            dicc_perso[cliente.personalidad].append(cliente.dinero -
                                                    (cliente._dinero_inicial
                                                     * 200))

            estadia.append(cliente.estadia)
            dicc_est[cliente.personalidad].append(cliente.estadia)
            if cliente.fuera:
                if cliente.razon_retirada == "descubierto":
                    razon_descubierto += 1
                elif cliente.razon_retirada == "retiro":
                    razon_retiro += 1
        promedio_estadia = int(promedio(estadia))
        promedio_din = round(promedio(diferencias_dinero), 2)
        uno = (f"1. En promedio, las diferencias de dinero de los clientes " +
              f"es de {promedio_din}")
        print(uno)
        dos = ("2. El promedio de diferencia de dinero por personalidad es " \
             "de:\n" +
            f"   * Ludópatas: {round(promedio(din_ludo), 2)}\n" +
            f"   * Kibitzers: {round(promedio(din_kibit), 2)}\n" +
            f"   * Dieciocher@s: {round(promedio(din_dieci), 2)}\n" +
            f"   * Ganadores: {round(promedio(din_gan), 2)}\n" +
            f"   * Millonari@s: {round(promedio(din_mill), 2)}")
        print(dos)
        tres = (f"3. En promedio, los clientes permanecieron en el casino " +
                f"por {promedio_estadia} minutos.")
        print(tres)

        cuatro = texto(f"4. En promedio, la estadía por personalidad de "
                       f"los clientes es de:\n" + \
                    f"   * Ludópatas: {int(promedio(est_ludo))}\n" + \
                    f"   * Kibitzers: {int(promedio(est_kibit))}\n" + \
                    f"   * Dieciocher@s: {int(promedio(est_dieci))}\n" + \
                    f"   * Ganadores: {int(promedio(est_gan))}\n" + \
                    f"   * Millonari@s: {int(promedio(est_mill))}")
        print(cuatro)
        cinco = (f"5. En promedio, el casino ganó " + \
              f"{round(promedio(self.casino.ganancias), 2)}")
        print(cinco)
        proporcion_ganancias_premios = []
        for juego in self.casino.juegos.values():
            if juego.ganancia + juego.premio == 0:
                proporcion_ganancias_premios.append((juego, 0))
            else:
                proporcion_ganancias_premios.append((juego, juego.ganancia / (
                    juego.ganancia + juego.premio)))
        juego_mayor = max(proporcion_ganancias_premios, key=lambda i: i[1])[0]


        seis = (f"6. El juego que generó mayor ganancia es: " + \
              f"{mayus(juego_mayor.tipo)} (id = {juego_mayor.id})")

        print(seis)
        # 7. porcentaje contó cartas
        total_clientes = len(self.casino.clientes)
        total_conteo = sum([1 for i in self.casino.clientes.values() if
                            i.contar])
        porcentaje = (total_conteo / total_clientes) * 100
        siete = (f"7. Un {porcentaje}% de los clientes contó cartas.")
        print(siete)

        if razon_retiro + razon_descubierto == 0:
            porcentaje_descubierto, porcentaje_voluntario = 0, 0
        else:
            porcentaje_voluntario = round((razon_retiro / (razon_retiro +
                                                razon_descubierto)) * 100, 2)
            porcentaje_descubierto = 100 - porcentaje_voluntario
        ocho = ("8. Los porcentajes de salida del casino son:" + \
                f"\n   * Retiro voluntario: {porcentaje_voluntario}%" + \
                f"\n   * Retiro por predecir: {porcentaje_descubierto}%")
        print(ocho)
        nueve = ("9. Los minutos sin funcionar de cada instalacion " \
                    "corresponden a:")
        for instalacion in self.casino.instalaciones.values():
            nueve += (f"\n   * {mayus(instalacion.tipo)} (id = " \
                      f"{instalacion.id}): {instalacion.tiempo_sin_funcionar}")
        print(nueve)
        diez = ("10. En promedio, la cantidad diario de jugadores por cada " + \
              "espacio es:")
        for juego in self.casino.juegos.values():
            promedio_jugadores = int(promedio(self.casino.jugadores[juego.id]))
            diez += (f"\n   * {mayus(juego.tipo)} (id = {juego.id}): " + \
                    f"{promedio_jugadores}")
        print(diez)
        self.guardar([uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve,
                   diez])

    def guardar(self, lineas):
        print("A continuación puede escribir el nombre del archivo en "
                  "donde quiere guardar los datos :D")
        print("[Enter] para guardar en (output.txt) c:")
        ruta = input()
        if ruta == "":
            ruta = "output.txt"
        hoy = str(datetime.today())[:-7]
        if isfile(ruta):
            archivo = open(ruta, encoding="utf-8", mode="a")
            archivo.write("\n")
            archivo.write(hoy)
            archivo.write("\n")
            for i in lineas:
                archivo.write(i)
                archivo.write("\n")
            archivo.close()
            print("Datos guardados con éxito :D")
        else:
            archivo = open(ruta, mode="w")
            archivo.close()
            archivo = open(ruta, encoding="utf-8", mode="a")
            archivo.write(hoy)
            archivo.write("\n")
            for i in lineas:
                archivo.write(i)
                archivo.write("\n")
            archivo.close()
            print("Datos guardados con éxito :D")





    def run(self):
        gui.set_size(773, 485)
        self.casino.mapeo()
        gui.run(self.tick, 1)

simulacion = Simulacion()
client = Cliente("ludopata")
client2 = Cliente("ludopata")
client.add_decoration("gui/assets/decoration/gris2.png")
traga1 = Game("tragamonedas", 30, 30)
traga2 = Game("tragamonedas", 200, 200)


tragamonedas1 = simulacion.add_something("tragamonedas", 280, 300)


ruleta1 = simulacion.add_something("ruleta", 240, 60)
ruleta2 = simulacion.add_something("ruleta", 390, 60)
ruleta3 = simulacion.add_something("ruleta", 240, 160)
ruleta4 = simulacion.add_something("ruleta", 400, 160)
restobar1 = simulacion.add_something("restobar", 40, 230, agregar=True)
restobar2 = simulacion.add_something("restobar", 580, 20, agregar=False)
tarot1 = simulacion.add_something("tarot", 658, 200, 90)
tarot2 = simulacion.add_something("tarot", 658, 290, 90)
tarot3 = simulacion.add_something("tarot", 658, 380, 90)
baño1 = simulacion.add_something("baños", 120, 20)
baño2 = simulacion.add_something("baños", 40, 410)
baño3 = simulacion.add_something("baños", 530, 410)
baño4 = simulacion.add_something("baños", 520, 20)


simulacion.run()
