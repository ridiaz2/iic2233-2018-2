from functools import namedtuple
from iic2233_utils import *
from datetime import datetime
import operator, math, os.path
from itertools import tee, count
from functools import reduce


############# Configurables ################
data_size = "medium"
ruta = f"./data/{data_size}"


############ Named Tuples ###################
Pasajero = namedtuple("Pasajero", ["id", "nombre", "clase", "edad"])
Aeropuerto = namedtuple("Aeropuerto", ["id", "nombre", "latitud", "longitud",
                                       "iso"])
Vuelo = namedtuple("Vuelo", ["id", "desde", "hasta", "fecha"])
Viaje = namedtuple("Viaje", ["id", "pasajero"])
Output = namedtuple("Output", ["id", "entrada", "tipo", "salida"])


############## Funciones ###################
def a_datetime(objeto):
    if type(objeto) == str:
	    return datetime.strptime(objeto, "%Y-%m-%d %H:%M:%S")
    elif type(objeto) == int:
        obj = str(objeto)
        return datetime(*map(int, [obj[:4], obj[4:6], obj[6:8], obj[8:10],
                            obj[10:12], obj[12:14]]))
    return objeto


def a_int(objeto):
    return int(str(objeto).replace("-", "").replace(":", "").replace(" ", ""))
    return objeto


def a_str(objeto):
    if type(objeto) == int:
        return str(a_datetime(objeto))
    elif type(objeto) == datetime:
        return str(objeto)
    return objeto


def obtener_pasajeros(ruta):
    with open(ruta + "/passengers.csv", encoding="UTF-8") as archivo:
        archivo.readline()
        for linea in archivo:
            lista = linea.strip().split(",")
            lista[0], lista[3] = int(lista[0]), int(lista[3])
            yield Pasajero(*lista)


def obtener_aeropuertos(ruta):
    with open(ruta + "/airports.csv", encoding="UTF-8") as archivo:
        archivo.readline()
        for linea in archivo:
            lista = linea.strip().split(",")
            lista[2], lista[3] = float(lista[2]), float(lista[3])
            yield Aeropuerto(*lista)


def obtener_vuelos(ruta):
    with open(ruta + "/flights.csv", encoding="UTF-8") as archivo:
        archivo.readline()
        for linea in archivo:
            lista = linea.strip().split(",")
            lista[0], lista[3] = int(lista[0]), a_int(lista[3])
            yield Vuelo(*lista)


def obtener_viajes(ruta):
    with open(ruta + "/flights-passengers2.csv", encoding="UTF-8") as archivo:
        archivo.readline()
        for linea in archivo:
            lista = [int(i) for i in linea.strip().split(",")]
            yield Viaje(*lista)


def obtener_inputs(ruta):
    with open(ruta, encoding="UTF-8") as archivo:
        for linea in archivo:
            yield parse(linea.strip())


def calcular_distancia(a1, a2):
    radio = 3440
    return 2 * radio * math.asin(math.sqrt(
        (math.sin((a2.latitud - a1.latitud) / 2) ** 2) + (math.cos(
            a1.latitud) * math.cos(a2.latitud) * (math.sin(
                (a2.longitud - a1.longitud) / 2) ** 2))))


def operacion(simbolo, valor1, valor2, set=False):
    #https://stackoverflow.com/questions/1740726/turn-string-into-operator
    operadores = {"<": operator.lt, ">": operator.gt, "!=": operator.ne,
                  "==": operator.eq, "AND": operator.methodcaller(
                  "intersection", valor2), "OR": operator.methodcaller(
                  "union", valor2), "XOR": operator.methodcaller(
                  "symmetric_difference", valor2),
                  "DIFF": operator.methodcaller("difference", valor2)}
    operador = operadores[simbolo]
    if set:
        return operador(valor1)
    return operador(valor1, valor2)


def load_database(base_datos):
    global ruta
    if base_datos == "Passengers":
        return obtener_pasajeros(ruta)
    elif base_datos == "Airports":
        return obtener_aeropuertos(ruta)
    elif base_datos == "Flights":
        return obtener_vuelos(ruta)
    elif base_datos == "Travels":
        return obtener_viajes(ruta)


def coincidencia_vuelo(i, vuelo, contador, generador):
    global super_contador
    print("AAAAAAAAAAAAAH", next(super_contador))
    print(contador, i.id == vuelo.desde or i.id == vuelo.hasta)
    if next(contador) >= 4:
        print("jijiji")
        generador = []
        raise StopIteration
    if i.id == vuelo.desde or i.id == vuelo.hasta:
        print("jeje")
        siguiente = next(contador)
        if siguiente >= 1:
            print("ya llegamos a 2 :D")
            generador = ""
        return True
    return False


def aeropuertos_por_vuelo(vuelo, aeropuertos):
    filtro = filter(lambda i: i.id == vuelo.desde or i.id == vuelo.hasta,
                aeropuertos)
    lista = list(filtro)
    return calcular_distancia(*lista)


def distancia_vuelo(vuelo, aeropuertos):
    return calcular_distancia(aeropuertos[vuelo.desde], aeropuertos[
        vuelo.hasta])


def filter_flights(vuelos, aeropuertos, tipo, simbolo, valor):
    if tipo == "date":
        return filter(lambda vuelo: operacion(simbolo, a_datetime(vuelo.fecha),
                                       a_datetime(valor)), vuelos)
    elif tipo == "distance":
        lista_aeropuertos = {x.id: x for x in aeropuertos}
        return filter(lambda vuelo: operacion(simbolo,
            distancia_vuelo(vuelo, lista_aeropuertos), valor), vuelos)


def filter_passengers(pasajeros, vuelos, viajes, id, start, end):
    comienzo = a_datetime(start)
    llegada = a_datetime(end)
    vuelos_coinciden = {i.id: i for i in vuelos if (i.hasta == id and
                        comienzo < a_datetime(i.fecha) < llegada)}
    diccionario_pasajeros = {i.id: i for i in pasajeros}
    filtro = filter(lambda viaje: viaje.id in vuelos_coinciden, viajes)
    for i in filtro:
        yield diccionario_pasajeros[i.pasajero]


def filter_passengers_by_age(pasajeros, edad, lower=True):
    if lower:
        simbolo = "<"
    else:
        simbolo = ">"
    return filter(lambda pasajero: operacion(simbolo, pasajero.edad, edad),
                  pasajeros)


def filter_airports_by_country(aeropuertos, iso):
    return filter(lambda aeropuerto: aeropuerto.iso == iso, aeropuertos)


def filter_airports_by_distance(aeropuertos, id, valor, lower=False):
    if lower:
        simbolo = "<"
    else:
        simbolo = ">"
    aeropuertos_1, aeropuertos_2 = tee(aeropuertos, 2)
    #diccionario_aeropuertos = {i.id: i for i in aeropuertos}
    aeros = [i for i in aeropuertos_2 if i.id == id]
    if len(aeros) == 0:
        return filter(True, [])
    aero_actual = aeros[0]
    return filter(lambda aeropuerto: operacion(simbolo, calcular_distancia(
        aero_actual, aeropuerto), valor), aeropuertos_1)


def viajes_por_pasajero(viajes, diccionario_vuelos):
    viajes_por_pasajero = dict()
    foreach(lambda i: viajes_por_pasajero.update({
        i.pasajero: (viajes_por_pasajero.get(i.pasajero, "") + " " + str(
            diccionario_vuelos.get(i.id, ""))).strip()}), viajes)
    return viajes_por_pasajero


def viajes_por_pasajero_2(viajes, diccionario_vuelos):
    viajes_por_pasajero = dict()
    [n for n in map(lambda i: viajes_por_pasajero.update({
        i.pasajero: (viajes_por_pasajero.get(i.pasajero, "") + " " + str(
            diccionario_vuelos.get(i.id, ""))).strip()}), viajes)]
    return viajes_por_pasajero


def mas_repetido(lista):
    #https://stackoverflow.com/questions/1518522/
    #find-the-most-common-element-in-a-list
    return max(lista, key=lista.count)


def favourite_airport(pasajeros, vuelos, viajes):
    #viajes_por_pasajero = {viaje.pasajero: (viajes_por_pasajero.get(
        #viaje.pasajero, "") + str(viaje.id)).strip() for viaje in viajes}
    diccionario_vuelos = {i.id: i.hasta for i in vuelos}
    diccionario_viajes = viajes_por_pasajero(viajes, diccionario_vuelos)
    diccionario_preferencias = {pasajero.id: mas_repetido(diccionario_viajes[
        pasajero.id].split(" ")) for pasajero in pasajeros}
    return diccionario_preferencias

def favourite_airport_2(pasajeros, vuelos, viajes):
    #viajes_por_pasajero = {viaje.pasajero: (viajes_por_pasajero.get(
        #viaje.pasajero, "") + str(viaje.id)).strip() for viaje in viajes}
    diccionario_vuelos = {i.id: i.hasta for i in vuelos}
    diccionario_viajes = viajes_por_pasajero_2(viajes, diccionario_vuelos)
    diccionario_preferencias = {pasajero.id: mas_repetido(diccionario_viajes[
        pasajero.id].split(" ")) for pasajero in pasajeros}
    return diccionario_preferencias




def passenger_miles(pasajeros, aeropuertos, vuelos, viajes):
    diccionario_aeropuertos = {i.id: i for i in aeropuertos}
    diccionario_vuelos = {i.id: distancia_vuelo(i, diccionario_aeropuertos)
                          for i in vuelos}
    diccionario_viajes = viajes_por_pasajero(viajes, diccionario_vuelos)
    diccionario_suma_distancias = {pasajero.id: sum(map(float,
        diccionario_viajes[pasajero.id].split(" "))) for pasajero in pasajeros}
    return diccionario_suma_distancias


def calcular_popular(lista, avg=False):
    if avg:
        return sum(map(int, lista)) / len(lista)
    else:
        return sum(map(int, lista))


def popular_airports(vuelos, aeropuertos, viajes, topn, avg=False):
    diccionario_vuelos = dict()
    foreach(lambda i: diccionario_vuelos.update({
            i.id: (diccionario_vuelos.get(i.id, 0) + 1)}), viajes)
    diccionario_aeropuertos = dict()
    foreach(lambda i: diccionario_aeropuertos.update({
        i.hasta: (diccionario_aeropuertos.get(i.hasta, "") + " " +
                  str(diccionario_vuelos[i.id])).strip()}), vuelos)
    if avg:
        lista = sorted(list(diccionario_aeropuertos), key=lambda i:
        calcular_popular(diccionario_aeropuertos[i].split(" ")), reverse=True)[
                :topn]
    else:
        lista = sorted(list(diccionario_aeropuertos), key=lambda i:
        calcular_popular(diccionario_aeropuertos[i].split(" "), False),
                       reverse=True)[:topn]
    return tuple(lista)

def popular_airports_2(vuelos, aeropuertos, viajes, topn, avg=False):
    diccionario_vuelos = dict()
    foreach(lambda i: diccionario_vuelos.update({
            i.id: (diccionario_vuelos.get(i.id, 0) + 1)}), viajes)
    diccionario_aeropuertos = dict()
    [n for n in map(lambda i: diccionario_aeropuertos.update({
        i.hasta: (diccionario_aeropuertos.get(i.hasta, "") + " " +
                  str(diccionario_vuelos[i.id])).strip()}), vuelos)]
    if avg:
        lista = sorted(list(diccionario_aeropuertos), key=lambda i:
        calcular_popular(diccionario_aeropuertos[i].split(" ")), reverse=True)[
                :topn]
    else:
        lista = sorted(list(diccionario_aeropuertos), key=lambda i:
        calcular_popular(diccionario_aeropuertos[i].split(" "), False),
                       reverse=True)[:topn]
    return tuple(lista)


def key_foreach(funcion, condicion):
    if condicion:
        return funcion
    else:
        pass


def airport_passengers(pasajeros, vuelos, viajes, id1, id2, operador):
    diccionario_vuelos, diccionario_aeropuertos = [dict() for i in range(2)]
    diccionario_pasajeros = {i.id: i for i in pasajeros}
    lista_vuelos = {i.id: (i.desde, i.hasta) for i in vuelos
                    if id1 in [i.desde, i.hasta] or id2 in [i.desde, i.hasta]}
    foreach(lambda i: diccionario_vuelos.update({i.id: (diccionario_vuelos.get(
        i.id, "") + " " + str(i.pasajero)).strip()}), viajes)
    foreach(lambda i: diccionario_aeropuertos.update({lista_vuelos[i][0]: (
        diccionario_aeropuertos.get(lista_vuelos[i][0], "") + " " +
        diccionario_vuelos.get(i, "")).strip(), lista_vuelos[i][1]: (
        diccionario_aeropuertos.get(lista_vuelos[i][1], "") + " " +
        diccionario_vuelos.get(i, "")).strip()}), lista_vuelos)
    return operacion(operador, *(set(map(lambda i: diccionario_pasajeros[
        int(i)], diccionario_aeropuertos.get(k, str(len(diccionario_aeropuertos
        ))).split(" "))) for k in [id1, id2]), True)

def airport_passengers_2(pasajeros, vuelos, viajes, id1, id2, operador):
    diccionario_vuelos, diccionario_aeropuertos = [dict() for i in range(2)]
    diccionario_pasajeros = {i.id: i for i in pasajeros}
    lista_vuelos = {i.id: (i.desde, i.hasta) for i in vuelos
                    if id1 in [i.desde, i.hasta] or id2 in [i.desde, i.hasta]}
    [n for n in map(lambda i: diccionario_vuelos.update({i.id: (
        diccionario_vuelos.get(
        i.id, "") + " " + str(i.pasajero)).strip()}), viajes)]
    [n for n in map(lambda i: diccionario_aeropuertos.update({lista_vuelos[i][
        0]: (diccionario_aeropuertos.get(lista_vuelos[i][0], "") + " " +
        diccionario_vuelos.get(i, "")).strip(), lista_vuelos[i][1]: (
        diccionario_aeropuertos.get(lista_vuelos[i][1], "") + " " +
        diccionario_vuelos.get(i, "")).strip()}), lista_vuelos)]
    return operacion(operador, *(set(map(lambda i: diccionario_pasajeros[
        int(i)], diccionario_aeropuertos.get(k, str(len(diccionario_aeropuertos
        ))).split(" "))) for k in [id1, id2]), True)

a = airport_passengers(load_database("Passengers"), load_database("Flights"),
                  load_database("Travels"), "0WI1", "3AA3", "AND")
a2 = airport_passengers_2(load_database("Passengers"), load_database("Flights"),
                  load_database("Travels"), "0WI1", "3AA3", "AND")
print(a)
print(a2)

def furthest_distance(pasajeros, aeropuertos, vuelos, viajes, id, n=3):
    di_pas, di_aero = ({i.id: i for i in k} for k in (pasajeros, aeropuertos))
    diccionario_vuelos, diccionario_viajes = ({vuelo.id: distancia_vuelo(vuelo,
                          di_aero) for vuelo in vuelos if
                          vuelo.desde == id}, dict())
    foreach(lambda i: diccionario_viajes.update({i.id:
        (diccionario_viajes.get(i.id, "") + " " + str(i.pasajero)).strip(
        )}), viajes)
    pasajeros_orden = [[di_pas[k] for k in
                    map(int, diccionario_viajes[i].split(" ")) if k in
                    di_pas] for i in sorted(diccionario_vuelos,
                    key=lambda i: diccionario_vuelos[i], reverse=True)]
    if len(pasajeros_orden) == 0:
        return []
    return reduce(lambda l1, l2: l1 + l2, pasajeros_orden)[:n]

def furthest_distance_2(pasajeros, aeropuertos, vuelos, viajes, id, n=3):
    di_pas, di_aero = ({i.id: i for i in k} for k in (pasajeros, aeropuertos))
    diccionario_vuelos, diccionario_viajes = ({vuelo.id: distancia_vuelo(vuelo,
                          di_aero) for vuelo in vuelos if
                          vuelo.desde == id}, dict())
    [n for n in map(lambda i: diccionario_viajes.update({i.id:
        (diccionario_viajes.get(i.id, "") + " " + str(i.pasajero)).strip(
        )}), viajes)]
    pasajeros_orden = [[di_pas[k] for k in
                    map(int, diccionario_viajes[i].split(" ")) if k in
                    di_pas] for i in sorted(diccionario_vuelos,
                    key=lambda i: diccionario_vuelos[i], reverse=True)]
    if len(pasajeros_orden) == 0:
        return []
    return reduce(lambda l1, l2: l1 + l2, pasajeros_orden)[:n]

a = furthest_distance(load_database("Passengers"), load_database(
    "Airports"), load_database("Flights"), load_database("Travels"), "0WI1", 4)
a2 = furthest_distance_2(load_database("Passengers"), load_database(
    "Airports"), load_database("Flights"), load_database("Travels"), "0WI1", 4)
print(a)
print(a2)

def funcion(texto):
    funciones = {"load_database": load_database, "filter_flights":
                filter_flights, "filter_passengers": filter_passengers,
                "filter_passengers_by_age": filter_passengers_by_age,
                "filter_airports_by_country": filter_airports_by_country,
                "filter_airports_by_distance": filter_airports_by_distance,
                "favourite_airport": favourite_airport,
                "passenger_miles": passenger_miles, "popular_airports":
                popular_airports, "airport_passengers":
                airport_passengers, "furthest_distance": furthest_distance}
    return funciones[texto]


def interpretar_input(diccionario):
    if type(diccionario) == dict:
        retorno = map(lambda i: funcion(interpretar_input(i))(
            *interpretar_input(diccionario[i])), diccionario)
        for i in retorno:
            return i
    elif type(diccionario) == list:
        return map(lambda i: interpretar_input(i), diccionario)
    else:
        return diccionario


def revisar_input(entrada, condicion, titulo="",
            error="Lo sentimos :O estamos teniendo problemas para"
            "entender el dato ingresado\nPor favor, inténtelo de nuevo :D"):
    if not condicion(entrada):
        print(error)
        if titulo != "":
            titulo = titulo.strip() + " "
        entrada = input(titulo)
        return revisar_input(entrada, condicion, titulo, error)
    else:
        return entrada


def formato_corchetes(numero, n):
    texto = " " * (n - len(str(numero))) + "[" + str(numero) + "]"
    return texto


def es_lista_de_numeros(texto, rango):
    if texto.isnumeric():
        if 0 <= int(texto) < rango:
            return True
        return False
    elif "," not in texto:
        return False
    lista = map(lambda i: i.strip(), texto.split(","))
    for i in lista:
        if not es_lista_de_numeros(i, rango):
            return False
    return True


def imprimir_output(output, titulo=""):
    if titulo != "":
        print(titulo)
    if type(output) in (dict, set, list, tuple):
        print(output)
        print()
        return ""
    foreach(print, output)
    print()


def leer_output_txt(ruta="./output.txt"):
    with open(ruta, encoding="UTF-8") as archivo:
        nueva_linea = ()
        nueva_linea_out = []
        for linea in archivo:
            if "----------" in linea:
                if not nueva_linea_out == []:
                    yield Output(*nueva_linea, nueva_linea_out)
                    nueva_linea_out = []
                num = int(linea[linea.find("a") + 1:][
                    :linea[linea.find("a"):].find("-") - 1])
                nueva_linea = (num, archivo.readline().strip(),
                               archivo.readline().strip())
            else:
                nueva_linea_out += [linea.strip()]
        if len(nueva_linea) == 0:
            return []
        yield Output(*nueva_linea, nueva_linea_out)


def print_objeto(objeto):
    if type(objeto) == str:
        print(objeto)
        return ""
    print(f"{formato_corchetes(int(objeto.id), 4)} {objeto.entrada} -> "
          f"{objeto.tipo}")
    print(" " * 8 + str(objeto.salida))


def imprimir_y_guardar(texto, lista, retorno=False, objeto_output=False):
    print_objeto(texto)
    if retorno:
        return texto
    lista += [texto]


def ultimo_valor_actual(lista):
    lista.reverse()
    texto = "|".join(lista)
    return lista[texto[:texto.find("----------")].count("|")]


def guardar_output_txt(dicc, ruta = "./output.txt"):
    if not os.path.exists(ruta):
        archivo = open(ruta, encoding="utf-8", mode="w")
        archivo.write()
        archivo.close()
    with open(ruta, encoding="utf-8") as archivo:
        datos = archivo.readlines()
        if datos == []:
            num = 0
        else:
            linea = ultimo_valor_actual(datos)
            num = int(linea[linea.find("a") + 1:][
                :linea[linea.find("a"):].find("-") - 1])
    with open(ruta, encoding="UTF-8", mode="a") as archivo:
        archivo.write(f"---------- Consulta {str(num + 1)} ----------\n")
        archivo.write(str(dicc.entrada) + "\n")
        archivo.write(str(dicc.tipo) + "\n")
        if dicc.tipo in ["generator", "filter"]:
            foreach(lambda i: archivo.write(str(i)+ "\n"), dicc.salida)
        else:
            archivo.write(str(dicc.salida) + "\n")


def guardar_consulta(diccionario):
    salida, opciones = interpretar_input(diccionario), ["Guardar", "Continuar"]
    tipo = str(type(salida))[8:-2]
    if tipo in ["generator", "filter"]:
        salida_lista = []
        foreach(lambda i: imprimir_y_guardar(str(i), salida_lista), salida)
    else:
        salida_lista = salida
        print(salida_lista)
    print("¿Desea guardar esta consulta?")
    foreach(lambda i: print(f"{i[0]} {i[1]}"), enumerate(opciones))
    respuesta = revisar_input(input(), lambda i: True if i in ["0", "1", ""]
        else False)
    if respuesta == "0":
        guardar_output_txt(Output("num", str(diccionario), tipo, salida_lista))


def reiniciar_output_txt(ruta="./output.txt"):
    with open(ruta, encoding="utf-8", mode="w") as archivo:
        archivo.write("")
    print("Datos borrados con éxito")


def escribir_en_archivo(archivo, dicc, num):
    archivo.write(f"---------- Consulta {str(num + 1)} ----------\n")
    archivo.write(str(dicc.entrada) + "\n")
    archivo.write(str(dicc.tipo) + "\n")
    if dicc.tipo in ["generator", "filter"]:
        foreach(lambda i: archivo.write(str(i) + "\n"), dicc.salida)
    else:
        archivo.write(str(dicc.salida) + "\n")

