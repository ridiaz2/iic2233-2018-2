from Encriptacion import encriptar


def obtener_etiquetas(numeros):
    etiquetas = ["sin clasificación", "Importante", "Publicidad", "Destacado",
                 "Newsletter"]
    lista = numeros.split(",")
    etiquetas_marcadas = []
    for i in lista:
        etiquetas_marcadas.append(etiquetas[int(i)])
    return ", ".join(etiquetas_marcadas)

def imprimir_mensaje(mensaje, caracter=" ", numero=78):
    mensaje_resto = mensaje
    mensaje_80 = ""
    while len(mensaje_resto) > numero:
        indice_espacio = mensaje_resto[:78].rfind(caracter)
        if indice_espacio == -1:
            indice_espacio = numero
        mensaje_80 += mensaje_resto[:indice_espacio] + "\n"
        mensaje_resto = mensaje_resto[indice_espacio+1:].strip()
    return mensaje_80 + mensaje_resto


def dudas_input():
    print("Estamos teniendo dificultades para entender su respuesta")
    print("Por favor, inténtelo de nuevo :D")
    opcion = input()
    return opcion

def dudas_caracteres(apartado, largo, texto, minimo=0):
    if minimo == 0:
        min = ""
    else:
        min = f" y un mínimo de {minimo}"
    print("Lo sentimos, el apartado de "+ apartado +" acepta como máximo " +
          str(largo) + f"{min}" + " caracteres")
    print("Por favor, inténtelo de nuevo :D")
    if len(texto) >= minimo:
        print("(Presione [Enter] para truncar automáticamente la cantidad de "
          "caracteres)")
    nuevo = input()
    if nuevo == "" and len(texto) >= minimo:
        nuevo = texto[:largo]
    return nuevo

def error_usuario(usuario):
    indice_arroba = usuario.find("@")
    if usuario.count("@") != 1:
        return False
    if indice_arroba == -1 or indice_arroba == len(usuario)-1:
        return False
    if usuario[:indice_arroba].count(",") > 0 or usuario[
                                                 :indice_arroba].count(".") > 0:
        return False
    indice_punto = usuario[indice_arroba:].find(".")
    if indice_punto == -1 or indice_punto == len(usuario[indice_arroba:])-1:
        return False
    return True


def error_destinatarios(destinatarios):
    destinatarios_set = set()
    errores = []
    for i in destinatarios.split(","):
        destinatarios_set.add(i.strip())
        if not error_usuario(i):
            errores.append(i.strip())
    vof = False
    enter = True
    while len(errores) > 0 and enter:
        vof = True
        print()
        if len(errores) > 1:
            print("Puede que los siguientes " + len(errores) + " usuarios de "
                  "correo no existan:")
        else:
            print("Puede que el siguiente usuario de correo no exista")
        print("-"*80)
        errores_texto = ", ".join(errores)
        print(imprimir_mensaje(errores_texto, ","))
        print("-"*80)
        print("Puede modificar a continuación los destinatarios detectados")
        print("O presionar [Enter] para continuar de todas formas :D")
        nuevo = input()
        if nuevo == "":
            enter = False
            continue
        nuevo_set = set(nuevo.split(","))
        errores_set = set(errores)
        destinatarios_set -= errores_set
        destinatarios_set ^= nuevo_set
        errores = []
        for i in destinatarios_set:
            if not error_usuario(i):
                errores.append(i.strip())
    if vof:
        print()
        print("Perfecto, los destinatarios quedaron de la siguiente forma:")
        print(imprimir_mensaje(", ".join(destinatarios_set), ","))
    return destinatarios_set


def dudas_etiquetas(etiquetas):
    if etiquetas == "":
        return True
    verdadero = False
    for i in "1234":
        if i in etiquetas:
            verdadero = True
    if not verdadero:
        return False
    if len(etiquetas.strip()) > 1:
        if etiquetas.count(",") == 0:
            return False
    return True



def modificar_correo(usuario, destinatarios, asunto, mensaje, etiquetas,
                     opcion):
    while opcion != "":
        print("[1] Modificar Destinatario")
        print("[2] Modificar Asunto")
        print("[3] Modificar Mensaje")
        print("[4] Modificar Etiquetas")
        print("[Enter] para enviar correo")
        opcion = input()
        while opcion not in ["1", "2", "3", "4", ""]:
            opcion = dudas_input()
        if opcion == "1":
            print("_" * 80)
            print("| Destinatarios")
            destinatarios = input("| Para: ")
            error_destinatarios(destinatarios)
            print("_" * 80)
        elif opcion == "2":
            print("_" * 80)
            print("| Asunto")
            asunto = input("| ")
            while len(asunto) > 50:
                asunto = dudas_caracteres("Asunto", 50, asunto)
            print("_" * 80)
        elif opcion == "3":
            print("_" * 80)
            print("| Mensaje")
            mensaje = input("| ")
            while len(mensaje) > 256:
                mensaje = dudas_caracteres("Mensaje", 256, mensaje)
            print("_" * 80)
        elif opcion == "4":
            print("_" * 80)
            print("| Etiquetas")
            print("| [1] Importante")
            print("| [2] Publicidad")
            print("| [3] Destacado")
            print("| [4] Newsletter")
            etiquetas = input("| ")
            while not dudas_etiquetas(etiquetas):
                etiquetas = dudas_input()
                dudas_input()
            print("_" * 80)
        else:
            continue
        print("Resumen del mensaje:")
        print("De: " + usuario)
        print("Para: " + destinatarios)
        print("Asunto: "+ asunto)
        print()
        print(imprimir_mensaje(mensaje))
        print()
        print("Etiquetas: " + obtener_etiquetas(etiquetas))
        print("_" * 80)
        print("¿Desea realizar otra modificación?")
    return destinatarios, asunto, mensaje, etiquetas


def enviar_correo(usuario, destinatarios, asunto, mensaje, etiquetas):
    archivo = open("./datos/correos_enviados.csv", "r", encoding="utf-8")
    lista_datos = archivo.readlines()
    archivo.close()
    archivo = open("./datos/correos_enviados.csv", "w", encoding="utf-8")
    datos = "".join(lista_datos) + "\n"
    datos += ",".join([usuario, destinatarios, "'" + asunto
                       + "'", encriptar(mensaje), obtener_etiquetas(
        etiquetas).replace(", ",";")])
    archivo.write(datos)
    archivo.close()
    print("¡Correo enviado con éxito!")

#archivo = open("./hola.txt","r")
#hola = archivo.readlines()
#archivo.close()
#archivo = open("./hola.txt","w")
#archivo.write("".join(hola)+"\n"+"jejejejejejejejejeje")
#archivo.close()



def plataforma_correo(usuario):
    print("_" * 80)
    print("Mensaje nuevo")
    print("_" * 80)
    print("| Destinatarios")
    destinatarios = input("| Para: ")
    destinatarios = ";".join(error_destinatarios(destinatarios))
    print("-" * 80)
    print("| Asunto")
    asunto = input("| ")
    while len(asunto) > 50:
        asunto = dudas_caracteres("Asunto", 50, asunto)
    print("-" * 80)
    print("| Mensaje")
    mensaje = input("| ")
    while len(mensaje) > 256:
        mensaje = dudas_caracteres("Mensaje", 256, mensaje)
    print("-" * 80)
    print("| Etiquetas")
    print("| [1] Importante")
    print("| [2] Publicidad")
    print("| [3] Destacado")
    print("| [4] Newsletter")
    etiquetas = input("| ")
    while not dudas_etiquetas(etiquetas):
        etiquetas = dudas_input()
    if etiquetas == "":
        etiquetas = "0"
    print("_" * 80)
    print("Resumen del mensaje:")
    print("De: " + usuario)
    print("Para: " + destinatarios)
    print("Asunto: "+ asunto)
    print()
    print(imprimir_mensaje(mensaje))
    print()
    print("Etiquetas: "+obtener_etiquetas(etiquetas))
    print("_"*80)
    print("¿Desea realizar algún cambio?")
    opcion = "0"
    destinatarios, asunto, mensaje, etiquetas = modificar_correo(
        usuario, destinatarios, asunto, mensaje, etiquetas, opcion)
    enviar_correo(usuario, destinatarios, asunto, mensaje, etiquetas)
