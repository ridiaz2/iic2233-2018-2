from collections import namedtuple
from Correo import error_usuario, dudas_input
from Bandeja_de_Entrada import bandeja, obtener_datos, obtener_recibidos
from Correo import plataforma_correo
from Calendario import buscador_evento, obtener_eventos
from Eventos import evento_nuevo


def menu_principal():
    print("_" * 80)
    print("DCCorreos")
    print("_" * 80)
    print("¡Bienvenido!")
    print("¿Qué acción deseas realizar?")
    print("[0] Iniciar Sesión")
    print("[1] Crear Nueva Cuenta")
    opcion = input()
    while opcion not in ["0", "1"]:
        print("Lo sentimos, estamos teniendo dificultades para entender tu "
              "respuesta")
        print("Por favor, inténtelo de nuevo :D")
        opcion = input()
    if opcion == "0":
        usuario = iniciar_sesion(abrir_datos_usuarios())
    if opcion == "1" or opcion == "":
        usuario = nuevo_usuario(abrir_datos_usuarios())
    while True:
        print("_"*80)
        print("Menú Principal: "+usuario)
        print("_"*80)
        print("¿Qué acción deseas realizar?")
        print("[0] Bandeja de Entrada")
        print("[1] Enviar correo")
        print("[2] Buscar evento en calendario")
        print("[3] Crear un evento")
        print("[Enter] Cerrar Sesión")
        opcion = input()
        while opcion not in ["0", "1", "2", "3", ""]:
            print("Lo sentimos, no entendimos tu respuesta")
            print("Por favor, inténtelo de nuevo :D")
            opcion = input()
        if opcion == "0":
            bandeja(usuario, obtener_recibidos(usuario, obtener_datos()))
        elif opcion == "1":
            plataforma_correo(usuario)
        elif opcion == "2":
            buscador_evento(obtener_eventos(), usuario)
        elif opcion == "3":
            evento_nuevo(usuario, obtener_eventos())
        else:
            return ""


def abrir_datos_usuarios():
    archivo = open("./data/db_users.csv", "r", encoding="utf-8")
    lista_datos = archivo.readlines()[1:]
    archivo.close()
    archivo = open("./datos/usuarios.csv", "r", encoding="utf-8")
    lista_datos.extend(archivo.readlines()[1:])
    datos = {}
    for i in lista_datos:
        lista = i.split(",")
        datos[lista[0]] = lista[1].strip()
    return datos

def iniciar_sesion(datos):
    print("_"*80)
    print("Inicio de Sesión")
    print("_"*80)
    usuario = input("Correo electrónico: ")
    while not usuario in datos:
        print("-"*80)
        print("No encontramos este nombre de usuario en nuestra base de datos")
        print("Puede ingresar nuevamente un nombre de usuario")
        print("O presionar [Enter] para crear una nueva cuenta")
        print("-"*80)
        usuario = input("Correo electrónico: ")
        if usuario == "":
            return "usuario_nuevo"
    contraseña = input("Contraseña: ")
    while datos[usuario] != contraseña:
        print("-"*80)
        print("Contraseña incorrecta, por favor inténtelo de nuevo :D")
        print("O puede presionar [Enter] para volver al menú de inicio")
        print("-"*80)
        contraseña = input("Contraseña: ")
        if contraseña == "":
            return "volver_menú"
    print("¡Bienvenido, " + usuario[:usuario.find("@")] + "!")
    return usuario


def validar_usuario(datos, usuario):
    if usuario.find("@") == -1:
        return False
    if usuario in datos:
        return False
    if not error_usuario(usuario):
        return False
    return True

def agregar_usuario(usuario, contraseña):
    archivo = open("./datos/usuarios.csv", "r", encoding="utf-8")
    lista_datos = archivo.readlines()
    archivo.close()
    archivo = open("./datos/usuarios.csv", "w", encoding="utf-8")
    datos = "".join(lista_datos) + "\n"
    datos += ",".join([usuario, contraseña])
    archivo.write(datos)
    archivo.close()
    print("¡Cuenta creada con éxito!")

def nuevo_usuario(datos):
    print("_"*80)
    print("Nueva Cuenta")
    print("_"*80)
    usuario = input("Correo electrónico: ")
    while not validar_usuario(datos, usuario):
        print("-"*80)
        indice_arroba = usuario.find("@")
        indice_punto = usuario[indice_arroba:].find(".")
        if usuario in datos:
            print("Este usuario ya existe")
        elif indice_arroba == -1:
            print("Lo sentimos, nuestra plataforma solo acepta correos cuya "
                  "dirección incluya un @")
        elif usuario[:indice_arroba].count(",") > 0 or usuario[
            indice_arroba].count(".") > 0:
            print("Lo sentimos, nuestra plataforma no acepta usuarios con "
                  "puntos y/o comas")
        elif  indice_arroba == -1 or indice_arroba == len(usuario)-1 or \
                        indice_punto  == -1 or indice_punto ==\
                        len(usuario[indice_arroba:])-1:
            if indice_arroba == len(usuario)-1:
                print("Lo sentimos, puede que tu usuario no incluya un "
                      "servidor después de @")
            else:
                print("Lo sentimos, puede que el servidor " + usuario[
                    indice_arroba + 1:] + " no exista")
        print("Por favor, inténtelo de nuevo :D")
        print("O presione [Enter] para volver al menú de inicio")
        print("-"*80)
        usuario = input("Correo electrónico: ")
        if usuario == "":
            return "volver_menú"
    contraseña = input("Contraseña: ")
    while contraseña.count(",") > 0 or contraseña.count(".") > 0 or len(
            contraseña) < 6:
        print("-"*80)
        if (contraseña.count(",") > 0 or contraseña.count(".") > 0) and len(
                contraseña) < 6:
            print("Lo sentimos, nuestra plataforma solo acepta contraseñas sin "
                  "signos de puntuación)")
            print("Y con un mínimo de seis caracteres")
        if contraseña.count(",") > 0 or contraseña.count(".") > 0:
            print("Lo sentimos, nuestra plataforma no acepta contraseñas con "
                  "signos de puntuación")
        else:
            print("Lo sentimos, nuestra plataforma solo acepta contraseñas")
            print("de seis carácteres como nínimo")
        print("Por favor, inténtelo de nuevo :D")
        print("O presione [Enter] para volver al menú de inicio")
        print("-" * 80)
        contraseña = input("Contraseña: ")
        if contraseña == "":
            return "volver_menú"
    agregar_usuario(usuario, contraseña)
    return usuario

def menu_inicio():
    datos = abrir_datos_usuarios()
    while True:
        print("_"*80)
        print("DCCorreos")
        print("_"*80)
        print("Menú de Inicio")
        print("[1] Iniciar Sesión")
        print("[2] Crear cuenta")
        opcion = input()
        while not opcion in ["1", "2"]:
            opcion = dudas_input()
        if opcion == "1":
            usuario = iniciar_sesion(datos)
            if usuario == "usuario_nuevo":
                opcion = 2
            elif usuario == "volver_menú":
                pass
            else:
                return usuario
        if opcion == "2":
            usuario = nuevo_usuario(datos)
            if usuario == "volver_menú":
                pass
            else:
                return usuario

while True:
    menu_principal()

