from estructuras_de_datos import Tupla

class InvalidQuery(Exception):
    def __init__(self, valor, tipo="C"):
        # Sobreescribimos el __init__ para cambiar el ingreso de los parámetros
        if tipo == "comuna" or tipo == "provincia" or tipo == "sistema":
            texto = "La {} '{}' no existe."
        else:
            if tipo == "C":
                tipo = "casa"
            elif tipo == "E":
                tipo = "estación elevadora"
            elif tipo == "T":
                tipo = "subestación de transmisión"
            elif tipo == "D":
                tipo = "subestación de distribución"
            elif tipo == "G":
                tipo = "central generadora"
            texto = "No existe una {} con id '{}'"
        super().__init__(texto.format(tipo, str(valor)))

class ElectricalOverload(Exception):
    def __init__(self, valor, funcion):
        id_ = valor.id
        valor = valor.potencia
        texto = "La acción {} sobrecarga la red a {} kW (Casa {})."
        super().__init__(texto.format(funcion.__name__, str(valor),
                         str(id_)))

class ErrorEntrada(Exception):
    def __init__(self, texto = ""):
        super().__init__(texto)

class ForbiddenAction(Exception):
    def __init__(self, desde, hasta, funcion, tipo="tipo"):
        if tipo == "tipo":
            tupla = Tupla(funcion.__name__, desde.clase, hasta.clase)
            texto = "Acción {} no está permitida entre {} y {}"
        elif tipo in Tupla("comuna", "provincia"):
            if desde.clase == hasta.clase:
                entidad = "casas"
            else:
                entidad = "casas y subestaciones"
            tupla = Tupla(funcion.__name__, entidad, tipo)
            texto = "Acción {} no está permitida entre {} que tienen {} " \
                    "distintas."
        elif tipo == "ciclo":
            tupla = Tupla(funcion.__name__)
            texto = "Acción {} no está permitida entre nodos " \
                    "previamente conectados porque se " \
                    "formaría un ciclo"
        elif tipo in ("GE", "ET", "TD"):
            if tipo == "GE":
                tupla = Tupla(funcion.__name__, desde.clase, hasta.clase)
            elif tipo in Tupla("ET", "TD"):
                tupla = Tupla(funcion.__name__, hasta.clase, desde.clase)
            texto = "Acción {} no está permitida porque esta {} ya tiene una " \
                    "{}."
        elif "sellama" in tipo:
            mensaje = tipo[:2]
            tupla = Tupla(funcion.__name__, mensaje)
            texto = "Accion {} no se completará porque esta conexión {} existe."
        super().__init__(texto.format(*tupla))

class Volver(Exception):
    def __init__(self):
        super().__init__("Volver atrás en el programa")

class VolverMenu(Exception):
    def __init__(self):
        super().__init__("Volver al Menú en el programa")