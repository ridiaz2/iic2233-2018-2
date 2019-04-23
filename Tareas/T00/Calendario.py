from collections import namedtuple
from datetime import datetime as Fecha
from Bandeja_de_Entrada import es_numero, resumen_destinatarios
from Correo import dudas_input, imprimir_mensaje
from calendar import Calendar
from Correo import error_destinatarios

def transformar_fecha_inverso(fecha):
    return f"{fecha.year}-{cero(fecha.month)}-{cero(fecha.day)} " \
           f"{cero(fecha.hour)}:{cero(fecha.minute)}:{cero(fecha.second)}"

def archivo_perteneciente(evento):
    with open("data/db_events.csv", encoding="utf-8") as archivo:
        i = 0
        fecha_i, fecha_f = map(transformar_fecha_inverso, [evento.fecha_i,
                                                           evento.fecha_f])
        for linea in archivo:

            if ",".join([evento.propietario, f"'{evento.nombre}'", fecha_i,
                         fecha_f, f"'{evento.descripcion}'"]) in linea.strip():
                return f"0{i}"
            i += 1
    with open("datos/eventos.csv", encoding="utf-8") as archivo:
        i = 0
        for linea in archivo:
            if ",".join([evento.propietario, f"'{evento.nombre}'", fecha_i,
                         fecha_f, f"'{evento.descripcion}'"]) in linea.strip():
                return f"1{i}"
            i += 1

def transformar_fecha(fecha, orden=False):
    fecha = fecha.strip()
    if orden:
        j = [6, -2, -8]
    else:
        j = [0 for i in range(3)]
    año = int(fecha[j[0]:4+j[0]])
    mes = int(fecha[5+j[1]:7+j[1]])
    dia = int(fecha[8+j[2]:10+j[2]])
    if len(fecha) == 10:
        return Fecha(año, mes, dia)
    hora = int(fecha[11:13])
    min = int(fecha[14:16])
    seg = int(fecha[17:19])
    return Fecha(año, mes, dia, hora, min, seg)

def generar_id(lista):
    propietario = lista[0]
    nombre = lista[1]
    fecha_i = lista[2]
    fecha_f = lista[3]
    id = fecha_i.replace("-","").replace(":","").replace(" ","")
    id += fecha_f.replace("-", "").replace(":", "").replace(" ", "")
    id += nombre
    id += propietario
    return id

Evento = namedtuple("Evento", ["propietario", "nombre", "fecha_i",
                                   "fecha_f", "descripcion", "invitados",
                                   "etiquetas", "id"])

def obtener_eventos():
    archivo = open("./data/db_events.csv", "r", encoding="utf-8")
    lista_datos = archivo.readlines()[1:]
    archivo.close()
    archivo = open("./datos/eventos.csv", "r", encoding="utf-8")
    lista_datos.extend(archivo.readlines()[1:])
    archivo.close()
    datos = []

    for i in range(len(lista_datos)):
        indice_1 = lista_datos[i].find("'")
        indice_2 = lista_datos[i][indice_1+1:].find("'") + indice_1 + 1
        indice_4 = lista_datos[i].rfind("'")
        indice_3 = lista_datos[i][indice_2+1:indice_4].find("'") + indice_2 + 1
        lista = lista_datos[i][:indice_1 - 1].split(",")
        lista.append(lista_datos[i][indice_1 + 1:indice_2])
        lista.extend((lista_datos[i][indice_2 + 2:indice_3 - 1]).split(","))
        lista.append(lista_datos[i][indice_3 + 1:indice_4])
        lista.extend(lista_datos[i][indice_4 + 2:].strip().split(","))
        lista.append(generar_id(lista))
        lista[2] = transformar_fecha(lista[2])
        lista[3] = transformar_fecha(lista[3])
        #lista[5] = set(lista[5].split(";"))
        #lista[6] = set(lista[6].split(";"))
        datos.append(Evento(lista[0], lista[1], lista[2], lista[3], lista[4],
                            lista[5], lista[6], lista[7]))
    #datos = sorted(datos, key=ordenar_eventos)
    return datos

def fechas_coinciden(fecha, fecha_i, fecha_f): #DLKJDÑLKJDLK
    fecha = fecha.lower()
    meses_escritos = "enero.febrero.marzo.abril.mayo.junio.agosto.septiembre" \
                     ".octubre.noviembre.diciembre".split(".")
    meses_ingles = "january.february.march.april.may.june.july.august" \
                   ".september.october.november.december".split(".")

def error_fecha(fecha):
    if fecha == "":
        return True
    fecha = fecha.lower().strip()
    numeros = list("0123456789")
    if len(fecha) != 10 and len(fecha) != 19:
        return False
    for i in range(10):
        if i in [0, 1, 3, 4, 6, 7, 8, 9, 11, 12, 14, 15, 17, 18]:
            if fecha[i] not in numeros:
                return False
        elif i == 10 and fecha[i] != " ":
            return False
        elif i in [2, 5] and fecha[i] != "-":
            return False
        elif i in [13, 16] and fecha[i] != ":":
            return False
    j = [6, -2, -8]
    año = int(fecha[6:10])
    mes = int(fecha[3:5])
    dia = int(fecha[0:2])
    if mes > 12:
        return False
    lista_dias = list(Calendar().itermonthdays(año, mes))
    if dia > max(lista_dias):
        return False
    if len(fecha) == 10:
        return True
    hora = int(fecha[11:13])
    min = int(fecha[14:16])
    seg = int(fecha[17:19])
    if hora > 23 or min > 59 or seg > 59:
        return False
    return True

def ordenar_eventos(evento):
    return evento.id

def buscar_fecha(mes, fecha):
    dias = "Lunes,Martes,Miércoles,Jueves,Viernes,Sábado,Domingo".split(",")
    for semana in mes:
        for dia in semana:
            if fecha == dia[0]:
                return dias[dia[1]]
def cero(fecha):
    if len(str(fecha)) == 1:
        return f"0{str(fecha)}"
    return str(fecha)

def mostrar_fecha(fecha_i, fecha_f):
    meses = "enero,febrero,marzo,abril,mayo,junio,agosto,septiembre,octubre," \
            "noviembre,diciembre".split(",")
    if fecha_i.date() == fecha_f.date():
        if Fecha.today().year == fecha_i.day:
            año = ""
        else:
            año = f" de {fecha_i.year}"
        calendario_mes = Calendar().monthdays2calendar(fecha_i.year,
                                                     fecha_i.month)
        dia = buscar_fecha(calendario_mes, fecha_i.day)
        return f"{dia}, {fecha_i.day} de {meses[fecha_i.month]}" \
               f"{año}\n{cero(fecha_i.hour)}:{cero(fecha_i.minute)}:" \
               f"{cero(fecha_i.second)} - " \
               f"{cero(fecha_f.hour)}:{cero(fecha_f.minute)}:" \
               f"{cero(fecha_f.second)}"
    else:
        return f"{fecha_i.day} de {meses[fecha_i.month]} de " \
               f"{fecha_i.year}, " \
               f"{cero(fecha_i.hour)}:{cero(fecha_i.minute)}:" \
               f"{cero(fecha_i.second)} - " \
               f"{fecha_f.day} de {meses[fecha_f.month]} de " \
               f"{fecha_f.year}, " \
               f"{cero(fecha_f.hour)}:{cero(fecha_f.minute)}:" \
               f"{cero(fecha_f.second)}"

def modificar_evento_editor(evento, opcion):
    usuario = evento.propietario
    nombre = evento.nombre
    fecha_i = evento.fecha_i
    fecha_f = evento.fecha_f
    descripcion = evento.descripcion
    invitados = evento.invitados
    etiquetas = evento.etiquetas
    while opcion != "":
        print("[0] Modificar Nombre")
        print("[1] Modificar Fecha de Inicio")
        print("[2] Modificar Fecha de Cierre")
        print("[3] Modificar Descripción")
        print("[4] Modificar Etiquetas")
        print("[Enter] para volver")
        opcion = input()
        while opcion not in ["0", "1", "2", "3", "4", ""]:
            opcion = dudas_input()
        if opcion == "0":
            print("_" * 80)
            print("| Nombre")
            nombre = input("| ")
            while len(nombre) > 50 or len(nombre) < 6:
                nombre = dudas_caracteres("Nombre del Evento", 50, nombre, 6)
            print("_" * 80)
        elif opcion == "1":
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
        elif opcion == "2":
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
        elif opcion == "3":
            print("_"*80)
            print("| Descripción")
            descripcion = input("| ")
            if descripcion == "":
                descripcion = "sin descripcion"
            print("_"*80)
        elif opcion == "4":
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
        mostrar_info_evento(evento_actual, False, True)
        print("¿Desea realizar algún cambio?")
    return usuario, nombre, fecha_i, fecha_f, descripcion, invitados, etiquetas
def editar_evento(evento):
    print("_"*80)
    print("Editor de Eventos")
    print("_"*80)
    print("A continuación se presentan las acciones disponibles del editor")
    print("[0] Volver a Resultados de la búsqueda")
    print("[1] Editar atributos del evento")
    print("[2] Eliminar evento")
    print("[3] Agregar invitados")
    print("[Enter] Volver al Menú")
    opcion = input().lower()
    while opcion not in ["0", "1", "2", "3", ""]:
        print("Lo sentimos, estamos teniendo dificultades para entender tu "
              "respuesta")
        print("Por favor, inténtelo de nuevo :D")
        opcion = input().lower()
    if opcion in ["1", "2", "3"]:
        ubicacion = archivo_perteneciente(evento)
        file = int(ubicacion[0])
        indice = int(ubicacion[1])
        if file == 0:
            archivo = open("data/db_events.csv", "r", encoding="utf-8")
            lista_datos = archivo.readlines()
            archivo.close()
            archivo = open("data/db_events.csv", "w", encoding="utf-8")
        elif file == 1:
            archivo = open("./datos/eventos.csv", "r", encoding="utf-8")
            lista_datos = archivo.readlines()
            archivo.close()
            archivo = open("./datos/eventos.csv", "w", encoding="utf-8")
        if opcion == "1":
            mostrar_info_evento(evento, False, True)
            opcion = "0"
            usuario, nombre, fecha_i, fecha_f, descripcion, invitados, \
            etiquetas = modificar_evento_editor(evento, opcion)
            if type(fecha_i) == Fecha:
                fecha_i, fecha_f = map(transformar_fecha_inverso, [fecha_i,
                                                                   fecha_f])
            lista_a_unir = [usuario, f"'{nombre}'", fecha_i, fecha_f,
                            f"'{descripcion}'", invitados, etiquetas]
            lista_datos[indice] = ",".join(lista_a_unir) + "\n"
        elif opcion == "2":
            lista_datos.pop(indice)
        elif opcion == "3":
            print("A continuación puede agregar invitados")
            print("| Invitados (separados por coma, en caso de ser más de uno)")
            invitados = input("| ")
            if invitados == "":
                invitados = "sin invitados"
            else:
                invitados = ";".join(error_destinatarios(invitados))
            if "sin invitados" in lista_datos[indice]:
                lista_datos[indice] = lista_datos[indice].replace("sin "
                                                    "invitados", invitados)
            if invitados != "sin invitados":
                indice_coma = lista_datos[indice].rfind(",")
                lista_datos[indice] = lista_datos[indice][:indice_coma] + \
                                      ";" + invitados + lista_datos[indice][
                    indice_coma:]
            else:
                pass
        datos = "".join(lista_datos) + "\n"
        archivo.write(datos)
        archivo.close()

def mostrar_info_evento(evento, crear_evento=False, editor=False, usuario=""):
    print("_"*80)
    print(evento.nombre)
    print(imprimir_mensaje(mostrar_fecha(evento.fecha_i, evento.fecha_f)))
    print("-"*80)
    print("Creado por: " + evento.propietario)
    if crear_evento:
        print(imprimir_mensaje("Invitados: " +
                               ", ".join(evento.invitados.split(";"))))
    elif editor:
        pass
    else:
        mas_invitados = resumen_destinatarios(evento.invitados.split(";"),
                                          "invitados")
    print("-"*80)
    print(imprimir_mensaje(evento.descripcion))
    print("-"*80)
    print(imprimir_mensaje("Etiquetas: " +
                           ", ".join(evento.etiquetas.split(";"))))
    print("_"*80)
    if crear_evento or editor:
        return ""
    if mas_invitados:
        print("[0] Mostrar lista de invitados completa")
    print("[1] Volver al Menú")
    if usuario == evento.propietario:
        print("[2] Editar Evento")
    print("[Enter] para volver a los Resultados de Búsqueda")
    opcion = input().strip()
    while not opcion in ["0", "1", "", "2"]:
        opcion = dudas_input()
    if opcion == "0":
        print(imprimir_mensaje(", ".join(evento.invitados.split(";")), ","))
        print("[1] Volver al Menú")
        print("[2] Editar evento")
        print("[Enter] para volver a los Resultados de Búsqueda")
        opcion = input().strip()
        while not opcion in ["1", "", "2"]:
            opcion = dudas_input()
    if opcion == "2":
        editar_evento(evento)
        return "menu"
    if opcion == "1":
        return "menu"
    if opcion == "":
        return "volver"
    else:
        return "volver"

def mostrar_eventos(datos, buscador=False, usuario=""):
    if len(datos) == 0:
        print("Lo sentimos, no encontramos eventos que coincidan con la "
              "búsqueda")
        print("Por favor, inténtelo de nuevo :D")
        return "menu"
    repetir = True
    while repetir:
        if buscador:
            print("-"*80)
            print("Resultados de búsqueda")
            print("-"*80)
        for evento in enumerate(datos):
            print("| [" + str(evento[0] + 1) + "] " + evento[1].nombre)
        print("-"*80)
        print("Ingrese el {numero} del evento que desea revisar: ")
        print("[0] para realizar otra búsqueda")
        print("[Enter] para volver al Menú")
        numero = input()
        while not es_numero(numero, len(datos)):
            if numero == "":
                continue
            numero = dudas_input()
        if numero == "":
            return "menu"
        opcion = mostrar_info_evento(datos[int(numero) - 1], usuario=usuario)
        if opcion == "volver":
            repetir = True
        elif opcion == "menu":
            return opcion



def buscador_evento(datos, usuario):
    repetir = True
    while repetir:
        print("_"*80)
        print("Buscador de Eventos")
        print("_"*80)
        print("Se presentarán los campos de intervalo de tiempo, nombre y "
              "etiquetas.")
        print("Puede escribir los filtros a continuación")
        print("Presione [Enter] si prefiere no especificar un campo")
        fecha_i = input("Fecha de inicio: ").lower()
        while not error_fecha(fecha_i):
            print("Lo sentimos, tenemos problemas con interpretar esta fecha.")
            print("El formato de fecha que soportamos es DD-MM-AAAA hh-mm-ss")
            print("Por ejemplo: '01-08-2018', o '01-08-2018 01-20-30'")
            print("Por favor, inténtelo de nuevo, o presione ENTER para saltar "
                  "este paso")
            fecha_i = input("Fecha de inicio (DD-MM-AAAA): ").lower()
        fecha_f = input("Fecha de cierre: ").lower()
        while not error_fecha(fecha_f):
            print("Lo sentimos, tenemos problemas con interpretar esta fecha.")
            print("El formato de fecha que soportamos es DD-MM-AAAA")
            print("Por ejemplo: 01-08-2018")
            print("Por favor, inténtelo de nuevo, o presione ENTER para saltar "
                  "este paso")
            fecha_i = input("Fecha de cierre (DD-MM-AAAA): ").lower()

        nombre = input("Nombre: ").lower()
        etiquetas = input("Etiquetas (separadas por coma): ").lower().split(",")
        listo_fi, listo_ff, listo_nombre, listo_etiquetas = [False for i in
                                                             range(4)]
        fecha_i_set, fecha_f_set, nombre_set, etiquetas_set = [set() for i in
                                                             range(4)]
        if fecha_i == "":
            listo_fi = True
            fecha_i_set = set(datos)
        else:
            fecha_i= transformar_fecha(fecha_i, True)
        if fecha_f == "":
            listo_ff = True
            fecha_f_set = set(datos)
        else:
            fecha_f = transformar_fecha(fecha_f, True)
        if nombre == "":
            listo_nombre = True
            nombre_set = set(datos)
        if etiquetas == [""]:
            listo_etiquetas = True
            etiquetas_set = set(datos)
        listo_todo = False
        if listo_etiquetas and listo_ff and listo_fi and listo_nombre:
            listo_todo = True
            resultado_busqueda = set()
        for evento in datos:
            if usuario == evento.propietario or usuario in \
                    evento.invitados.split(";"):
                if listo_todo:
                    resultado_busqueda.add(evento)
                else:
                    if not listo_fi and evento.fecha_i >= fecha_i:
                            fecha_i_set.add(evento)
                    if not listo_ff and evento.fecha_f <= fecha_i:
                            fecha_f_set.add(evento)
                    if not listo_nombre and nombre in evento.nombre.lower():
                            nombre_set.add(evento)
                    if not listo_etiquetas:
                        etiqueta_encontrada = False
                        for etiquetas_de_evento in evento.etiquetas.split(";"):
                            if etiqueta_encontrada:
                                continue
                            for etiqueta_buscada in etiquetas:
                                if etiqueta_encontrada:
                                    continue
                                if etiqueta_buscada.strip() in etiquetas_de_evento.lower():
                                    etiqueta_encontrada = True
                        if etiqueta_encontrada:
                            etiquetas_set.add(evento)
        if not listo_todo:
            resultado_busqueda = fecha_i_set & fecha_f_set & \
                nombre_set & etiquetas_set
        resultado_busqueda = sorted(list(resultado_busqueda), key=ordenar_eventos)
        opcion = mostrar_eventos(resultado_busqueda, True, usuario)
        if opcion == "menu":
            repetir = False
        elif opcion == "volver":
            repetir = True


