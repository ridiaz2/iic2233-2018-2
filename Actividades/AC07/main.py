
from collections import deque

class Terreno:

    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = set()



class Ciudad:

    def __init__(self, path):
        self._terrenos = dict()
        with open(path, encoding="utf-8") as archivo:
            for linea in archivo:
                origen, destinos = linea.strip().split(":")
                destinos = destinos.strip().split(",")
                for destino in destinos:
                    self.agregar_calle(origen, destino)

    def agregar_calle(self, origen, destino):
        for nodo in (origen, destino):
            if nodo not in self._terrenos:
                self._terrenos[nodo] = Terreno(nodo)
        self._terrenos[origen].vecinos.add(destino)

    def eliminar_calle(self, origen, destino):
        if origen not in self._terrenos or destino not in self._terrenos:
            return ()
        elif destino in self._terrenos[origen].vecinos:
            self._terrenos[origen].vecinos.remove(destino)
            return (origen, destino)
        else:
            return ()

    @property
    def terrenos(self):
        return set(self._terrenos)

    @property
    def calles(self):
        conjunto = set()
        for origen in self._terrenos:
            for destino in self._terrenos[origen].vecinos:
                conjunto.add((origen, destino))
        return conjunto

    def verificar_ruta(self, ruta):
        if ruta == []:
            return True
        elif len(ruta) == 1:
            return ruta[0] in self.terrenos
        cola = deque(ruta)
        while cola:
            nodo = cola.popleft()
            if nodo not in self.terrenos:
                return False
            if cola:
                if cola[0] not in self._terrenos[nodo].vecinos:
                    return False
        return True

    def entregar_ruta(self, origen, destino, camino=[], mejor_camino=[]):

        if origen not in self._terrenos or destino not in self._terrenos:
            return []

        # Para esta función, me basé principalmente en la estructura DFS ya
        # que, si bien BFS entregaría la más corta primero, de momento no se
        # me ocurre una manera para ir guardando el camino correspondiente a
        # cada nodo. Con recursión en DFS me pareció más fácil tener este
        # registro :D Intenté hacer algunos comentarios para explicar cada
        # paso de la función, ya que la estructuré de una manera algo confusa :D

        # Caso en que origen y destino son iguales antes de comenzar la
        # recursión (se retorna una lista con el nodo crrespondiente)
        if origen == destino and not camino:
            return [origen]

        # Se obtiene el terreno correspondiente al origen
        nodo = self._terrenos[origen]

        # Si no hemos pasado por este nodo (para evitar loops :D)
        if nodo.nombre not in camino:
            #print(f"{nodo.nombre} ---> {camino}")

            # Agregamos el nodo al camino
            camino.append(nodo.nombre)

            # Caso en que llegamos al nodo de destino (:
            if nodo.nombre == destino:

                # Si el camino que encontramos es mejor que el mejor camino
                # que teníamos hasta el momento, ahora es nuestro mejor camino
                if mejor_camino == [] or len(mejor_camino) > len(camino):
                    mejor_camino = camino.copy()

                #Volvemos un paso atrás y retornamos el mejor_camino encontrado
                camino.pop()
                return mejor_camino

            #Si ya recorrimos todos los vecinos del nodo actual, volvemos atrás
            elif nodo.vecinos == []:
                camino.pop()

            # En cualquier otro caso
            else:

                # Por cada vecino del nodo
                for vecino in nodo.vecinos:

                    # Reemplazar mejor_camino por el encontrado
                    # Esta sería la llamada recursiva
                    mejor_camino = self.entregar_ruta(vecino, destino,
                                                    camino, mejor_camino)

                # Cuando se recorren todos los caminos, se vuelve atrás :D
                camino.pop()

        # Retornar el mejor_camino encontrado
        return mejor_camino


    def ruta_corta(self, origen, destino):
        return self.entregar_ruta(origen, destino)


    def ruta_entre_bombas(self, origen, *destinos):
        camino_completo = [origen]
        for destino in destinos:
            camino = self.entregar_ruta(origen, destino)[1:]
            camino_completo += camino
            origen = destino
        return camino_completo

    def ruta_corta_entre_bombas(self, origen, *destinos):
        return self.ruta_entre_bombas(origen, *destinos)




if __name__ == '__main__':
    facil = Ciudad("facil.txt")
    medio = Ciudad("medio.txt")
    dificil = Ciudad("dificil.txt")
    kratos = Ciudad("kratos.txt")

    print(facil.entregar_ruta("A", "B"))
    print(medio.entregar_ruta("C", "D"))
    print(dificil.entregar_ruta("E", "F"))
    print(kratos.entregar_ruta("G", "H"))
    # Agrega aqui tus consultas
