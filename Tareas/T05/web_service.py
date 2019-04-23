import requests
from funciones import entrada, completar_numero, resumen_datos, verificar, \
    en_rango, formula_haversine
from excepciones import OtraCategoria, Volver, VolverMenu
import math
from datetime import datetime, time


CLIENT_ID = "MVNV44OIUGUN3ZAIOQKJ5AM24RY4WWOO42MIKJ4K4O3EL0BF"
CLIENT_SECRET = "TTAPASZEXJEMZCB4IUQ10LD4GBQZ1RZP5LS153SUR0I0SMWU"
IPSTACK_KEY = "c9e5734f72cdfa2dcca9493949e3ff3a"

UBICACION_AUTOMATICA = True
LATITUD = 0
LONGITUD = 0


def obtener_ubicacion():
    if UBICACION_AUTOMATICA:
        respuesta = requests.get(f"http://api.ipstack.com/check?access_key"
                                 f"={IPSTACK_KEY}")
        diccionario = respuesta.json()
        return diccionario["latitude"], diccionario["longitude"]
    else:
        return LATITUD, LONGITUD

def obtener_paraderos(latitud, longitud):
    respuesta = requests.get(f"https://api.scltrans.it/v1/stops?center_lon="
                             f"{longitud}&center_lat={latitud}&radius=10000")
    diccionario = respuesta.json()
    return diccionario["results"]

def calcular_distancia(lat_0, lon_0, lat_1, lon_1):
    return formula_haversine(lat_0, lon_0, lat_1, lon_1)

def obtener_paradero_mas_cercano(latitud, longitud):
    paraderos = obtener_paraderos(latitud, longitud)
    mas_cercano = min(paraderos, key=lambda i: calcular_distancia(
        latitud, longitud, float(i["stop_lat"]), float(i["stop_lon"])))
    #for i in paraderos:
     #   print(i["stop_code"], calcular_distancia(latitud, longitud,
      #                          float(i["stop_lat"]), float(i["stop_lon"])))
    return mas_cercano

def obtener_recorridos(paradero):
    respuesta = requests.get(
        f"https://api.scltrans.it/v1/stops/{paradero['stop_id']}/stop_routes")
    diccionario = respuesta.json()
    return [(i["direction"]["route_id"], i["direction"]["direction_id"],
             i["direction"]["direction_headsign"])
            for i in diccionario]

def obtener_paraderos_recorrido(recorrido, direction):
    respuesta = requests.get(
        f"https://api.scltrans.it/v2/routes/{recorrido}/directions/{direction}")
    diccionario = respuesta.json()
    paraderos = diccionario["results"]["stop_times"]

    return {i["stop_sequence"]: (i["stop_id"], i["arrival_time"]) for i in
            paraderos}

def obtener_ubicacion_paradero(paradero_id):
    respuesta = requests.get(f"https://api.scltrans.it/v1/stops/{paradero_id}")
    diccionario = respuesta.json()
    return diccionario["stop_lat"], diccionario["stop_lon"]

def obtener_nombre_paradero(paradero_id):
    respuesta = requests.get(f"https://api.scltrans.it/v1/stops/{paradero_id}")
    diccionario = respuesta.json()
    return diccionario["stop_name"]

def obtener_listado_completo(paradero, ubicacion):
    recorridos = dict()
    mas_cercano = None
    distancia_menor = math.inf
    recorridos_ = obtener_recorridos(paradero)
    indice = 1
    largo = len(recorridos_)
    print(f"Cargando...")
    for recorrido in recorridos_:
        paraderos = obtener_paraderos_recorrido(*recorrido[:-1])
        mini_diccionario = dict()
        encontrado = False
        n = 1
        actual = None
        encontrado_aqui = False
        while actual != paradero["stop_id"]:
            actual, tiempo_0 = paraderos[n]
            distancia = calcular_distancia(*ubicacion,
                        *obtener_ubicacion_paradero(actual))
            if distancia <= 10:
                mini_diccionario[actual] = distancia
            if distancia < distancia_menor:
                distancia_menor = distancia
                mas_cercano = (recorrido, actual, tiempo_0)
                encontrado_aqui = True
            n += 1
        if encontrado_aqui:
            tiempo_1 = tiempo_0


        recorridos[recorrido] = mini_diccionario
        print(f"Cargando... ({indice}/{largo})")
        indice += 1

        '''    print({paradero[0]: (paradero[1],
            calcular_distancia(*ubicacion, *obtener_ubicacion_paradero(
                paradero[1]))) for paradero \
            in obtener_paraderos_recorrido(*recorrido).items()})
            '''
    return recorridos, mas_cercano, distancia_menor, tiempo_1

def obtener_tiempo_llegada(paradero, recorrido):
    while True:
        respuesta = requests.get(
            f"https://api.scltrans.it/v1/stops/{paradero}/next_arrivals")
        diccionario = respuesta.json()
        if diccionario.get("title", True) != "smsbus webservice timeout":
            for i in diccionario["results"]:
                if i["route_id"] == recorrido:
                    return i["arrival_estimation"]

def calcular_duracion_viaje(tiempo_0, tiempo_1):
    diferencia = a_datetime(tiempo_1) - a_datetime(tiempo_0)
    return segundos_a_string(diferencia.seconds)

def segundos_a_string(segundos_):
    segundos = segundos_ % 60
    minutos_ = segundos_ // 60
    minutos = minutos_ % 60
    horas = minutos_ // 60
    return str(time(horas, minutos, segundos))


def a_datetime(string):
    return datetime.strptime(string, '%H:%M:%S')


def consulta():
    while True:
        try:
            print("_"*80)
            print("A continuación puede buscar una categoría o descripción:")
            busqueda = entrada(">>> ")
            print(busqueda)
            url = "https://api.foursquare.com/v2/venues/search"
            params = dict(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                intent="browse",
                v=20180323,
                near="Santiago, CL",
                limit=100,
                query=busqueda
                )
            try:
                resp = requests.get(url=url, params=params)
                data = resp.json()
                if not data["response"]["venues"]:
                    raise OtraCategoria()
                datos = data["response"]["venues"]
            except OtraCategoria:
                try:
                    params.pop("query")
                    params["categoryId"] = busqueda
                    resp = requests.get(url=url, params=params)
                    data = resp.json()
                    if data["meta"]["code"] == 400:
                        raise OtraCategoria
                    datos = data["response"]["venues"]
                except OtraCategoria:
                    print("No se encontraron resultados para esta búsqueda")
                    raise Volver()
            print("-"*80)
            for numero, lugar in enumerate(datos):
                print(f"{completar_numero(numero)} {resumen_datos(lugar)}")
                print("-"*80)
            print("Ahora, puede ingresar el número de su búsqueda:")
            num = verificar(">>> ", lambda i: en_rango(i, len(datos) - 1))
            lugar_elegido = datos[int(num)]
            print("_"*80)
            print(f"Lugar elegido ---> [{num}] {lugar_elegido['name']}")
            latitud, longitud = lugar_elegido["location"]["lat"], \
                                lugar_elegido["location"]["lng"]
            paradero_cercano = obtener_paradero_mas_cercano(latitud, longitud)
            print(f"Paradero más cercano al lugar ---> "
                  f"{paradero_cercano['stop_name']}")


            latitud_1, longitud_1 = obtener_ubicacion()
            recorrido, mas_cercano, distancia_paradero, tiempo_1= \
                obtener_listado_completo(
                paradero_cercano, (latitud_1, longitud_1))
            distancia_total = calcular_distancia(latitud_1, longitud_1,
                                                 latitud, longitud)
            duracion_viaje = calcular_duracion_viaje(mas_cercano[-1], tiempo_1)
            if duracion_viaje == "00:00:00":
                print("No encontramos paraderos cerca de tu ubicación con "
                      "recorridos que lleguen al destino indicado, "
                      "puede ingresar a continuación otra búsqueda :D")
                raise Volver()
            else:
                tiempo_llegada = obtener_tiempo_llegada(mas_cercano[1],
                                                        mas_cercano[0][0])
                nombre_paradero = obtener_nombre_paradero(mas_cercano[1])
                print(f"Paradero disponible más cercano a ti ---> "
                      f"{nombre_paradero}")
                print(f"Recorrido a seguir (bus) ---> {mas_cercano[0][0]}")
                print(f"Tiempo estimado de llegada del bus ---> {tiempo_llegada}")
                print(f"El destino se encuentra aproximadamente a ---> "
                      f"{round(distancia_total, 2)} km")
                print(f"Duración estimada de viaje ---> {duracion_viaje}")
        except Volver:
            pass
        except VolverMenu:
            raise VolverMenu()

