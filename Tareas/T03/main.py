from excepciones import VolverMenu, Volver
from graph import SistemaElectrico
from estructuras_de_datos import Tupla
from funciones import input_lista
from mensajes import mensaje
from clases import Generadora, Casa

#### MODIFICABLES ####

tipo_datos = "small"
ruta = f"bd/{tipo_datos}"

######################


if __name__ == '__main__':
    grafo = SistemaElectrico()
    grafo.cargar_datos(ruta)
    grafo.cargar_conexiones(ruta)
    grafo.calcular_demanda()
    grafo.simular_flujo()


    while True:
        try:
            mensaje("menu")
            opciones = Tupla("Generar Consulta",
                             "Agregar Nodo",
                             "Remover Nodo",
                             "Añadir o Quitar Conexiones (Classic)",
                             "Añadir o Quitar Conexiones (Modo Hackermen)")
            respuesta = int(input_lista(opciones, ">>> "))
            if respuesta == 0:
                grafo.consulta()
            elif respuesta == 1:
                grafo.agregar_nodo()
            elif respuesta == 2:
                grafo.remover_nodo()
            elif respuesta == 3:
                grafo.modificar_aristas_clasico()
            elif respuesta == 4:
                grafo.modificar_aristas()

        except Volver:
            pass

        except VolverMenu:
            print("Volviendo al Menú :D")