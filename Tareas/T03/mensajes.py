from funciones import range_, input_lista, entrada
from estructuras_de_datos import Tupla

def mensaje(tipo="-", opcional=""):
    grupos = Tupla("Central Generadora", "Estación de Elevación",
                   "Subestación de Transmisión", "Subestación de "
                                                 "Distribución", "Casa")

    if tipo == "modificar_arista":
        print("_" * 80)
        print("AGREGAR O ELIMINAR CONEXIÓN")
        print("-" * 80)
        print("A continuación, puede ingresar lo conexión a agregar/eliminar")
        print("La forma para ingresarlo es:")
        print("Xi * Yj")
        print("Donde:\n"
              "* <X> corresponde al tipo de conexión del nodo de donde "
              "comienza la conexión")
        print("* <Y> es el tipo de conexión del nodo de destino")
        print("* <i> es la id del nodo X")
        print("* <j> es la id del nodo Y")
        print("* <*> corresponde a la acción a realizar")
        print("-" * 80)
        print("Tipos de conexión y acciones:")
        print("G: Central Generadora, E: Estación de Elevación")
        print("T: Subestación de Transmisión, D: Subestación de Distribución")
        print("C: Casas, +: Agragar Conexión, -: Quitar Conexión")
        print("-" * 80)
        print("Ejemplos:")
        print("G0 - E2 ---> Quita conexión entre la Central(0) y la "
              "EstaciónElevadora(2)")
        print("T2 + D3 ---> Agrega una conexión entre el Transmisor(2) y la "
              "Distribuidora(3)")
        print("-" * 80)

    elif tipo == "modificar_aristas_clasico":
        print("_" * 80)
        print("AGREGAR O ELIMINAR CONEXIÓN (CLÁSICO)")
        print("-" * 80)
        mensaje("listado")
        print("-" * 80)
        print("A continuación puede ingresar el [número] correspondiente al "
              "tipo de nodo :D")

    elif tipo == "consultas":
        print("_" * 80)
        print("CONSULTAS")
        print("-" * 80)
        print("A continuación puede ingresar el [número] de la consulta :D")
        return input_lista(Tupla("Energía total consumida en una comuna",
                              "Cliente "
                        "con mayor consumo energético", "Cliente con menor "
                        "consumo energético", "Potencia perdida en "
                        "transmisión", "Consumo de una subestación"), ">>> ")

    elif tipo == "consumo_total":
        print("-" * 80)
        print("Ahora puede ingresar el [numero] de la comuna :D")

    elif tipo == "mayor_menor_consumo":
        print("-" * 80)
        print("Ahora puede ingresar la sigla del sistema eléctrico a "
              "consultar :D")

    elif tipo == "perdida_potencia":
        print("-" * 80)
        print("Ahora puede ingresar la id de la casa a consultar :D")

    elif tipo == "consumo_subestacion":
        print("-" * 80)
        print("¿Qué tipo de subestación desea consultar?")
        num = input_lista(Tupla("Subestación de Transmisión", "Subestación de "
                                                        "Distribución"))
        if int(num) == 0:
            nodo = "T"
        elif int(num) == 1:
            nodo = "D"
        print("Ahora puede ingresar la id de la subestación a consultar :D")
        id_ = entrada(">>> id:")
        return Tupla(nodo, id_)

    elif tipo == "error_entrada":
        print("(Error) ErrorEntrada", opcional)
        print("Lo sentimos :O Estamos teniendo problemas para "
              "entender lo ingresado")
        print("Por favor, inténtelo de nuevo :D")

    elif tipo in Tupla("agregar_nodo", "remover_nodo"):
        print("_" * 80)
        if tipo == "agregar_nodo":
            print("AGREGAR NODO")
        elif tipo == "remover_nodo":
            print("REMOVER NODO")
        print("-" * 80)
        mensaje("listado")
        print("-" * 80)
        print("A continuación puede ingresar el [número] correspondiente al "
              "tipo de nodo :D")

    elif tipo == "error":
        print("Estamos teniendo problemas para entender el input")
        print("Por favor, inténtelo de nuevo :D")

    elif tipo == "excepcion":
        print(f"(Error) {opcional[0]}: {opcional[1]}")
        print("¡Lo sentimos! Puedes intentarlo de nuevo :D ")

    elif tipo == "listado":
        for n in range_(len(grupos)):
            print(f"[{n}] {grupos[n]}")

    elif tipo == "menu":
        print("_" * 80)
        print("Bienvenid@ a Electromatic :D")
        print("_" * 80)
        print("A continuación se muestran las opciones disponibles:")

