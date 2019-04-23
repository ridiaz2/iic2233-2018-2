import math

class Circulo:
    def __init__(self,coordenada_x,coordenada_y,radio):
        self.x = float(coordenada_x)
        self.y = float(coordenada_y)
        self.r = float(radio)

    def obtener_area(self):
        return math.pi*(self.r**2)

    def obtener_perimetro(self):
        return 2*math.pi*self.r

    def __str__(self):
        return "Círculo de radio "+str(self.pi)

class Rectangulo:
    def __init__(self,coordenada_x,coordenada_y,largo,ancho):
        self.x = float(coordenada_x)
        self.y = float(coordenada_y)
        self.l = largo
        self.a = ancho

    def obtener_area(self):
        return largo*ancho

    def obtener_perimetro(self):
        return (2*largo)+(2*ancho)

    def es_cuadrado(self):
        if largo == ancho:
            return True
        else:
            return False

    def __str__(self):
        if self.es_cuadrado()==True:
            return "Cuadrado de lado "+str(largo)
        else:
            return "Rectángulo de "+str(largo)+"x"+str(ancho)

circulo1=Circulo(3,4,8)
rectangulo1=Rectangulo(3,4,2,2)