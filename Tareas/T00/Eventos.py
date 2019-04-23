from Calendario import obtener_eventos, error_fecha, transformar_fecha, \
    Evento, mostrar_info_evento, generar_id, cero, transformar_fecha_inverso
from Correo import dudas_caracteres, error_destinatarios, dudas_input
from datetime import datetime as Fecha
from datetime import timedelta


def comparar_fechas(fecha_i, fecha_f):
    if fecha_f == "":
        return True
    fecha_f = transformar_fecha(fecha_f, True)
    if fecha_f < fecha_i:
        return False
    return True



def modificar_evento(usuario, nombre, fecha_i, fecha_f, descripcion, invitados,
                     etiquetas, opcion):
    while opcion != "":
        print("[1] Modificar Nombre")
        print("[2] Modificar Fecha de Inicio")
        print("[3] Modificar Fecha de Cierre")
        print("[4] Modificar Descripción")
        print("[5] Modificar Invitados")
        print("[6] Modificar Etiquetas")
        print("[Enter] para crear evento")
        opcion = input()
        while opcion not in ["1", "2", "3", "4", "5", "6", ""]:
            opcion = dudas_input()
        if opcion == "1":
            print("_" * 80)
            print("| Nombre")
            nombre = input("| ")
            while len(nombre) > 50 or len(nombre) < 6:
                nombre = dudas_caracteres("Nombre del Evento", 50, nombre, 6)
            print("_" * 80)
        elif opcion == "2":
            print("_"*80)
            fecha_i = input("| Desde: ")
            while not error_fecha(fecha_i):
                print(
                    "Lo sentimos, tenemos problemas con interpretar esta fecha.")
                print(
                    "El formato de fecha que soportamos es DD-MM-AAAA hh-mm-ss")
                print("Por ejemplo: '01-08-2018', o '01-08-2018 01-20-30'")
                print(
                    "Por favor, inténtelo de nuevo, o presione ENTER para utilizar "
                    "la fecha actual")
                fecha_i = input("| Fecha de inicio (DD-MM-AAAA): ")
            if fecha_i == "":
                fecha_i = Fecha.today()
            if not type(fecha_i) == Fecha:
                fecha_i = transformar_fecha(fecha_i, True)
            print("_"*80)
        elif opcion == "3":
            print("_"*80)
            fecha_f = input("| Hasta: ")
            while not error_fecha(fecha_f) or not comparar_fechas(fecha_i,
                                                                  fecha_f):
                if not error_fecha(fecha_f):
                    print(
                        "Lo sentimos, tenemos problemas con interpretar esta fecha.")
                    print(
                        "El formato de fecha que soportamos es DD-MM-AAAA hh-mm-ss")
                    print("Por ejemplo: '01-08-2018', o '01-08-2018 01-20-30'")
                    print(
                        "Por favor, inténtelo de nuevo, o presione ENTER para "
                        "utilizar "
                        "la fecha correspondiente a una hora después de la inicial")
                if not comparar_fechas(fecha_i, fecha_f):
                    print(
                        "Lo sentimos, la fecha de cierre debe ocurrir después que "
                        "la de inicio.")
                    print(
                        "Por favor, inténtelo de nuevo, o presione ENTER para "
                        "utilizar la fecha correspondiente a una hora después de la "
                        "inicial")
                fecha_f = input("| Fecha de cierre (DD-MM-AAAA): ")
            if fecha_f == "":
                fecha_f = fecha_i + timedelta(hours=1)
            if not type(fecha_f) == Fecha:
                fecha_f = transformar_fecha(fecha_f, True)
            print("_"*80)
        elif opcion == "4":
            print("_"*80)
            print("| Descripción")
            descripcion = input("| ")
            if descripcion == "":
                descripcion = "sin descripcion"
            print("_"*80)
        elif opcion == "5":
            print("_"*80)
            print("| Invitados (separados por coma, en caso de ser más de uno)")
            invitados = input("| ")
            if invitados == "":
                invitados = "sin invitados"
            else:
                invitados = ";".join(error_destinatarios(invitados))
            print("_"*80)
        elif opcion == "6":
            print("_"*80)
            print("| Etiquetas (separadas por coma)")
            etiquetas = (";").join(input("| ").split(","))
            if etiquetas == "":
                etiquetas = "sin etiquetas"
            print("_"*80)
        else:
            continue
        if type(fecha_i) == Fecha:
            fecha_i_i, fecha_f_i = map(transformar_fecha_inverso,
                                   [fecha_i, fecha_f])
        else:
            fecha_i_i, fecha_f_i = fecha_i, fecha_f
            fecha_i, fecha_f = map(transformar_fecha,
                                       [fecha_i, fecha_f])
        evento_actual = Evento(usuario, nombre, fecha_i, fecha_f, descripcion,
                               invitados, etiquetas,
                               generar_id([usuario, nombre,
                                           fecha_i_i, fecha_f_i]))
        mostrar_info_evento(evento_actual)
        print("¿Desea realizar algún cambio?")
    return usuario, nombre, fecha_i, fecha_f, descripcion, invitados, etiquetas

def crear_evento(usuario, nombre, fecha_i, fecha_f, descripcion, invitados,
                     etiquetas):
    archivo = open("./datos/eventos.csv", "r", encoding="utf-8")
    lista_datos = archivo.readlines()
    archivo.close()
    archivo = open("./datos/eventos.csv", "w", encoding="utf-8")
    datos = "".join(lista_datos) + "\n"
    datos += ",".join([usuario, f"'{nombre}'", fecha_i, fecha_f,
                       f"'{descripcion}'", invitados, etiquetas])
    archivo.write(datos)
    archivo.close()
    print("¡Evento creado con éxito!")

def evento_nuevo(usuario, datos):
    print("_" * 80)
    print("Evento nuevo")
    print("_" * 80)
    print("| Nombre")
    nombre = input("| ")
    while len(nombre) > 50 or len(nombre) < 6:
        nombre = dudas_caracteres("Nombre del Evento", 50, nombre, 6)
    print("-" * 80)
    fecha_i = input("| Desde: ")
    while not error_fecha(fecha_i):
        print("Lo sentimos, tenemos problemas con interpretar esta fecha.")
        print("El formato de fecha que soportamos es DD-MM-AAAA hh-mm-ss")
        print("Por ejemplo: '01-08-2018', o '01-08-2018 01-20-30'")
        print("Por favor, inténtelo de nuevo, o presione ENTER para utilizar "
              "la fecha actual")
        fecha_i = input("| Fecha de inicio (DD-MM-AAAA): ")
    if fecha_i == "":
        fecha_i = Fecha.today()
    if not type(fecha_i) == Fecha:
        fecha_i = transformar_fecha(fecha_i, True)
    fecha_f = input("| Hasta: ")
    while not error_fecha(fecha_f) or not comparar_fechas(fecha_i, fecha_f):
        if not error_fecha(fecha_f):
            print("Lo sentimos, tenemos problemas con interpretar esta fecha.")
            print("El formato de fecha que soportamos es DD-MM-AAAA hh-mm-ss")
            print("Por ejemplo: '01-08-2018', o '01-08-2018 01-20-30'")
            print("Por favor, inténtelo de nuevo, o presione ENTER para "
                  "utilizar "
                  "la fecha correspondiente a una hora después de la inicial")
        if not comparar_fechas(fecha_i, fecha_f):
            print("Lo sentimos, la fecha de cierre debe ocurrir después que "
                  "la de inicio.")
            print("Por favor, inténtelo de nuevo, o presione ENTER para "
                  "utilizar la fecha correspondiente a una hora después de la "
                  "inicial")
        fecha_f = input("| Fecha de cierre (DD-MM-AAAA): ")
    if fecha_f == "":
        fecha_f = fecha_i + timedelta(hours=1)
    if not type(fecha_f) == Fecha:
        fecha_f = transformar_fecha(fecha_f, True)
    print("-"*80)
    print("| Descripción")
    descripcion = input("| ")
    if descripcion == "":
        descripcion = "sin descripcion"
    print("-" * 80)
    print("| Invitados (separados por coma, en caso de ser más de uno)")
    invitados = input("| ")
    if invitados == "":
        invitados = "sin invitados"
    else:
        invitados = ";".join(error_destinatarios(invitados))
    print("-" * 80)
    print("| Etiquetas (separadas por coma)")
    etiquetas = (";").join(input("| ").split(","))
    if etiquetas == "":
        etiquetas = "sin etiquetas"
    print("_" * 80)
    print("Resumen del evento:")
    fecha_i_i, fecha_f_i = map(transformar_fecha_inverso, [fecha_i, fecha_f])
    evento_actual = Evento(usuario, nombre, fecha_i, fecha_f, descripcion,
                           invitados, etiquetas, generar_id([usuario, nombre,
                            fecha_i_i, fecha_f_i]))
    mostrar_info_evento(evento_actual, True)
    valido = False
    print("¿Desea realizar algún cambio?")
    while not valido:
        opcion = "0"
        usuario, nombre, fecha_i, fecha_f, descripcion, invitados, etiquetas = \
            modificar_evento(
            usuario, nombre, fecha_i, fecha_f, descripcion, invitados,
            etiquetas, opcion)
        if type(fecha_i) == Fecha:
            fecha_i, fecha_f = map(transformar_fecha_inverso,
                                   [fecha_i, fecha_f])
        i = 0
        valido = True
        while valido and i < len(datos):
            evento = datos[i]
            if evento.id == generar_id([usuario, nombre, fecha_i, fecha_f]):
                print("Detectamos que existe un evento creado por ti con el "
                      "mismo título y fechas")
                print("Lo sentimos, pero nuestro sistema no soporta estas "
                      "coincidencias")
                print("Por favor, realiza alguna modificación :D")
                valido = False
            i += 1

    crear_evento(usuario, nombre, fecha_i, fecha_f, descripcion, invitados,
                     etiquetas)

