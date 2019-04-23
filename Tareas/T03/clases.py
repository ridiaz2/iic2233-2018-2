from excepciones import InvalidQuery, ElectricalOverload, ErrorEntrada
from estructuras_de_datos import Tupla, Lista, Texto, Conjunto, Cola, \
    Listado, Diccionario
from funciones import indice, proporciones, range_, descifrar_input_conexion


#### MODIFICABLES ####

resistividad = 0.0172

######################




############################# CLASES ##########################################


class Nodo:

    tipos = Texto("G,E,T,D,C,C")

    def __init__(self, tipo, *args):
        self.id = "id"
        self.clave = tipo
        self.consumo = -1
        self.seccion_transversal = -1 #del receptor
        self.children = Lista()
        self.parent = Lista()
        self.l_children = Lista()
        self.l_parent = Lista()
        self.mij = -1
        self.demanda = -1
        self.nodo = "0"
        self.potencia = -1
        self.potencia_restante = 0
        self.potencia_0 = 0
        self.potencia_cambiada = False
        self.mij_0 = 0
        self.demanda_calculada = False
        self.potencia_previa = 0
        self.mij_previo = -1
        self.mij_0_previo = 0
        self.potencia_restante_previa = 0
        self.consumo_previo = 0


    @property
    def texto(self):
        return ""

    def volver_paso(self):
        self.consumo = self.consumo_previo
        self.potencia = self.potencia_previa
        self.mij = self.mij_previo
        self.mij_0 = self.mij_0_previo
        self.potencia_restante = self.potencia_restante_previa

    def actualizar_datos(self, datos):
        datos.actualizar(self)

    def add_children(self, id_nodo, longitud):

        if repr(self.children) == "":
            self.children += id_nodo
            self.l_children += longitud
        else:
            self.children += f":{id_nodo}"
            self.l_children += f":{longitud}"

    def add_parent(self, id_nodo, longitud, tipo="C"):

        if repr(self.parent) == "":
            self.parent += id_nodo
            self.l_parent += longitud
            if type(self) == Casa:
                self.n_parent += tipo
        else:
            self.parent += f":{id_nodo}"
            self.l_parent += f":{longitud}"
            if type(self) == Casa:
                self.n_parent += f":{tipo}"



    def calcular_demanda(self):
        #print(self, self.demanda_calculada)
        if self.demanda_calculada:
            return float(self.demanda)

        elif len(self.children) == 0:
            self.demanda = self.consumo
            if type(self) == Casa:
                self.demanda = str(float(self.demanda))
            self.demanda_calculada = True
            #print(self.demanda)
            return float(self.demanda)

        else:
            suma = float(self.consumo)
            if type(self) == Casa:
                suma = float(self.consumo)
            for n in self.children:
                nodo = n[0]
                longitud = float(n[1])
                if nodo.mij == -1:
                    demanda_j = nodo.calcular_demanda()
                    cantidad_conexiones = len(nodo.parent)
                    valor_actual = (demanda_j / cantidad_conexiones) / (1 -
                                                    (resistividad * longitud) /
                                                    nodo.seccion_transversal)
                    nodo.mij = str(valor_actual)
                else:
                    valor_actual = float(nodo.mij)
                suma += valor_actual
            self.demanda = suma
            self.demanda_calculada = True
            #print(self.demanda)
            return suma

class Generadora(Nodo):
    def __init__(self, datos, tipo="G", inicio=True):
        super().__init__(tipo)
        if inicio:
            valores = Lista()
            for elemento in datos.items():
                valores.agregar(elemento[1])
        else:
            valores = datos

        self.id, self.nombre, self.sistema, self.provincia, self.comuna, \
            self.tipo, self.potencia = valores

        self.consumo = 0

        if self.sistema == "AYSEN":
            self.sistema = "SEA"
        elif self.sistema == "MAGALLANES":
            self.sistema = "SEM"

        self.potencia = float(self.potencia) * 1000

        self.nodo_parent = "G"
        self.nodo = "G"
        self.nodo_children = "E"
        self.clase = "Generadora"



    def __repr__(self):
        return f"CentralGeneradora(id={self.id}, nombre={self.nombre}, " \
               f"sistema={self.sistema}, provincia={self.provincia}, comuna=" \
               f"{self.comuna}, tipo={self.tipo}, potencia={self.potencia}, " \
               f"demanda={self.demanda}\n" \
               f"Subnodos: {repr(self.children)}"

    def __str__(self):
        return f"Central Generadora {self.id} '{self.nombre}' (" \
               f"{self.sistema}, " \
               f"{self.provincia}, " \
               f"{self.comuna}, {self.tipo})"

    @property
    def texto(self):
        return f"{self.id},{self.nombre.replace(',', '+')},{self.sistema}," \
               f"{self.provincia}," \
               f"{self.comuna},{self.tipo},{self.potencia},{self.consumo}," \
               f"({self.children}),({self.l_children}),[{self.parent}]," \
               f"[{self.l_parent}],{self.mij},{self.demanda}"

class Estacion(Nodo):
    def __init__(self, datos, tipo, inicio=True):
        super().__init__(tipo)
        if inicio:
            valores = Lista()
            for elemento in datos.items():
                valores.agregar(elemento[1])
        else:
            valores = datos

        self.id, self.nombre, self.sistema, self.provincia, self.comuna, \
            self.consumo_datos = valores

        if self.consumo in Tupla(-1, "-1"):
            self.consumo = self.consumo_datos

        self.nodo = tipo

        if tipo == "E":
            self.tipo = "Estacion Elevadora"
            self.seccion_transversal = 253
        elif tipo == "T":
            self.tipo = "Subestacion de Transmisión"
            self.seccion_transversal = 202.7
        elif tipo == "D":
            self.tipo = "Subestación de Distribución"
            self.seccion_transversal = 152

        if self.sistema == "AYSEN":
            self.sistema = "SEA"
        elif self.sistema == "MAGALLANES":
            self.sistema = "SEM"

        self.clase = self.tipo
        self.nodo_parent = Nodo.tipos[Nodo.tipos.find(self.nodo) - 1]
        self.nodo_children = Nodo.tipos[Nodo.tipos.find(self.nodo) + 1]

        self.consumo = float(self.consumo) * 1000
        self.consumo_previo = self.consumo

    @property
    def potencia_elevadora(self):
        suma = 0
        for central in self.parent:
            suma += float(central[0].potencia)
        return suma

    def __repr__(self):
        return f"{self.tipo.replace(' ', '')}" \
               f"(id={self.id}, nombre={self.nombre}, sistema=" \
               f"{self.sistema}, provincia={self.provincia}, comuna=" \
               f"{self.comuna}, consumo={self.consumo}, demanda=" \
               f"{self.demanda}\n" \
               f"Subnodos: {repr(self.children)}\n" \
               f"Supernodos: {repr(self.parent)}"

    def __str__(self):
        return f"{self.tipo} {self.id} '{self.nombre}' ({self.sistema}, " \
               f"{self.provincia}, " \
               f"{self.comuna})"

    @property
    def texto(self):
        return f"{self.id},{self.nombre},{self.sistema},{self.provincia}," \
               f"{self.comuna},{self.consumo_datos},{self.consumo}," \
               f"({self.children}),({self.l_children}),[{self.parent}]," \
               f"[{self.l_parent}],{self.mij},{self.demanda}"



class Casa(Nodo):
    def __init__(self, datos, tipo="C", inicio=True):
        super().__init__(tipo)
        if inicio:
            valores = Lista()

            for elemento in datos.items():
                valores.agregar(elemento[1])
        else:
            valores = datos

        self.id, self.sistema, self.provincia, self.comuna, \
            self.consumo_datos = valores

        if self.sistema == "AYSEN":
            self.sistema = "SEA"
        elif self.sistema == "MAGALLANES":
            self.sistema = "SEM"


        if self.consumo in Tupla(-1, "-1"):
            self.consumo = self.consumo_datos

        self.seccion_transversal = 85

        self.nodo_parent = "D"
        self.nodo = "C"
        self.nodo_children = "C"
        self.clase = "Casa"

        self.consumo = float(self.consumo)
        self.consumo_previo = self.consumo

    def __repr__(self):
        return f"Casa(id={self.id}, sistema={self.sistema}, provincia=" \
               f"{self.provincia}, comuna={self.comuna}, consumo=" \
               f"{self.consumo}, demanda={self.demanda}\n" \
               f"Subnodos: {repr(self.children)}\n" \
               f"Supernodos: {repr(self.parent)}"

    def __str__(self):
        return f"Casa {self.id} ({self.sistema}, {self.provincia}, " \
               f"{self.comuna})"

    @property
    def texto(self):
        return f"{self.id},{self.sistema},{self.provincia}," \
               f"{self.comuna},{self.consumo_datos},{self.consumo}," \
               f"({self.children}),({self.l_children}),[{self.parent}]," \
               f"[{self.l_parent}],{self.mij},{self.potencia},{self.demanda}," \
               f"<{self.n_parent}>"


