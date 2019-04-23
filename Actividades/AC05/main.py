# Aqui abajo debes escribir el código de tus clases
from abc import ABC, abstractmethod
from collections import namedtuple

class Individuo(ABC):
    def __init__(self, nombre, vida, ki, fuerza, resistencia, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self._vida = vida
        self.ki = ki
        self.fuerza = fuerza
        self.resistencia = resistencia

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor):
        if valor < 0:
            self._vida = 0
        else:
            self._vida = valor

    @abstractmethod
    def atacar(self, enemigo):
        pass

class Humano(Individuo):
    def __init__(self, nombre, vida, ki, fuerza, resistencia):
        super().__init__(nombre, vida, ki, fuerza, resistencia)
        self._inteligencia = 100

    @property
    def inteligencia(self):
        return self._inteligencia

    @inteligencia.setter
    def inteligencia(self, valor):
        if valor < 0:
            self._inteligencia = 0
        else:
            self._inteligencia = valor

    def atacar(self, enemigo):
        #print("Atacando como Humano")
        perdida = max(self.ki * (1 + enemigo.fuerza - enemigo.resistencia)/2, 0)
        enemigo.vida -= perdida
        print(f"{self.nombre} le quita {perdida} de vida a "
              f"{enemigo.nombre}")

    def meditar(self):
        self.ki += (self.inteligencia / 100)
        print(f"¡Yo, {self.nombre} estoy meditando!")

class Extraterrestre(Individuo):
    def __init__(self, nombre, vida, ki, fuerza, resistencia):
        super().__init__(nombre, vida, ki, fuerza, resistencia)

    def atacar(self, enemigo):
        #print("Atacando como Extraterrestre")
        perdida = max(self.ki * (1 + self.fuerza - enemigo.resistencia), 0)
        enemigo.vida -= perdida
        print(
            f"{self.nombre} le quita {perdida} de vida a {enemigo.nombre}")
        self.fuerza += (0.3 * self.fuerza)


class Supersaiyayin(Extraterrestre, Humano):
    def __init__(self, nombre, vida, ki, fuerza, resistencia):
        super().__init__(nombre, vida, ki, fuerza, resistencia)
        self._cola = True

    @property
    def cola(self):
        return self._cola

    @cola.setter
    def cola(self, booleano):
        if booleano != True and booleano != False:
            pass
        else:
            self._cola = booleano

    def perder_cola(self):
        if not self.cola:
            print(f"Actualmente, {self.nombre} no tiene cola")
            print("Entonces no puede perderla jeje")
        else:
            self.cola = False
            self.resistencia -= (0.6 * self.resistencia)

class Hakashi(Extraterrestre):
    def __init__(self, nombre, vida, ki, fuerza, resistencia):
        super().__init__(nombre, vida, ki, fuerza, resistencia)

    def robar_ki(self, *adversarios):
        for enemigo in adversarios:
            ki_robado = 0.5 * enemigo.ki
            enemigo.ki -= (ki_robado)
            self.ki += ki_robado


if __name__ == '__main__':
    """
    A continuación debes instanciar cada uno de los objetos pedidos,
    para que puedas simular la batalla.
    """
    Videl = Humano("Videl", 10000, 200, 1000, 10000)
    Gohan = Supersaiyayin("Gohan", 10000, 8000, 8000, 10000)
    Krillin = Humano("Krillin", 10000, 200, 1000, 10000)
    Goku = Supersaiyayin("Goku", 10000, 10000, 10000, 10000)
    Vegeta = Supersaiyayin("Vegeta", 10000, 10000, 10000, 10000)
    Trunks = Supersaiyayin("Trunks", 10000, 8000, 8000, 10000)
    Freezer = Hakashi("Freezer", 100000, 10000, 10000, 10000)
    Cell = Hakashi("Cell", 100000, 10000, 10000, 10000)

    '''
    #Lo siguiente es porque me quedó algo de tiempo c:
    Personajes = [Videl, Gohan, Krillin, Goku, Vegeta, Trunks, Freezer, Cell]
    print("Bienvenid@ a DragonCCball")
    while True:
        print("Seleccione un Personaje")
        for i, j in enumerate(Personajes):
            print(f"[{i+1}] {j.nombre}")
        seleccion = input()
        while seleccion not in list("12345678"):
            print("Por favor ingrese el valor de nuevo :D")
            seleccion = input()
        seleccion = int(seleccion) - 1
        personaje = Personajes[seleccion]
        print(f"Personaje seleccionado: {personaje.nombre}")
        if type(personaje) == Humano:
            print("Humano")
        elif type(personaje) == Supersaiyayin:
            print("Supersaiyayin")
        elif type(personaje) == Hakashi:
            print("Hakashi")
        #No alcancé a hacer mucho jeje :D
    '''