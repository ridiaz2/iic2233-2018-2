class Volver(Exception):
    def __init__(self):
        super().__init__("Volver atrás en el programa")

class VolverMenu(Exception):
    def __init__(self):
        super().__init__("Volver al Menú en el programa")

class OtraCategoria(Exception):
    def __init__(self):
        super().__init__("Es una búsqueda de otro tipo")