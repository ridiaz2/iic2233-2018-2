from excepciones import Volver, VolverMenu
import requests
import re
import math



RADIO_TERRESTRE = 6371 #km (Aproximación del radio medio)
def formula_haversine(lat_0, lon_0, lat_1, lon_1):
    '''https://www.genbeta.com/desarrollo/como-calcular-la-distancia
    -entre-dos-puntos-geograficos-en-c-formula-de-haversine'''
    '''https://lapertenencia.wordpress.com/2017/08/28/calcular-distancia
    -entre-dos-coordenadas-en-la-tierra/'''
    lat_0, lat_1, lon_0, lon_1 = map(lambda i: math.radians(float(i)),
                                     (lat_0, lat_1, lon_0, lon_1))
    dif_lat = lat_1 - lat_0
    dif_lon = lon_1 - lon_0
    a_ = (math.sin(dif_lat/2)**2) + (math.cos(lat_0) * math.cos(lat_1) *
                                    (math.sin(dif_lon/2)**2))
    c_ = 2 * RADIO_TERRESTRE * math.asin(math.sqrt(a_))
    return c_


def comprobar_correo_2(correo):
    condicion = "^([A-Za-z0-9\_]{3,8})(\@)"
    condicion_largo = ""
    for n in range(1, 11):
        agregar = "[A-Za-z0-9\_]{" + str(n) + "}(\.)[A-Za-z0-9_]{" \
                  + str(max(1, 3 - n)) + "," + str(11 - n) + "}"
        condicion_largo += agregar + "|"
    condicion += "(" + condicion_largo[:-1] + ")$"

    # condicion = "^([A-Za-z0-9\_]{3,8})(\@)([a-zA-Z0-9(\.){1}]){4,12}"

    return bool(re.fullmatch(condicion, correo))

def comprobar_correo(correo):
    condicion = "([A-Za-z0-9\_]{3,8})(\@)[A-Za-z0-9\_\.]{4,12}"
    condicion_punto = "[A-Za-z0-9\_]+(\.)[A-Za-z0-9]+"
    if re.fullmatch(condicion, correo):
        dominio = re.split("@", correo)[1]
        return bool(re.fullmatch(condicion_punto, dominio))
    return False

def comprobar_password(password):
    condicion = "[A-Za-z0-9]{8,12}"
    condicion_mayuscula = "[A-Za-z0-9]*[A-Z][A-Za-z0-9]*"
    if re.fullmatch(condicion, password):
        return bool(re.fullmatch(condicion_mayuscula, password))
    return False

def entrada(string=""):
    variable = input(string)
    if variable == "<":
        raise Volver()
    elif variable == "<<":
        raise VolverMenu
    return variable

def verificar(string="", funcion_comprobar=bool, mensaje="Lo sentimos :O "
    "Puede que la respuesta no sea válida, por favor, inténtelo de nuevo :D"):
    variable = entrada(string)
    while not funcion_comprobar(variable):
        print(mensaje)
        variable = entrada(string)
    return variable


def completar_numero(numero, largo=2):
    numero = str(numero)
    espacios = largo - len(numero)
    return f"{' ' * espacios}[{numero}]"

def resumen_datos(lugar):
    contacto = f"\n     * Contacto: {lugar['contact']}" if lugar['contact'] \
        else ""

    return f"{lugar['name']}{contacto}\n     * " \
           f"Ubicación: {lugar['location']['formattedAddress'][0]}"

def en_rango(string, *args):
    if not string.isnumeric():
        return False
    numero = int(string)
    limite_0, limite_1 = 0, args[0] if len(args) == 1 else args
    return limite_0 <= numero <= limite_1

