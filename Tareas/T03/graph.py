import csv
from excepciones import InvalidQuery, ErrorEntrada, ForbiddenAction, \
    ElectricalOverload, Volver, VolverMenu
from clases import Casa, Estacion, Generadora, Nodo, resistividad
from funciones import indice, proporciones, range_, descifrar_input_conexion,\
    entrada, print_lista, input_lista
from estructuras_de_datos import Tupla, Lista, Texto, Conjunto, Cola, \
    Listado, Diccionario, DiccionarioPorDefecto
from mensajes import mensaje


class SistemaElectrico:
    def __init__(self):
        self.casas = Diccionario()
        self.generadoras = Diccionario()
        self.distribucion = Diccionario()
        self.elevadoras = Diccionario()
        self.transmision = Diccionario()
        self.diccionario = Diccionario(Tupla(Tupla("C", self.casas), Tupla("G",
                        self.generadoras), Tupla("D", self.distribucion),
                        Tupla("E", self.elevadoras), Tupla("T",
                        self.transmision)))
        self.siguiente = Diccionario(Tupla(Tupla("C", "C"), Tupla("G", "E"),
                            Tupla("D", "C"), Tupla("E", "T"), Tupla("T", "D")))
        self.lugares = DiccionarioPorDefecto(Conjunto)
        self.comunas = Conjunto()
        self.sistemas = DiccionarioPorDefecto(Conjunto)
        self.tipos_centrales = Tupla("Solar", "Termoelectrica", "Biomasa")
        self.nombres = Tupla("Central Generadora", "Estación Elevadora",
                             "Subestación de Transmisión", "Subestación de "
                                "Distribución", "Casa")

    def cargar_datos(self, ruta, todo=True, casas=False, centrales=False,
                     distribucion=False, elevadoras=False, transmision=False):
        if todo:
            casas, centrales, distribucion, elevadoras, transmision = True, \
                                            True,  True, True, True
        if casas:
            with open(f"{ruta}/casas.csv", newline="") as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    nodo = Casa(fila)
                    self.lugares[nodo.provincia].add(nodo.comuna)
                    self.sistemas[nodo.sistema].add(nodo.provincia)
                    self.comunas.add(nodo.comuna)
                    self.casas[nodo.id] = nodo

        if centrales:
            with open(f"{ruta}/centrales.csv", newline="") as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    nodo = Generadora(fila)
                    self.lugares[nodo.provincia].add(nodo.comuna)
                    self.comunas.add(nodo.comuna)
                    self.sistemas[nodo.sistema].add(nodo.provincia)
                    self.generadoras[nodo.id] = nodo

        if distribucion:
            with open(f"{ruta}/distribucion.csv", newline="") as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    nodo = Estacion(fila, "D")
                    self.lugares[nodo.provincia].add(nodo.comuna)
                    self.comunas.add(nodo.comuna)
                    self.sistemas[nodo.sistema].add(nodo.provincia)
                    self.distribucion[nodo.id] = nodo

        if elevadoras:
            with open(f"{ruta}/elevadoras.csv", newline="") as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    nodo = Estacion(fila, "E")
                    self.lugares[nodo.provincia].add(nodo.comuna)
                    self.comunas.add(nodo.comuna)
                    self.sistemas[nodo.sistema].add(nodo.provincia)
                    self.elevadoras[nodo.id] = nodo

        if transmision:
            with open(f"{ruta}/transmision.csv", newline="") as archivo:
                reader = csv.DictReader(archivo)
                for fila in reader:
                    nodo = Estacion(fila, "T")
                    self.lugares[nodo.provincia].add(nodo.comuna)
                    self.comunas.add(nodo.comuna)
                    self.sistemas[nodo.sistema].add(nodo.provincia)
                    self.transmision[nodo.id] = nodo

    def conectar(self, diccionario_d, diccionario_h, datos, desde_hasta = True):
        lista = Lista()
        for i in datos.items():
            lista.agregar(i[1])
        desde, hasta, longitud = lista
        if not desde_hasta:
            desde, hasta = hasta, desde
        diccionario_d[desde].children.agregar(Tupla(diccionario_h[hasta],
                                                    longitud))
        diccionario_h[hasta].parent.agregar(Tupla(diccionario_d[desde],
                                                  longitud))

    def cargar_conexiones(self, ruta):
        with open(f"{ruta}/casas_casas.csv", newline="") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                self.conectar(self.casas, self.casas, fila, True)
        with open(f"{ruta}/casas_distribucion.csv", newline="") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                self.conectar(self.distribucion, self.casas, fila, False)
        with open(f"{ruta}/distribucion_transmision.csv", newline="") as \
                archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                self.conectar(self.transmision, self.distribucion, fila, False)
        with open(f"{ruta}/transmision_elevadoras.csv", newline="") as \
                archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                self.conectar(self.elevadoras, self.transmision, fila, False)
        with open(f"{ruta}/centrales_elevadoras.csv", newline="") as \
                archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                self.conectar(self.generadoras, self.elevadoras, fila, True)

    def calcular_demanda(self):
        for nodo in self.generadoras.valores():
            nodo.calcular_demanda()

        for grupo in Tupla(self.generadoras, self.elevadoras,
                           self.transmision, self.distribucion, self.casas):
            for nodo in grupo.valores():
                nodo.demanda_calculada = False

    def flujo(self, primero=Nodo("G"), funcion=str):
        ### El método BFS fue extraído de los contenidos del curso :D
        try:
            visited = Conjunto()
            if primero.tipo == "G":
                for i in self.elevadoras.valores():
                    primero.children.agregar(Tupla(i, 0))
            queue = Cola(primero)

            while queue:
                nodo = queue.popleft()
                vertex = nodo.valor
                if vertex not in visited:
                    if vertex.nodo != "G":
                        visited.add(vertex)
                        if vertex.nodo == "E":
                            vertex.potencia_previa = vertex.potencia
                            vertex.potencia = float(vertex.potencia_elevadora)
                        else:
                            vertex.consumo_previo = vertex.consumo
                            vertex.consumo = min(float(vertex.consumo_datos),
                                                float(vertex.potencia))

                        vertex.potencia_restante_previa = \
                            vertex.potencia_restante
                        vertex.potencia_restante = float(vertex.potencia) - \
                                                   float(vertex.consumo)
                        valores_mij = Tupla()
                        for child in vertex.children.descomprimir(0):
                                valores_mij.agregar(float(child.mij))

                        potencias_entregar = proporciones(valores_mij, \
                                                    vertex.potencia_restante)

                        for num in range_(len(potencias_entregar)):
                            valor_mij = potencias_entregar[num]
                            nodo_num = vertex.children.descomprimir(0)[num]

                            nodo_num.potencia_previa = nodo_num.potencia
                            nodo_num.potencia = \
                                max(min(valor_mij - (valor_mij * resistividad *
                                        float(
                                        vertex.children.descomprimir(1)[num]) /
                                    nodo_num.seccion_transversal),
                                        float(nodo_num.demanda)), 0)
                            if float(nodo_num.potencia) > 30000 and \
                                    nodo_num.nodo == "C":
                                print(repr(nodo_num))
                                raise ElectricalOverload(nodo_num,
                                                         funcion)

                            nodo_num.mij_previo, nodo_num.mij_0_previo = \
                                nodo_num.mij, nodo_num.mij_0
                            nodo_num.mij, nodo_num.mij_0 = valor_mij, \
                                                           nodo_num.mij

                    for n in vertex.children:
                        v = n[0]
                        if v not in visited:
                            queue.append(v)
        except ElectricalOverload as error:
            for grupo in Tupla(self.elevadoras,
                               self.transmision, self.distribucion, self.casas):
                for nodo in grupo.valores():
                    nodo.volver_paso()
            raise error
        return visited

    def simular_flujo(self, funcion=str):
        for elevadora in self.elevadoras.valores():
            elevadora.potencia = float(elevadora.potencia_elevadora)
            if elevadora.potencia < elevadora.demanda:
                self.flujo(elevadora, funcion)

    def agregar_conexion(self, desde, hasta, largo, confirmado=False):
        if not confirmado:
            # Corresponden los tipos:
            if self.siguiente[desde.nodo] != hasta.nodo:
                raise ForbiddenAction(desde, hasta, self.agregar_conexion,
                                      "tipo")
            # Si hasta es casa, verificar que desde es de la misma comuna:
            elif hasta.nodo == "C" and desde.comuna != hasta.comuna:
                raise ForbiddenAction(desde, hasta, self.agregar_conexion,
                                      "comuna")
            # Si hasta es estacion elevadora, verificar que generadora no
                # tenga una previamente
            elif hasta.nodo == "E" and len(desde.children) > 0:
                raise ForbiddenAction(desde, hasta, self.agregar_conexion, "GE")

            # Verificar relaciones 1 a n
            elif desde.nodo in Tupla("E", "T") and len(hasta.parent) > 0:
                raise ForbiddenAction(desde, hasta, self.agregar_conexion,
                                      f"{desde.nodo}{hasta.nodo}")

            elif desde in hasta.children.descomprimir(0) or hasta in \
                    desde.parent.descomprimir(0):
                raise ForbiddenAction(desde, hasta, self.agregar_conexion,
                                      "ciclo")
            elif hasta in desde.children.descomprimir(0):
                raise ForbiddenAction(desde, hasta, self.agregar_conexion,
                                      "yasellama")

        desde.children.agregar(Tupla(hasta, largo))
        hasta.parent.agregar(Tupla(desde, largo))
        try:
            self.simular_flujo(self.agregar_conexion)
        except ElectricalOverload as error:
            mensaje("excepcion", Tupla("ElectricalOverload", error))
            desde.children.remove(hasta, lambda i: i[0])
            hasta.parent.remove(desde, lambda i: i[0])






    def remover_conexion(self, desde, hasta, confirmado=False):
        if not confirmado:
            if self.siguiente[desde.nodo] != hasta.nodo:
                raise ForbiddenAction(desde, hasta, self.remover_conexion,
                                      "tipo")
            elif hasta not in desde.children.descomprimir(0):
                raise ForbiddenAction(desde, hasta, self.remover_conexion,
                                      "nosellama")

        desde.children.remove(hasta, lambda i: i[0])
        hasta.parent.remove(desde, lambda i: i[0])

        try:
            self.simular_flujo(self.remover_conexion)
        except ElectricalOverload as error:
            mensaje("excepcion", Tupla("ElectricalOverload", error))
            desde.children.agregar(Tupla(hasta, largo))
            hasta.parent.agregar(Tupla(desde, largo))

    def modificar_aristas_clasico(self):
        try:
            mensaje("modificar_aristas_clasico")
            numero_tipo = entrada(">>> ")
            while numero_tipo.strip() not in Tupla("0", "1", "2", "3", "4"):
                mensaje("error")
                numero_tipo = entrada(">>> ")
            print("-" * 80)
            grupos = Tupla(self.generadoras, self.elevadoras, self.transmision,
                           self.distribucion, self.casas, self.casas)
            grupo = grupos[int(numero_tipo)]
            numero_nodo = input_lista(grupo.valores(), f">>> "
                                    f"{self.nombres[int(numero_tipo)]}: ")
            nodo_ = grupo.valores()[numero_nodo]
            print("-" * 80)
            print("¿Qué acción desea realizar?")
            numero_accion = int(input_lista(Tupla("Añadir Conexión", "Quitar "
                                    "Conexión"), ">>> "))
            if int(numero_tipo) == 0:
                numero_respuesta = 0
            else:
                numero_respuesta = int(input_lista(Tupla("Este nodo es quien "
                        "inicia la conexión", "Este nodo es el receptor"),
                                                   ">>> "))
            print("-" * 80)
            print("Ahora puede elegir el otro nodo :D")
            if numero_accion == 0:
                if numero_respuesta == 0:
                    numero_child = input_lista(grupos[int(numero_tipo) +
                                                1].valores(), ">>> ")
                    desde = nodo_
                    hasta = desde.children.descomprimir(0)[numero_child]

                elif numero_respuesta == 1:
                    numero_parent = input_lista(grupos[int(numero_tipo) -
                                                1].valores(), ">>> ")
                    hasta = nodo_
                    desde = hasta.parent.descomprimir(0)[numero_parent]

                print("Ahora, puedes ingresar la distancia que hay entre los "
                      "nodos :D")
                distancia = entrada(">>> Distancia: ")
                while not distancia.replace('.', '', 1).isnumeric():
                    print("Estamos teniendo problemas para leer el "
                          "input")
                    print("Por favor, inténtelo de nuevo :D")
                    distancia = entrada(">>> Distancia: ")
                try:
                    self.agregar_conexion(desde, hasta, distancia)
                except ForbiddenAction as error:
                    mensaje("excepcion", Tupla("ForbiddenAction", error))
                    raise Volver()


            elif numero_accion == 1:
                if numero_respuesta == 0:
                    numero_child = input_lista(nodo_.children.descomprimir(0),
                                               ">>> ")
                    desde = nodo_
                    hasta = desde.children.descomprimir(0)[numero_child]

                elif numero_respuesta == 1:
                    numero_parent = input_lista(nodo_.parent.descomprimir(0),
                                                ">>> ")
                    hasta = nodo_
                    desde = hasta.parent.descomprimir(0)[numero_parent]
                try:
                    self.remover_conexion(desde, hasta, confirmado=True)
                except ForbiddenAction as error:
                    mensaje("excepcion", Tupla("ForbbidenAction", error))
                    raise Volver()

        except Volver:
            self.modificar_aristas_clasico()

    def modificar_aristas(self):
        try:
            mensaje("modificar_arista")
            ingreso = entrada(">>> ")
            while ingreso != "":
                try:
                    descifrado = descifrar_input_conexion(ingreso)
                except ErrorEntrada as error:
                    mensaje("error_entrada", error)
                else:
                    try:
                        desde = self.diccionario[descifrado[1][0]][
                            descifrado[1][1]]
                        hasta = self.diccionario[descifrado[2][0]][
                            descifrado[2][1]]

                    except InvalidQuery as error:
                        mensaje("excepcion", Tupla("InvalidQuery", error))
                        raise Volver()

                    else:
                        if descifrado[0] == "+":
                            print("A continuación puede ingresar la distancia "
                                  "que separa a estos nodos")
                            distancia = entrada(">>> Distancia: ")
                            while not distancia.replace('.', '', 1).isnumeric():
                                print("Estamos teniendo problemas para leer el "
                                      "input")
                                print("Por favor, inténtelo de nuevo :D")
                                distancia = entrada(">>> Distancia: ")
                            try:
                                self.agregar_conexion(desde, hasta, distancia)
                            except ForbiddenAction as error:
                                print("Error:", error)
                                print("Puede intentarlo nuevamente :D")
                        elif descifrado[0] == "-":
                            try:
                                self.remover_conexion(desde, hasta)

                            except ForbiddenAction as error:
                                mensaje("excepcion",
                                        Tupla("ForbiddenAction", error))
                finally:
                    ingreso = entrada(">>> ")

        except Volver:
            self.modificar_aristas()

    def agregar_nodo(self):
        try:
            mensaje("agregar_nodo")
            numero_tipo = entrada(">>> ")
            while numero_tipo.strip() not in Tupla("0", "1", "2", "3", "4"):
                mensaje("error")
                numero_tipo = entrada(">>> ")
            print("-" * 80)
            presentacion = "A continuación puede ingresar los datos de la {} " \
                           "nueva.\nEn algunos campos se tiene la " \
                           "posibilidad de presionar [ENTER] para " \
                           "ingresar un valor al azar."

            titulos = self.nombres
            grupos = Tupla(self.generadoras, self.elevadoras, self.transmision,
                           self.distribucion, self.casas)
            grupo = grupos[int(numero_tipo)]

            tipo_estacion = "GETDC"[int(numero_tipo)]

            print(presentacion.format(f"{titulos[int(numero_tipo)]}"))

            # 0. ID
            print("-" * 80)

            id_ = entrada(">>> id: ")
            while grupo.existe(id_):
                if id_ == "":
                    id_ = grupo.llave_random()
                else:
                    print("Esta id ya existe, por favor elige otra :D")
                    id_ = entrada(">>> id: ")

            if id_ == "":
                id_ = grupo.llave_random()
            print(f"id seleccionada: {id_}")
            print("-" * 80)

            if int(numero_tipo) != 4:
                # 1. Nombre
                nombre_ = entrada(">>> Nombre: ")
                print("-" * 80)
                print(f"nombre seleccionada: {nombre_}")

            # 2. Sistema
            numero_sistema = input_lista(self.sistemas.llaves(),
                                         ">>> Sistema Eléctrico: ")
            sistema_ = self.sistemas.llaves()[numero_sistema]

            print(f"sistema electrico seleccionada: {sistema_}")
            print("-" * 80)

            # 3. Provincia
            numero_provincia = input_lista(self.sistemas[sistema_],
                                           ">>> Provincia: ", True)
            if numero_provincia == "*":
                provincia_ = entrada(">>> Provincia (nombre): ").upper()
            else:
                provincia_ = self.sistemas[sistema_][numero_provincia]

            print(f"provincia seleccionada: {provincia_}")
            print("-" * 80)

            # 4. Comuna
            numero_comuna = input_lista(self.lugares[provincia_],
                                        ">>> Comuna: ", True)
            if numero_comuna == "*":
                comuna_ = entrada(">>> Comuna (nombre): ").upper()
            else:
                comuna_ = self.lugares[provincia_][numero_comuna]

            print(f"comuna seleccionada: {comuna_}")
            print("-" * 80)

            if int(numero_tipo) == 0:
                # 5. Tipo
                numero_tipo = input_lista(self.tipos_centrales, ">>> Tipo: ")
                tipo_ = self.tipos_centrales[numero_tipo]
                print(f"tipo seleccionado: {tipo_}")
                print("-" * 80)

                # 6. Potencia
                potencia_ = entrada(">>> Potencia (MW): ")
                while not potencia_.replace('.', '', 1).isnumeric():
                    print("No pudimos entender tu input :O "
                          "inténtelo de nuevo por favor :D")
                    potencia_ = entrada(">>> Potencia (MW): ")

                central_ = Generadora(Tupla(id_, nombre_, sistema_,
                                            provincia_, comuna_, tipo_,
                                            potencia_),
                                      inicio=False)
                self.generadoras[central_.id] = central_
                self.lugares[provincia_].add(comuna_)
                self.comunas.add(comuna_)

            elif int(numero_tipo) in Tupla(1, 2, 3):
                # 6. Consumo
                consumo_ = entrada(">>> Consumo (MW): ")
                while not consumo_.replace('.', '', 1).isnumeric():
                    print("No pudimos entender tu input :O "
                          "inténtelo de nuevo por favor :D")
                    consumo_ = entrada(">>> Consumo (MW): ")

                estacion_ = Estacion(Tupla(id_, nombre_, sistema_,
                                provincia_, comuna_, consumo_),
                                      inicio=False, tipo=tipo_estacion)
                grupo[estacion_.id] = estacion_
                self.lugares[provincia_].add(comuna_)
                self.comunas.add(comuna_)

            elif int(numero_tipo) == 4:
                # 6. Consumo
                consumo_ = entrada(">>> Consumo (kW): ")
                while not consumo_.replace('.', '', 1).isnumeric():
                    print("No pudimos entender tu input :O "
                          "inténtelo de nuevo por favor :D")
                    consumo_ = entrada(">>> Consumo (kW): ")

                casa_ = Casa(Tupla(id_, sistema_, provincia_, comuna_,
                                      consumo_), inicio=False)
                self.casas[casa_.id] = casa_
                self.lugares[provincia_].add(comuna_)
                self.comunas.add(comuna_)

        except Volver:
            self.agregar_nodo()

    def remover_nodo(self):
        try:
            mensaje("remover_nodo")
            numero_tipo = entrada(">>> ")
            while numero_tipo.strip() not in Tupla("0", "1", "2", "3", "4"):
                mensaje("error")
                numero_tipo = entrada(">>> ")
            print("-" * 80)
            grupos = Tupla(self.generadoras, self.elevadoras, self.transmision,
                          self.distribucion, self.casas)
            grupo = grupos[int(numero_tipo)]
            numero_nodo = input_lista(grupo.valores(), f">>> "
                                        f"{self.nombres[int(numero_tipo)]}: ")
            nodo_ = grupo.valores()[numero_nodo]
            borrado = grupo.pop(nodo_.id).valor
            print(f"Se quitó el nodo: {borrado}")

        except Volver:
            self.remover_nodo()

    def consumo_total(self, comuna):
        comuna = str(comuna).strip().upper()
        if comuna not in self.comunas:
            raise InvalidQuery(comuna, "comuna")
        consumo_casas = float()
        consumo_total = float()
        for casa in self.casas.valores():
            if casa.comuna == comuna:
                consumo_casas += float(casa.consumo)
            consumo_total += float(casa.consumo)


        for grupo in Tupla(self.elevadoras, self.transmision,
                           self.distribucion):
            for nodo in grupo.valores():
                if nodo.comuna == comuna:
                    consumo_total += float(nodo.consumo)
        if consumo_total == 0:
            porcentaje = 100
        else:
            porcentaje = (consumo_casas / consumo_total) * 100
        return Tupla(consumo_casas, porcentaje)

    def mayor_menor_consumo(self, sistema, tipo=0):
        sistema = str(sistema).strip().upper()
        if sistema not in self.sistemas.llaves():
            raise InvalidQuery(sistema, "sistema")
        grupo = Tupla()
        for casa in self.casas.valores():
            if casa.sistema == sistema:
                grupo.agregar(casa)
        if int(tipo) == 1:
            nodo = max(grupo, key=lambda i: float(i.consumo))
            accion = "mayor"
        elif int(tipo) == 2:
            accion = "menor"
            nodo = min(grupo, key=lambda i: float(i.consumo))

        return Tupla(nodo.id, nodo.provincia, nodo.comuna)

    def potencia_perdida(self, id_):
        casa = self.casas[id_]
        nodo_actual = casa
        visitados = Conjunto()
        cola = Cola(casa)
        total = float()
        while cola and nodo_actual.nodo != "E":
            nodo_actual = cola.popleft().valor
            if nodo_actual not in visitados and nodo_actual.nodo != "E":
                visitados.add(nodo_actual)
                for n in nodo_actual.parent:
                    v = n[0]
                    largo = float(n[1])
                    rij = resistividad * (largo / float(
                        nodo_actual.seccion_transversal))
                    mij = float(nodo_actual.mij)
                    total += (rij * mij)
                    if v not in visitados:
                        cola.append(v)
        return total

    def consumo_subestacion(self, id_, tipo):
        grupo = self.diccionario[tipo]
        nodo = grupo[id_]
        return nodo.calcular_demanda()

    def consulta(self):
        try:
            opcion = mensaje("consultas")
            if int(opcion) == 0:
                mensaje("consumo_total")
                respuesta = input_lista(self.comunas, otro=True)
                if respuesta == "*":
                    comuna = entrada(">>> Comuna: ").strip().upper()
                else:
                    comuna = self.comunas[respuesta]
                consumo, porcentaje = self.consumo_total(comuna)
                print(f"La comuna {comuna} tiene un consumo de "
                          f"{consumo} kW (un {round(porcentaje, 2)}% del "
                      f"total)")
            elif int(opcion) in Tupla(1, 2):
                mensaje("mayor_menor_consumo")
                sigla = entrada(">>> Sigla: ")
                id_, provincia, comuna = self.mayor_menor_consumo(
                        sigla, opcion)
                print(f"Los datos de la casa indicada son:")
                print(f"Casa: id = {id_}, Provincia = {provincia}, Comuna ="
                          f" {comuna}")
            elif int(opcion) == 3:
                mensaje("perdida_potencia")
                id_ = entrada(">>> id: ")
                resultado = self.potencia_perdida(id_)
                print(f"La potencia de perdida en la transmisión es de "
                          f"{resultado} kW.")
            elif int(opcion) == 4:
                tipo, id_ = mensaje("consumo_subestacion")
                respuesta = self.consumo_subestacion(id_, tipo)
                print(f"El consumo total de esta subestación es de "
                          f"{respuesta} kW.")
        except InvalidQuery as error:
            mensaje("excepcion", Tupla("InvalidQuery", error))
            self.consulta()
        except Volver:
            self.consulta()