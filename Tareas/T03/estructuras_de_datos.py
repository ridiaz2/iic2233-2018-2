


def range_(*args, **kwargs):
    #https://stackoverflow.com/questions/9252543/
    #importerror-cannot-import-name-x
    from funciones import range_ as range_0
    return range_0(*args, **kwargs)


class Vertice:
    def __init__(self, valor=None):
        """Inicializa la estructura del nodo"""
        self.valor = valor
        self.siguiente = None
        self.llave = ""

    def __repr__(self):
        if self.llave:
            return f"{self.llave}: {repr(self.valor)}"
        return repr(self.valor)

    def __str__(self):
        if self.llave:
            return f"{self.llave}: {str(self.valor)}"
        return str(self.valor)

class Lista:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def agregar(self, nuevo):
        if type(nuevo) != Vertice:
            nuevo = Vertice(nuevo)

        if not self.cabeza:
            self.cabeza = nuevo
            self.cola = self.cabeza
        else:
            self.cola.siguiente = nuevo
            self.cola = self.cola.siguiente

    def obtener(self, posicion):
        nodo_actual = self.cabeza

        for i in range_(posicion):
            if nodo_actual:
                nodo_actual = nodo_actual.siguiente

        if not nodo_actual:
            return "Posición no encontrada"
        return nodo_actual

    def __getitem__(self, posicion):
        return self.obtener(posicion).valor

    def suma(self):
        sumatoria = 0
        for i in self:
            # https://stackoverflow.com/questions/354038/
            # how-do-i-check-if-a-string-is-a-number-float
            # Comentario 52
            if type(i) == str:
                if i.replace('.', '', 1).isnumeric():
                    sumatoria += float(i)
            elif type(i) == int or type(i) == float:
                sumatoria += float(i)
        return sumatoria

    def remove(self, elemento, funcion):
        encontrado = False
        nodo_actual = self.cabeza
        # Caso Primero
        if len(self) == 0:
            return

        elif funcion(nodo_actual.valor) == elemento:
            if self.cola == self.cabeza:
                self.cola = None
            elif len(self) == 1:
                return
            self.cabeza = self.cabeza.siguiente
            return

        while not encontrado and nodo_actual:
            nodo_valor = nodo_actual.valor
            if funcion(nodo_valor) == elemento:
                encontrado = True
                nodo_previo.siguiente = nodo_actual.siguiente
            nodo_previo = nodo_actual
            nodo_actual = nodo_actual.siguiente
        return

    def insertar(self, valor, posicion):
        nodo_nuevo = Vertice(valor)
        nodo_actual = self.cabeza

        # Caso particular: insertar en la cabeza
        if posicion == 0:
            nodo_nuevo.siguiente = self.cabeza
            self.cabeza = nodo_nuevo
            # Caso más particular. Si era el primer nodo, actualizamos la cola
            if nodo_nuevo.siguiente is None:
                self.cola = nodo_nuevo
            return

        for i in range_(posicion - 1):
            if nodo_actual:
                nodo_actual = nodo_actual.siguiente

        if nodo_actual is not None:
            nodo_nuevo.siguiente = nodo_actual.siguiente
            nodo_actual.siguiente = nodo_nuevo
            # Caso particular: si es que insertamos en la última posición
            if nodo_nuevo.siguiente is None:
                self.cola = nodo_nuevo

    def descomprimir(self, posicion):
        lista = Lista()
        for i in self:
            lista.agregar(i[posicion])
        return lista

    def __iter__(self):
        nodo_actual = self.cabeza
        while nodo_actual:
            yield nodo_actual.valor
            nodo_actual = nodo_actual.siguiente

    def __len__(self):
        largo = 0
        nodo_actual = self.cabeza
        while nodo_actual:
            largo += 1
            nodo_actual = nodo_actual.siguiente
        return largo

    def __repr__(self):
        string = ""
        nodo_actual = self.cabeza
        while nodo_actual:
            string = f"{string}{nodo_actual.valor}, "
            nodo_actual = nodo_actual.siguiente
        return f"[{string[:-2]}]"

    def agrupar(self, other):
        grupo = Lista()
        for i in range_(min(len(self), len(other))):
            grupo.agregar(Lista())

class Diccionario(Lista):
    def __init__(self, datos=""):
        super().__init__()
        if datos:
            for elemento in datos:
                self[elemento[0]] = elemento[1]

    def __setitem__(self, llave, valor):
        nodo = Vertice(valor)
        nodo.llave = llave
        self.agregar(nodo)

    def pop(self, llave):
        encontrado = False
        nodo_actual = self.cabeza
        # Caso Primero
        if len(self) == 0:
            return

        elif nodo_actual.llave == llave:
            if self.cola == self.cabeza:
                self.cola = None
            elif len(self) == 1:
                return nodo_actual
            self.cabeza = self.cabeza.siguiente
            return nodo_actual

        nodo_pop = None
        while not encontrado and nodo_actual:
            nodo_valor = nodo_actual.llave
            if nodo_valor == llave:
                encontrado = True
                nodo_pop = nodo_actual
                nodo_previo.siguiente = nodo_actual.siguiente
            nodo_previo = nodo_actual
            nodo_actual = nodo_actual.siguiente
        return nodo_pop

    def llaves(self):
        lista = Lista()
        nodo_actual = self.cabeza
        while nodo_actual:
            lista.agregar(nodo_actual.llave)
            nodo_actual = nodo_actual.siguiente
        return lista

    def existe(self, llave):
        from excepciones import InvalidQuery
        try:
            self[llave]
        except KeyError:
            return False
        except InvalidQuery:
            return False
        else:
            return True

    def llave_random(self):
        return str(int(max(self.llaves(), key=int)) + 1)


    def valores(self):
        lista = Lista()
        nodo_actual = self.cabeza
        while nodo_actual:
            lista.agregar(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente
        return lista

    def __iter__(self):
        nodo_actual = self.cabeza
        while nodo_actual:
            yield nodo_actual
            nodo_actual = nodo_actual.siguiente

    def __repr__(self):
        string = ""
        nodo_actual = self.cabeza
        while nodo_actual:
            string = f"{string}{nodo_actual.llave}: {repr(nodo_actual.valor)}, "
            nodo_actual = nodo_actual.siguiente
        return f"({string[:-2]})"

    def __str__(self):
        string = ""
        nodo_actual = self.cabeza
        while nodo_actual:
            string = f"{string}{nodo_actual.llave}: {str(nodo_actual.valor)}, "
            nodo_actual = nodo_actual.siguiente
        return f"({string[:-2]})"

    def __getitem__(self, llave):
        from excepciones import InvalidQuery
        from clases import Nodo
        if type(llave) == int:
            llave = str(llave)
        for nodo in self:
            if nodo.llave == llave:
                return nodo.valor
        if isinstance(self.cabeza.valor, Nodo):
            raise InvalidQuery(llave, self.cabeza.valor.nodo)
        raise KeyError(llave)

class DiccionarioPorDefecto(Diccionario):
    def __init__(self, tipo=str):
        super().__init__()
        self.por_defecto = tipo

    def __getitem__(self, llave):
        if type(llave) == int:
            llave = str(llave)
        for nodo in self:
            if nodo.llave == llave:
                return nodo.valor
        self[llave] = self.por_defecto()
        return self[llave]

class Tupla(Lista):
    def __init__(self, *args):
        super().__init__()
        for arg in args:
            self.agregar(arg)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range_(len(self)):
            if self[i] != other[i]:
                return False
        return True

    def __repr__(self):
        string = ""
        nodo_actual = self.cabeza
        while nodo_actual:
            string = f"{string}{nodo_actual.valor}, "
            nodo_actual = nodo_actual.siguiente
        return f"({string[:-2]})"


class Texto:
    def __init__(self, texto="", separador=",", diccionario=False):
        if diccionario:
            self.texto = ""
            for elemento in texto.items():
                self.texto += f"{elemento[1]},"
            self.texto = self.texto[:-1]
        else:
            self.texto = texto
        self.simbolo = separador

    def agregar(self, elemento):
        if self.texto:
            self.texto += f"{self.simbolo}{elemento}"
        else:
            self.texto += f"{elemento}"

    @property
    def suma(self):
        sumatoria = 0
        for i in self:
            #https://stackoverflow.com/questions/354038/
            #how-do-i-check-if-a-string-is-a-number-float
            #Comentario 52
            if i.replace('.', '', 1).isnumeric():
                sumatoria += float(i)
        return sumatoria

    def agrupar(self, other):
        if self.texto == "":
            return ""
        agrupado = ""
        for n in range_(len(self)):
            agrupado += f"({self[n]} | {other[n]}), "
        return agrupado[:-2]

    def find(self, elemento):
        for i in range_(len(self)):
            if self[i] == elemento:
                return i
        return -1

    def __add__(self, other):
        return self.texto + str(other)

    def __repr__(self):
        return str(self.texto)

    def __iter__(self):
        texto_2 = self.texto
        if texto_2 == "":
            return
        for i in range_(self.texto.count(self.simbolo)):
            yield texto_2[:texto_2.find(self.simbolo)]
            texto_2 = texto_2[texto_2.find(self.simbolo) + 1:]
        yield texto_2

    def __getitem__(self, numero):
        texto_2 = self.texto
        for i in range_(numero):
            texto_2 = texto_2[texto_2.find(self.simbolo)+1:]
        if not texto_2.count(self.simbolo):
            texto_2 += self.simbolo
        return texto_2[:texto_2.find(self.simbolo)]

    def __len__(self):
        return self.texto.count(self.simbolo) + 1


class Conjunto(Lista):
    def __init__(self, *args):
        super().__init__()
        for arg in args:
            self.add(arg)

    def add(self, elemento):
        if elemento not in self:
            self.agregar(elemento)

    def count(selfs, valor):
        contador = 0
        for i in self:
            if i == valor:
                contador += 1
        return contador

    def repite(self, valor):
        encontrado = False
        for i in self:
            if i == valor and not encontrado:
                encontrado = True

            elif i == valor and encontrado:
                return True
        return False

    def __repr__(self):
        string = ""
        nodo_actual = self.cabeza
        while nodo_actual:
            string = f"{string}{nodo_actual.valor}, "
            nodo_actual = nodo_actual.siguiente
        return f"conjunto({string[:-2]})"


class Cola(Lista):
    def __init__(self, *args):
        super().__init__()
        for arg in args:
            self.agregar(arg)
        self.append = self.agregar

    def popleft(self):
        if self.cabeza is None:
            return
        primero = self.cabeza
        self.cabeza = self.cabeza.siguiente
        if self.cabeza is None:
            self.cola = None
        return primero

    def pop(self):
        if self.cabeza is None:
            return
        elif self.cabeza == self.cola:
            self.cabeza = None
            self.cola = None
            return self.cabeza
        ultimo = self.cola
        penultimo = self.obtener(len(self) - 2)
        penultimo.siguiente = None
        self.cola = penultimo
        if self.cabeza is None:
            self.cola = None
        return ultimo

    def __repr__(self):
        string = ""
        nodo_actual = self.cabeza
        while nodo_actual:
            string = f"{string}{nodo_actual.valor}, "
            nodo_actual = nodo_actual.siguiente
        return f"cola([{string[:-2]}])"



class Listado:
    def __init__(self, *args, tipo="C"):
        pass