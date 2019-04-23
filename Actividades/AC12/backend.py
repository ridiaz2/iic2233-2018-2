import json
import os
import os.path as path
import pickle

from clases import Comida, ComidaEncoder

BOOK_PATH = 'recetas.book'


class PyKitchen:
    def __init__(self):
        self.recetas = []
        self.comidas = []
        self.despachadas = []

    def cargar_recetas(self):
        '''Esta función se encarga de cargar el archivo recetas.book'''
        with open("recetas.book", "rb") as archivo:
            self.recetas.extend(pickle.load(archivo))

    def guardar_recetas(self):
        '''Esta función se encarga de guardar las recetas (instancias), en el
        archivo recetas.book'''
        with open("recetas.book", "wb") as archivo:
            pickle.dump(self.recetas, archivo)

    def cocinar(self):
        '''Esta funcion debe:
        - filtrar recetas verificadas
        - crear comidas a partir de estas recetas
        - guardar las comidas en la carpeta horno
        '''
        for receta in self.recetas:
            if receta.verificada:
                comida = Comida.de_receta(receta)
                print(comida.fecha_ingreso)
                with open(f"./horno/{receta.nombre}.json", "w") as archivo:
                    json.dump(comida, archivo, cls=ComidaEncoder)

    def despachar_y_botar(self):
        ''' Esta funcion debe:
        - Cargar las comidas que están en la carpeta horno.
            Pro tip: string.endswith('.json') retorna true si un string
            termina con .json
        - Crear instancias de Comida a partir de estas.
        - Guardar en despachadas las que están preparadas
        - Imprimir las comidas que están quemadas
        - Guardar en comidas las no preparadas ni quemadas
        '''
        nombres = [i for i in os.listdir("horno") if i.endswith(".json")]
        for nombre in nombres:
            with open(nombre) as archivo:
                comida = json.load(archivo)
                if not comida.preparado:
                    self.comidas.append(comida)
                elif comida.preparado and not comida.quemado:
                    self.despachadas.append(comida)
                elif comida.quemado:
                    print(comida.nombre)



