from collections import namedtuple, defaultdict, deque

"""
Aquí están las estructuras de datos para guardar la información respectiva.

NO MODIFICAR.
"""

# Como se vio en la ayudantía, hay varias formas de declarar una namedtuple :)
Entrenador = namedtuple('Entrenador', 'nombre apellido')
Pokemon = namedtuple('Pokemon', ['nombre', 'tipo', 'max_solicitudes'])
Solicitud = namedtuple('Solicitud', ['id_entrenador', 'id_pokemon'])

################################################################################
"""
En esta sección debe completar las funciones para cargar los archivos al sistema.

Puedes crear funcionas auxiliar si tú quieres, ¡pero estas funciones DEBEN
retornar lo pedido en el enunciado!
"""

def cargar_entrenadores(ruta_archivo):
    """
    Esta función debería leer el archivo archivo_entrenadores y cargarlo usando
    las estructuras entregadas.
    """
    file = open(ruta_archivo, 'r', encoding='utf-8')
    Entrenadores = {}
    for linea in file:
        datos = linea.strip().split(";")
        Entrenadores[datos[0]] = Entrenador(datos[1], datos[2])
    file.close()
    return Entrenadores


def cargar_pokemones(ruta_archivo):
    """
    Esta función debería leer el archivo archivo_pokemones y cargarlo usando las
    estructuras entregadas.
    """
    file = open(ruta_archivo, 'r', encoding='utf-8')
    Pokemones = {}
    for linea in file:
        datos = linea.strip().split(";")
        Pokemones[datos[0]] = Pokemon(datos[1], datos[2], datos[3])
    file.close()
    return Pokemones


def cargar_solicitudes(ruta_archivo):
    """
    Esta función debería leer el archivo archivo_solicitudes y cargarlo usando
    las estructuras entregadas.
    """
    file = open(ruta_archivo, 'r', encoding='utf-8')
    Solicitudes = deque()
    lista = []
    for linea in file:
        datos = linea.strip().split(";")
        Solicitudes.append(Solicitud(datos[0], datos[1]))
    file.close()
    return Solicitudes


################################################################################

"""
Lógica del Sistema.
Debes completar esta función como se dice en el enunciado.
"""

def sistema(modo, entrenadores, pokemones, solicitudes):
    """
    Esta función se encarga de llevar a cabo la 'simulación', de acuerdo al modo
    entregado.
    """
    lista = []
    Registro = {}
    maximos = defaultdict(int)
    for id in pokemones.keys():
        maximos[id] = int(pokemones[id].max_solicitudes)
    if modo == "1":
        solicitud = solicitudes.popleft()
        if maximos[solicitud.id_pokemon] > 0:
            if not solicitud.id_entrenador in Registro:
                Registro[solicitud.id_entrenador].add(pokemones[solicitud.id_pokemon])
                maximos[solicitud.id_pokemon] -= 1
            else:
                Registro[solicitud.id_entrenador] = set([pokemones[solicitud.id_pokemon].nombre])
                maximos[solicitud.id_pokemon] -= 1
    elif modo == "2":
        solicitud = solicitudes.pop()
        if maximos[solicitud.id_pokemon] > 0:
            if not solicitud.id_entrenador in Registro:
                Registro[solicitud.id_entrenador].add(pokemones[solicitud.id_pokemon])
                maximos[solicitud.id_pokemon] -= 1
            else:
                Registro[solicitud.id_entrenador] = set([pokemones[solicitud.id_pokemon].nombre])
                maximos[solicitud.id_pokemon] -= 1

    return Registro

################################################################################
"""
Funciones de consultas, deben rellenarlos como dice en el enunciado :D.
"""

def pokemones_por_entrenador(id_entrenador, resultado_simulacion):
    """
    Esta función debe retornar todos los pokemones que ganó el entrenador con el
    id entregado.

    Recuerda que esta función debe retornar una lista.
    """
    lista = []
    return list(resultado_simulacion[id_entrenador])

def mismos_pokemones(id_entrenador1, id_entrenador2, resultado_simulacion):
    """
    Esta función debe retornar todos los pokemones que ganó tanto el entrenador
    con el id_entrenador1 como el entrenador con el id_entrenador2.

    Recuerda que esta función debe retornar una lista.
    """
    return list(resultado_simulacion[id_entrenador1] & resultado_simulacion[id_entrenador2])

def diferentes_pokemones(id_entrenador1, id_entrenador2, resultado_simulacion):
    """
    Esta función debe retornar todos los pokemones que ganó el entrenador con
    id_entrenador1 y que no ganó el entrenador con id_entrenador2.

    Recuerda que esta función debe retornar una lista.
    """
    return list(resultado_simulacion[id_entrenador1] - resultado_simulacion[id_entrenador2])


if __name__ == '__main__':

    ############################################################################
    """
    Poblando el sistema.
    Ya se hacen los llamados a las funciones, puedes imprimirlos para ver si se
    cargaron bien.
    """

    entrenadores = cargar_entrenadores('entrenadores.txt')
    pokemones = cargar_pokemones('pokemones.txt')
    solicitudes = cargar_solicitudes('solicitudes.txt')

    # print(entrenadores)
    # print(pokemones)
    # print(solicitudes)

    ################################   MENU   ##################################
    """
    Menú.
    ¡No debes cambiar nada! Simplemente nota que es un menú que pide input del
    usuario, y en el caso en que este responda con "1" ó "2", entonces se hace
    el llamado a la función. En otro caso, el programa termina.
    """

    eleccion = input('Ingrese el modo de lectura de solicitudes:\n'
                 '1: Orden de llegada\n'
                 '2: Orden Inverso de llegada\n'
                 '>\t')

    if eleccion in {"1", "2"}:
        resultados_simulacion = sistema(eleccion, entrenadores,
                                        pokemones, solicitudes)
    else:
        exit()

    ##############################   Pruebas   #################################
    """
    Casos de uso.

    Aquí pueden probar si sus consultas funcionan correctamente.
    """
