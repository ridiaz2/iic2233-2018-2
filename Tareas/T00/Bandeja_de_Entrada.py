from collections import namedtuple
from Correo import dudas_input, imprimir_mensaje
from Encriptacion import desencriptar

def obtener_datos():
    archivo = open("./data/db_emails.csv", "r", encoding="utf-8")
    lista_datos = archivo.readlines()[1:]
    archivo.close()
    archivo = open("./datos/correos_enviados.csv", "r", encoding="utf-8")
    lista_datos.extend(archivo.readlines()[1:])
    archivo.close()
    datos = []
    Correo = namedtuple("Correo", ["usuario", "destinatarios", "asunto",
                                   "mensaje", "etiquetas"])
    for i in range(len(lista_datos)):
        indice_1 = lista_datos[i].find("'")
        indice_2 = lista_datos[i].rfind("'")
        lista = lista_datos[i][:indice_1-1].split(",")
        lista.append(lista_datos[i][indice_1+1:indice_2])
        lista.extend(lista_datos[i][indice_2+2:].strip().split(","))
        lista[1] = set(lista[1].split(";"))
        lista[4] = set(lista[4].split(";"))
        datos.append(Correo(lista[0], lista[1], lista[2], lista[3], lista[4]))
    return datos

def obtener_recibidos(usuario, datos):
    recibidos = []
    for i in datos:
        if usuario in i.destinatarios:
            recibidos.append(i)
    return recibidos[::-1]

usuario = "albertmorales@yahoo.com"
recibidos = obtener_recibidos(usuario, obtener_datos())

def es_numero(numero, largo):
    if numero == "":
        return True
    numeros = "0123456789"
    rango = range(1, largo+1)
    for i in numero:
        if not i in numeros:
            return False
    if not int(numero) in rango:
        return False
    return True

def resumen_destinatarios(destinatarios, opcion="destinatarios"):
    if opcion == "destinatarios":
        titulo = "Para"
    else:
        titulo = "Invitados"
    lista = list(destinatarios)
    if len(lista) > 8:
        print(imprimir_mensaje(f"{titulo}: " + ", ".join(lista[:2]) +
              " y otros (" + str(len(lista)-2) + f") {opcion} más"))
        return True
    else:
        print(imprimir_mensaje(f"{titulo}: " + ", ".join(lista), ","))
        return False


def mostrar_correo(correo):
    print("_"*80)
    print(correo.asunto)
    print("-"*80)
    print("De: " + correo.usuario)
    mas_destinatarios = resumen_destinatarios(correo.destinatarios)
    print("-"*80)
    print(imprimir_mensaje(desencriptar(correo.mensaje)))
    print("-"*80)
    print(", ".join(correo.etiquetas))
    print("_"*80)
    if mas_destinatarios:
        print("[0] Mostrar lista de destinatarios completa")
    print("[1] Volver al Menú")
    print("[Enter] para volver a la Bandeja de Entrada")
    opcion = input().strip()
    while not opcion in ["0", "1", ""]:
        opcion = dudas_input()
    if opcion == "0":
        print(imprimir_mensaje(", ".join(correo.destinatarios), ","))
        print("[1] Volver al Menú")
        print("[Enter] para volver a la Bandeja de Entrada")
        opcion = input().strip()
        while not opcion in ["1", ""]:
            opcion = dudas_input()
    if opcion == "1":
        return "menú"
    else:
        return "bandeja"



def bandeja(usuario, recibidos):
    repetir = True
    while repetir:
        print("_"*80)
        print("Bandeja de Entrada:",usuario[:usuario.find("@")])
        print("_"*80)
        for i in range(len(recibidos)):
            print("| [" + str(i+1) + "] " + recibidos[i].asunto)
            print("|    " + (" "*len(str(i+1))) + "" + " . ".join(recibidos[
                                                          i].etiquetas) + "")
            print("-"*57)
        print("Ingrese el {numero} del correo que desea revisar: ")
        print("[Enter] para volver al Menú")
        numero = input()
        while not es_numero(numero, len(recibidos)):
            if numero == "":
                continue
            numero = dudas_input()
        if numero == "":
            return "menu"
        revisar = recibidos[int(numero)-1]
        opcion = mostrar_correo(revisar)
        if opcion == "bandeja":
            repetir = True
        elif opcion == "menú":
            repetir = False
            continue

#bandeja(usuario, recibidos)