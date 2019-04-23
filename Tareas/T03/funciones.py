from estructuras_de_datos import Tupla, Texto, Lista
from excepciones import InvalidQuery, ForbiddenAction, ErrorEntrada, \
    ElectricalOverload, Volver, VolverMenu
from random import randint

def entrada(texto):
    respuesta = input(texto)
    if respuesta == "<":
        raise Volver()
    elif respuesta == "<<":
        raise VolverMenu()
    return respuesta

def ajus(numero, espacio = 4):
    if type(numero) == int:
        numero = str(numero)
    if numero[0] == "[":
        numero = numero[1:]
    if numero[-1] == "]":
        numero = numero[:-1]
    return f"{' ' * max((espacio - len(numero) - 2), 0)}[{numero}]"

def input_lista(tupla, mensaje=">>> ", otro=False):
    print_lista(tupla)
    try:
        if otro:
            print(f"{ajus('*')} Otro")
        entrada_ = entrada(mensaje)
        while entrada_ not in range_(len(tupla), tipo=str):
            if entrada_ == "":
                entrada_ = randint(0, len(tupla) - 1)
                return entrada_

            elif entrada_ == "*" and otro:
                return "*"
            print("No pudimos entender tu input :O inténtelo de nuevo por favor :D")
            entrada_ = entrada(mensaje)
    except Volver:
        raise Volver()
    return entrada_

def print_lista(tupla):
    for n in range_(len(tupla)):
        print(f"{ajus(n)} {tupla[n]}")

def indice(texto, numero):
    texto_2 = texto
    for i in range_(numero):
        texto_2 = texto_2[texto_2.find(",")+1:]
    if not texto_2.count(","):
        texto_2 += ","
    return texto_2[:texto_2.find(",")]

def proporciones(valores_mij, potencia_total):
    consumo_total = valores_mij.suma()

    potencias = Lista()
    for i in valores_mij:
        consumo = float(i)
        if consumo_total == 0:
            potencia = 0
        else:
            potencia = consumo * potencia_total / consumo_total
        potencias.agregar(potencia)
    return potencias


def range_(*args, **kwargs):
    if kwargs:
        tipo = kwargs["tipo"]
    else:
        tipo = int
    primero = 0
    intervalo = 1
    if len(args) == 1:
        ultimo, *_ = args
    elif len(args) == 2:
        primero, ultimo = args
    elif len(args) == 3:
        primero, ultimo, intervalo = args

    ultimo, primero, intervalo = int(ultimo), int(primero), int(intervalo)
    lista = Lista()
    numero = primero
    while numero < ultimo:
        lista.agregar(tipo(numero))
        numero += intervalo

    return lista

def descifrar_input_conexion(texto):
    mas, menos = texto.find("+"), texto.find("-")
    if mas == -1 and menos == -1:
        raise ErrorEntrada("Simbolo de acción no encontrado")
    elif mas > -1 and menos > -1:
        raise ErrorEntrada("Se encontraron multiples acciones")
    if mas > -1:
        funcion = "+"
    elif menos > -1:
        funcion = "-"
    datos = Texto(texto, separador=funcion)
    tupla = Tupla(funcion)
    for i in datos:
        tipo, numero = i.strip()[0].upper(), i.strip()[1:]
        if tipo not in Tupla("G", "E", "T", "D", "C"):
            raise ErrorEntrada("Tipo no encontrado")
        elif not numero.isnumeric():
            raise ErrorEntrada("Dificultades al entender la id")
        tupla.agregar(Tupla(tipo, int(numero)))
    return tupla