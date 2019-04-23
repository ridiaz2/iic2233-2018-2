# Tarea 3: Electromati(DC)C :school_satchel:


A continuación, se presentan algunas consideraciones y datos de la _unica_ y _fabulosa_ Tarea 3 de Programación Avanzada, que presenta una simulación de red eléctrica utilizando grafos.

## Consideraciones generales :octocat:

* En un principio, la tarea la estaba realizando de una manera diferente a la del producto final, es por esto que existen funciones o clases que no son utilizadas :D.
* Para revisar si la potencia es la necesaria para cubrir la demanda, se revisan las estaciones elevadoras a partir de la energía que le entregan las generadoras.
* El consumo de una estación elevadora es dado equitativamente a cada generadora.
* En `main.py` existen modificables para cambiar la base de datos a utilizar :D (*tipo_datos* y *ruta*). En el caso de `clases.py`, la variable *resitividad* también es modificable.
* En la clase `Diccionario`, es utilizada *getitem* y *setitem*, lo que tengo entendido es legal :O, ya que no utiliza elementos de la clase `dict`, en este caso :D.
* No entendí muy bien la parte del enunciado sobre crear el archivo en `testing`. Entendí que es una especie de item opcional, sin embargo, intenté hacer lo que creí que se debería. De esta forma, al correr el test, se crea un archivo con los casos de testeo, y la respuesta ideal :D (sé que en estos casos hay que abrir una *issue*, pero ya era un poco tarde para preguntar, mi error D:)
* Por enunciado, la parte de `setUp` y `tearDown` parecían ser opcionales, de todas formas estas son utilizadas (además, se aprovechan en la creación del archivo).


### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 1 (Estructuras de datos): Hecha completa (```estructuras_de_datos.py```)
   * ```Vertice``` (11) (Corresponde al elemento básico de la mayoría de las estructuras de datos utilizadas, representa un nodo, con un valor, una referencia al siguiente vértice, y una llave, en caso de corresponder a un elemento de diccionario).
   * ```Lista``` (28) (Esta clase es muy similar a las listas predeterminadas de python, utiliza gran parte de los algoritmos utilizados en los contenidos de [Listas Ligadas](https://github.com/IIC2233/contenidos/blob/master/semana-06/1-listas-ligadas.ipynb))
   * ```Diccionario``` (152) (Muy similar a la estructura `dict` que viene con python, hereda de `Lista`). 
   * ```DiccionarioPorDefecto``` (255) (Representa un `defaultdict`, hereda de `Diccionario`)
   * ```Tupla``` (269) (Representa a `tuple`, muy similar a `Lista` -de hecho, hereda de ella :D-, pero intenta ser una versión más simplificada, y permite agregar una cantidad de argumentos indefinidos en la inicialización de esta (lo que me fue muy útil para escribir `for`'s por ejemplo).
   * ```Texto``` (292) (Antes de que decidiera utilizar Listas Ligadas para la tarea, intenté utilizar una estructura de datos que funcionara a partir de `strings`. Básicamente tiene un string que lo representa, y que es recorrido como una lista, teniendo la opción de agregar elementos).
   * ```Conjunto``` (361) (Representa un `set`. Es utilizado como una tupla sin repetir elementos :D)
   * ```Cola``` (397) (Reperesenta un `deque`. Hereda de `Lista`, pero agrega las funciones `pop` y `popleft`).
   * ```Listado``` (438) (Correspondía a la estructura que relacionaba los strings de `Texto`, con los elementos de la red eléctrica. Este fue borrado tras la creación de lista, sin embargo, se dejó en caso de que en algún módulo fuera utilizado).
   
* Parte 2 (Modulación): Hecha completa (```clases.py```)
   * ```Nodo``` (19) (Estructura básica de las entidades de la red. Contiene las funciones utilizadas, para luego ser heredadas).
   * ```Generadora``` (121) (Representa una *Estación Generadora*)
   * ```Estacion``` (171) (Representa a una *Estación elevadora*, *Subestación de Transmisión* y *Subestación de Distribución*
   * ```Casa``` (241) (Representa a las *Entidades de Consumo*)
   
* Parte 3 (Red Eléctrica): Hecha casi completa (```graph.py```)
   * `Agregar arista` (208) ---> `SistemaElectrico.agregar_conexion(desde, hasta, largo)`. (Agrega una conexión entre dos nodos si es que es permitida)
   * `Remover arista` (250) ---> `SistemaElectrico.remover_conexion(desde, hasta, largo)`. (Quita una conexión si es que es posible (o existe)).
   * `Nota`: Ambas funciones modifican la red de manera real (a menos que de un error `ElectricalOverload`). Pido disculpas por esto, de hecho, cada nodo tiene una función `volver_paso()`, que vuelve los valores de la red al momento previo de las modificaciones, uniendo esto con el hecho de que las funciones `agregar_conexion` y `remover_conexion` son inversas, se podría haber simulado el efecto de esa modificación en la red, y luego revertirlo.
   * `Agregar nodo` (392) ---> `SistemaElectrico.agregar_nodo()`. Agrega un nodo a partir de los datos pedidos dentor de la misma función, utiliza `__setitem__` del `Diccionario` correspondiente. a partir de su uso como:
   
         Diccionario[llave] = Nodo
      
   * `Remover nodo` (520) ---> `SistemaElectrico.remover_nodo()` Quita un nodo a partir de los datos pedidos, utiliza `pop` de `Diccionario`, de la manera:
   
         Diccionario.pop(llave)
         
* Parte 4 (Cálculo de potencia): Hecha casi completa (```graph.py```)
  * `Calcular demanda` (125) ---> `SistemaElectrico.calcular_demanda()`. Utiliza la función `Nodo.calcular_demanda()` (línea 86 de `clases.py`).
  * `Simular flujo` (202) ---> `SistemaElectrico.simular_flujo()`. Calcula el flujo de una estación elevadora, solo si no se alcanza a cubrir la demanda :D.
  
* Parte 5 (Consultas): Hecha completa (`graph.py`)
  * `Energía total de una comuna` (540) ---> `SistemaElectrico.consumo_total(comuna)`. Retorna el consumo total de este lugar, además del porcentaje correspondiente al total.
  * `Cliente con mayor consumo` (563) ---> `SistemaElectrico.mayor_menor_consumo(sigla_sistema, tipo=1)`. Retorna la casa con mayor consumo que tenga como sistema el dado en la función.
  * `Cliente con menor consumo` (563) ---> `SistemaElectrico.mayor_menor_consumo(sigla_sistema, tipo=2)`. Misma función que el anterior, sin embargo, cuando tipo == 2, la casa con menor consumo es retornada.
  * `Potencia perdida en la transmisión` (580) ---> `SistemaElectrico.potencia_perdida(id_casa)` Retorna la pérdida de potencia dese la estación elevadora hasta la casa con la id dada.
  * `Consumo de subestación` (601) ---> `SistemaElectrico.consumo_subestacion(id, tipo)`. Retorna el consumo total de la subestación de tipo "T" (transmisión) o "D" (distribución), con la id dada.
  
* Parte 6 (Excepciones): Hecha completa (`excepciones.py`)
  * `ElectricalOverload` (22)
  * `ForbiddenAction` (34)
  * `InvalidQuery` (3)
  
* Parte 7 (Testing): Hecha "completa" (`testing.py`)
   * `Energía total de una comuna` (47) ---> `test_consumo_total()`.
  * `Cliente con mayor consumo` (70) ---> `test_mayor_consumo()`.
  * `Cliente con menor consumo` (86) ---> `test_menor_consumo()`.
  * `Potencia perdida en la transmisión` (102) ---> `test_potencia_perdida()`.
  * `Consumo de subestación` (128) ---> `test_consumo_subestacion()`.
  * `InvalidQuery` (154) ---> `test_invalid_query()`.
  * `ForbiddenAction` (205) ---> `test_forbidden_action()`.
  * `ElectricalOverload` (154) ---> `test_electrical_overload()`. (Este test falla -se explica un poco de esto en un comentario al finalizar la función-, se plantea un caso en donde debería haber sobrecarga eléctrica al agregar conexiones, pero esto no ocurre, quizás por la formula que utilicé en el cálculo de potencia, o porque realmente el caso planteado no genera sobrecarga :o).


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Para ejecutar el testeo, el módulo es: `testing.py`.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```unittest```-> `TestCase`
2. ```os```-> `path.isfile`, `remove`
3. ```csv```-> `DictReader`
4. ```random```-> `randint`

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. `estructuras_de_datos`-> Contiene las estructuras de datos creadas para esta tarea.
2. `clases` -> Contiene las clases utilizadas como nodos al interior del grafo.
3. `graph`-> Contiene a `SistemaElectrico`, que representa el grafo junto a sus múltiples funciones :D.
4. `mensajes` -> Módulo con la clase `mensaje` utilizada para mostrar mensajes en pantalla (y así no sobrecargar los demás modulos con demasiados `print` :D).
5. `funciones` -> Contiene varias de las funciones utilizadas para esta tarea. (Nota: `range_()` pretende ser una función alternativa a `range()` predeterminado, en nuestro caso, esta retorna una `Lista` con enteros en el rango indicado).
6. `excepciones` -> Contiene las clases de exepciones utilizadas.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. (https://github.com/IIC2233/contenidos/blob/master/semana-06/1-listas-ligadas.ipynb): Contenido de Listas Ligadas del curso para la creación de la estructura de datos `Listas`.
2. (https://stackoverflow.com/questions/9252543/importerror-cannot-import-name-x): Aquí hay una solución a la "importación curuzada" que estaba dando error.
3. (https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float): `isnumeric` no me estaba funcionando con `float`, así que el comentario 52 de la página dio una buena idea que no pensé en utilizar.
4. (https://github.com/IIC2233/contenidos/blob/master/semana-07/1-grafos.ipynb): Algoritmo BFS para recorrer el grafo es utilizado en la creación de `SistemaElectrico`, a partir de los Contenidos de Grafos del curso.


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descue
