#http://code.activestate.com/recipes/65117-converting-between-ascii-numbers-and-
# characters/
# Get the ASCII number of a character
#number = o`(char)
# Get the character given by an ASCII number
#char = chr(number)


from random import randint


def intercambio_0_1(numero):
    if numero == "1":
        return "0"
    else:
        return "1"


def cifrado_cesar(caracter, cifrar=True):
    #Si cifrar==True, la función aplica el cifrado.
    #En caso de ser False, se aplica el proceso inverso
    numero = ord(caracter)
    if cifrar:
        numero_10 = numero + 10
    else:
        numero_10 = numero - 10
    return chr(numero_10)


def caracter_a_binario(caracter, numerico=False):
    if numerico:
        numero = int(caracter)
    else:
        numero = ord(caracter)
    binario = ("00000000" + bin(numero)[2:])[-8:]
    return binario


def binario_a_caracter(binario):
    #daniel.blogmatico.com/python-de-binario-a-decimal-y-de-decimal-a-binario/
    numero = int(binario, 2)
    return chr(numero)


def obtener_cadena_aleatoria():
    numeros = ""
    for i in range(10):
        numeros += str(randint(0, 9))
    return numeros


def clave():
    return "2233"


def obtener_cadena_inicio(cadena_aleatoria):
    cadena_inicio = ""
    while len(cadena_inicio) < 256:
        cadena_inicio += clave() + cadena_aleatoria
    cadena_inicio = cadena_inicio[:256]
    return cadena_inicio


def obtener_lista(cadena_inicio, largo_mensaje):
    numeros = list(range(256))
    #numeros[i] se intercambia por numeros[j]
    #con j = i + cadena_inicio[i]
    for i in range(256):
        j = (i + int(cadena_inicio[i])) % 256
        numeros[i], numeros[j] = numeros[j], numeros[i]
    return numeros[:largo_mensaje]


def binario_a_mensaje(binario):
    mensaje = ""
    for i in range(len(binario)//8):
        mensaje += binario_a_caracter(binario[i*8:(i+1)*8])
    return mensaje


def encriptar(mensaje):
    largo_mensaje = len(mensaje)
    mensaje_cesar = ""
    cadena_aleatoria = obtener_cadena_aleatoria()
    for i in mensaje:
        mensaje_cesar += cifrado_cesar(i)
    lista_numeros = obtener_lista(
        obtener_cadena_inicio(cadena_aleatoria), largo_mensaje)
    lista_binaria = ""
    mensaje_binario = ""
    mensaje_codificado = ""
    for i in range(largo_mensaje):
        mensaje_binario += caracter_a_binario(mensaje_cesar[i])
        lista_binaria += caracter_a_binario(lista_numeros[i], True)
    for i in range(len(mensaje_binario)):
        if mensaje_binario[i] == lista_binaria[i]:
            mensaje_codificado += "0"
        else:
            mensaje_codificado += "1"
    return cadena_aleatoria + mensaje_codificado


def desencriptar(codigo):
    cadena_aleatoria = codigo[:10]
    largo_mensaje = len(codigo[10:])//8
    lista_numeros = obtener_lista(
        obtener_cadena_inicio(cadena_aleatoria), largo_mensaje)
    lista_binaria = ""
    for i in lista_numeros:
        lista_binaria += caracter_a_binario(i, True)
    mensaje_binario = ""
    for i in range(len(codigo[10:])):
        if codigo[10:][i] == "1":
            mensaje_binario += intercambio_0_1(lista_binaria[i])
        else:
            mensaje_binario += lista_binaria[i]
    mensaje_cifrado = binario_a_mensaje(mensaje_binario)
    mensaje_decifrado = ""
    for i in mensaje_cifrado:
        mensaje_decifrado += cifrado_cesar(i, False)
    return mensaje_decifrado


