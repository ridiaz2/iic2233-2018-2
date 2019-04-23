import json
from datetime import datetime, timedelta
from hashlib import blake2b

RECETAS_LOCK_PATH = 'RecetasLockJSON.json'
INGREDIENTES_PATH = 'ingredientes.txt'
'''
=====================================
NO BORRAR NI CAMBIAR!
'''
SUPER_SECRET_KEY = b'IIC2233'
'''
=====================================
'''


class Receta:
    """Clase que modela una receta del 'PyKitchen' cookbook"""

    def __init__(self, nombre='', ingredientes=None, alinos=None):
        self.nombre = nombre
        self.ingredientes = ingredientes or []
        self.alinos = alinos or []
        self.llave_segura = None

    @property
    def verificada(self):
        """Property que nos indica si una receta fue limpiada o no."""
        return hasattr(
            self, 'llave_segura') and self.llave_segura == self.encriptar()

    def encriptar(self):
        """Funcion que encripta el valor a partir de una llave secreta"""
        encriptador = blake2b(key=SUPER_SECRET_KEY, digest_size=16)
        encriptador.update(self.nombre.encode())

        return encriptador.hexdigest()

    @staticmethod
    def abrir_ingredientes():
        """Genera las líneas del archivo ingredientes.txt"""
        with open(INGREDIENTES_PATH, encoding='utf-8') as fp:
            yield from map(lambda x: x.strip(), fp)

    def abrir_recetas_lock(self):
        """
        Funcion para abrir el archivo que indica los atributos
        de las recetas
        """
        with open(RECETAS_LOCK_PATH, encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return set(datos)

    def __setstate__(self, state):
        """
        Deserializa

        Elimina los atributos incorrectos y los ingredientes inválidos.
        """
        filtro = {llave: valor for llave, valor in state.items() if llave in
                  self.abrir_recetas_lock()}
        ingredientes = self.abrir_ingredientes()
        filtro["ingredientes"] = [ingrediente for ingrediente in filtro[
            "ingredientes"] if ingrediente in ingredientes]
        self.__dict__ = filtro

    def __getstate__(self):
        """
        Serializa

        Recuerda colocar el atributo llave_segura.
        """
        self.llave_segura = self.encriptar()
        return self.__dict__


class Comida:
    def __init__(self,
                 nombre='',
                 nivel_preparacion=0.0,
                 ingredientes=None,
                 alinos=None,
                 fecha_ingreso=None):
        self.nombre = nombre
        self.nivel_preparacion = nivel_preparacion
        self.ingredientes = ingredientes or []
        self.alinos = alinos or []

        ''' Recuerda cambiar aqui el nivel de preparacion de acuerdo a la fecha
        de ingreso!'''
        if self.nivel_preparacion is not None and fecha_ingreso is not None:
            fecha_actual = datetime.now()
            self.fecha_ingreso = self.str_a_date(fecha_ingreso) if type(
                self.fecha_ingreso) == str else self.fecha_ingreso
            minutos = (fecha_actual - fecha_ingreso).seconds // 60
            self.nivel_preparacion += minutos



    @property
    def quemado(self):
        return self.nivel_preparacion > 100

    @property
    def preparado(self):
        return self.nivel_preparacion >= 100

    @staticmethod
    def date_a_str(fecha):
        return fecha.strftime('%Y-%m-%d-%H-%M-%S')

    @staticmethod
    def str_a_date(fecha_str):
        return datetime.strptime(fecha_str, '%Y-%m-%d-%H-%M-%S')

    @classmethod
    def de_receta(cls, receta):
        return cls(receta.nombre, 0.0, receta.ingredientes, receta.alinos)


class ComidaEncoder(json.JSONEncoder):
    """Utiliza esta clase para codificar en json"""

    def default(self, obj):
        if isinstance(obj, Comida):
            return {'nombre': obj.nombre,
                    'nivel_preparacion': obj.nivel_preparacion,
                    'ingredientes': obj.ingredientes,
                    "alinos": obj.alinos,
                    'fecha_ingreso': obj.date_a_str(datetime.now())}

            # Mantenemos la serialización por defecto para otros tipos
        return super().default(obj)


