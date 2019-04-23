class Aventurero:
    def __init__(self, nombre, vida, ataque, velocidad):
        self.nombre = nombre
        self._vida = vida
        self.ataque = ataque
        self.velocidad = velocidad

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor):
        if valor < 0:
            self._vida = 0
        elif valor > 100:
            self._vida = 100

    @property
    def poder(self):
        return sum([int(i) for i in [self._vida, self.ataque, self.velocidad]])

    def grito_de_guerra(self):
        print(f"{self.nombre}: ¡Gloria al gran Tini!")

class Guerrero(Aventurero):
    def __init__(self, nombre, vida, ataque, velocidad, defensa):
        super().__init__(self, nombre, vida, ataque, velocidad)
        self.defensa = defensa

    @property
    def poder(self):
        return sum([x*y for (x, y) in zip([0.8, 2.2, 1.5, 0.5], [self.vida,
                                                         self.ataque,
                                          self.defensa, self.velocidad])])

class Mago(Aventurero):
    def __init__(self, nombre, vida, ataque, velocidad, magia):
        super().__init__(self, nombre, vida, ataque, velocidad)
        self. magia = magia

    @property
    def poder(self):
        return vida + sum([x*y for (x, y) in zip([0.1, 2.5, 1.4], [self.ataque,
                                                         self.magia,
                                          self.velocidad])])


class Monstruo:
    def __init__(self, nombre, vida, poder, jefe):
        self.nombre = nombre
        self._vida = vida
        self._poder = poder
        self.jefe = jefe

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor):
        if valor < 0:
            self._vida = 0

    @property
    def poder(self):
        if jefe:
            return self._poder * 3
        else:
            return self._poder

class Clan:
    def __init__(self, nombre):
        self.nombre = nombre
        self.aventureros = []

    @property
    def rango(self):
        lista = [(0, 2, "Bronce"), (3, 5, "Plata")]
        for _rango in lista:
            if _rango[0] < len(self.aventureros) < _rango[1]:
                return _rango[2]
        return "Oro"

    @property
    def poder(self):
        return sum([aventurero.poder for aventurero in self.aventureros]) * \
        self.rango

    def agregar(self, entidad):
        if type(entidad) == self.__class__.__name__:
            self.aventureros.append(entidad)
        elif type(entidad) == Monstruo:
            print("No es posible agregar monstruos a los clanes")
        elif type(entidad) == Aventurero:
            print("No es posible agregar personas a las mazmorras")

    def remover(self, entidad):
        if entidad in self.aventureros:
            self.aventureros.remove(entidad)

        else:
            print("Entidad no encontrada")

    def __add__(self, other):
        if self.__class__.__name__ == other.__class__.__name__:
            lista = self.aventureros.copy()
            lista.extend(other.aventureros)
            if self.__class__.__name__ == Clan:
                nuevo = Clan(self.nombre+other.nombre)
            else:
                nuevo = Mazmorra(self.nombre+other.nombre)
            for i in lista:
                nuevo.agregar(i)
            return nuevo

    def __str__(self):
        return f"{self.nombre}, {self.poder}, {self.rango}, {str(len("
              f"self.aventureros))}")

class Mazmorra(Clan):
    def __init__(self, nombre):
        super().__init__(self, nombre)

    @property
    def rango(self):
        return 1

    @property
    def monstruos(self):
        return self.aventureros


