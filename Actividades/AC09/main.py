import threading
import time
from itertools import chain
from random import randint, random


def desencriptar(nombre_archivo):
    """
    Esta simple (pero útil) función te permite descifrar un archivo encriptado.
    Dado el path de un archivo, devuelve un string del contenido desencriptado.
    """

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        murcielago, numeros = "murcielago", "0123456789"
        dic = dict(chain(zip(murcielago, numeros), zip(numeros, murcielago)))
        return "".join(
            dic.get(char, char) for linea in archivo for char in linea.lower())


def reparar(nebilockbottom, cracker):
        nebilockbottom.acquire()
        print(f"NebiLockbottom comenzó a ayudar a {cracker.nombre_equipo}")
        time.sleep(randint(1, 3))
        print(f"NebiLockbottom finalizó la ayuda al equipo "
              f"{cracker.nombre_equipo}")
        nebilockbottom.release()


class Equipo(threading.Thread):
    def __init__(self, nombre, nlb, mision, nombre_archivo="pista.txt"):
        super().__init__()
        self.nombre = nombre
        self.hacker = Hacker(self.nombre, nlb, nombre_archivo)
        self.cracker = Cracker(self.nombre, nlb)
        self.nlb = nlb
        self.daemon = True
        self.mision = mision

    def run(self):
        self.hacker.start()
        self.cracker.start()
        self.hacker.join()
        self.cracker.join()
        if not self.mision.ganador:
            print(f"¡Somos el equipo {self.nombre} y ganamos!")
        self.mision.ganador = True


class Hacker(threading.Thread):
    def __init__(self, equipo, nlb, nombre_archivo="pista.txt"):
        super().__init__()
        self.nombre_archivo = nombre_archivo
        self.nombre_equipo = equipo
        self.desencriptado = False

    def run(self):
        tiempo = randint(4, 12)
        time.sleep(tiempo)
        desencriptar(self.nombre_archivo)
        self.desencriptado = True
        print(f"Equipo {self.nombre_equipo}: ¡Nuestro hacker finalizó la "
              f"desencriptación!")



class Cracker(threading.Thread):
    def __init__(self, equipo, nlb):
        super().__init__()
        self.nombre_equipo = equipo
        self.lineas = 50
        self.nlb = nlb

    def run(self):
        lineas_por_minuto = randint(5, 15)
        while self.lineas > lineas_por_minuto:
            time.sleep(1)
            self.lineas -= lineas_por_minuto
            if random() <= 0.2:
                reparar(self.nlb, self)
        time.sleep(1)
        self.lineas = 0
        print(f"Equipo {self.nombre_equipo}: ¡Nuestro cracker finalizó la "
              f"escritura"
              f"del código!")
        # 50 / cantidad_lporm
        # Son 50 líneas
        # Pueden escribir de 5 a 15 líneas por minuto




class Mision:
    def __init__(self):
        print("Comenzamos la misión :D")
        self.ganador = False





    def run(self):

        nebilockbottom = threading.Lock()


        equipo_1 = Equipo("Vamosquesepuede", nebilockbottom, self)
        equipo_2 = Equipo("CRHackermens", nebilockbottom, self)
        equipo_3 = Equipo("Activity9", nebilockbottom, self)

        equipo_1.start()
        equipo_2.start()
        equipo_3.start()

        equipo_1
        equipo_2
        equipo_3

        while not self.ganador:
            pass

        for i in (equipo_1, equipo_2, equipo_3):
            print(f"{i.nombre}:")
            print(f"Su cracker escribió {50 - i.cracker.lineas} lineas")
            if i.hacker.desencriptado:
                print("Su hacker logró desencriptar el código :D")
            else:
                print("Su hacker por el momento no alcanza a desencriptar :O")






if __name__ == "__main__":
    mision = Mision()
    mision.run()

