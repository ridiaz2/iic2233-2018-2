from functions import *



if __name__ == '__main__':
    print("_" * 80)
    print("Bienvenid@ a DCCAirlines")
    try:
        while True:
            print("_" * 80)
            print("Menú principal")
            print("-" * 80)
            print("¿Qué acción desea realizar?")
            foreach(lambda i: print(f"[{i[0]}] {i[1]}"), enumerate([
                "Abrir archivo de consultas", "Ingresar consulta",
                "Abrir historial", "Configurables"]))
            entrada = revisar_input(input(), (lambda i: True if i in
                    list("0123") else False))
            if entrada == "0":
                print("_" * 80)
                print(
                    "A continuación puede ingresar la dirección de consultas:")
                archivo_ruta = revisar_input(input("Ruta del archivo: "),
                                             (lambda i: True
                                             if i == "" or os.path.exists(i)
                                            else False), "Ruta del archivo: ")
                if archivo_ruta == "":
                    archivo_ruta = "queries.txt"
                entrada = list(obtener_inputs(archivo_ruta))
                entradas_mostrar = enumerate(entrada)
                foreach(lambda i: print(f"{formato_corchetes(i[0], 4)} {i[1]}"),
                        entradas_mostrar)
                print("-" * 80)
                print(
                "A continuación puede seleccionar las consultas a visualizar")
                print(
                    "En el formato: consulta1, consulta2, consulta3,"
                    "... (indicando el numero respectivo)")
                print("[Enter] para volver :D")
                consultas = revisar_input(input(),
                                          lambda i: True if es_lista_de_numeros(
                                              i, len(entrada)) else False)
                lista_consultas = map(int, consultas.split(","))
                foreach(lambda i: imprimir_output(interpretar_input(entrada[i]),
                                                  f"Consulta {i}: "
                                                  f"{entrada[i]}"),
                        lista_consultas)
            elif entrada == "1":
                ruta = "./output.txt"
                print("A continuación puede ingresar una consulta")
                consulta = input("Consulta: ")
                if consulta == "":
                    pass
                else:
                    guardar_consulta(parse(consulta))
            elif entrada == "2":
                ruta = "./output.txt"
                datos = leer_output_txt(ruta)
                lista_datos = [imprimir_y_guardar(i, [], True) for i in datos]
                print("¿Desea eliminar parte del historial?")
                foreach(lambda i: print(f"[{i[0]}] {i[1]}"),
                        enumerate(["Borrar todo",
                                   "Borrar lista de datos",
                                   "o [Enter] Continuar"]))
                respuesta = revisar_input(input(),
                                          lambda i: True if i in ["0", "1", "2",
                                                                ""] else False)
                if respuesta == "0":
                    print("¿Está seguro que desea vaciar todo el historial?")
                    foreach(lambda i: print(f"[{i[0]}] {i[1]}"),
                            enumerate(["Borrar todo",
                                       "No borrar"]))
                    si_no = revisar_input(input(),
                                          lambda i: True if i in ["0", "1",
                                                                 ""] else False)
                    if si_no == "0":
                        reiniciar_output_txt(ruta)
                    elif si_no in ["1", ""]:
                        print("Los datos no fueron borrados (:")
                elif respuesta == "1":
                    print("A continuación, puede ingresar una lista"
                          "de datos a borrar")
                    print("De la forma numero_consulta1, numero_consulta2, ...")
                    print("[Enter] para volver al Menú")
                    consultas = revisar_input(input(),
                                lambda i: True if es_lista_de_numeros(
                                i, len(lista_datos)) else False)
                    lista_consultas = map(int, consultas.split(","))
                    foreach(lambda i: lista_datos.pop(i - 1), lista_consultas)
                    reiniciar_output_txt(ruta)
                    with open(ruta, encoding="UTF-8", mode="a") as archivo:
                        num = count(start=0)
                        foreach(lambda i: escribir_en_archivo(archivo, i,
                                                              next(num)),
                                lista_datos)



            # rellenar esta parte con el llamado a sus funciones
            # sigue corriendo el uso restringido en toda situacion
            # de los for/while/etc dentro de este main a excepcion
            # del que se encuentra arriba, por lo que no se puede
            # agregar ninguno mas

    # no es necesario que hagan una parte para salir del menu
    except KeyboardInterrupt():
        exit()
