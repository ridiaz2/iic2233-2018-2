# Tarea 1: DCCAirlines :school_satchel:


A continuación, se presentan algunas consideraciones y datos de la _unica_ y _fabulosa_ Tarea 1 de Programación Avanzada, que presenta una plataforma para hacer consultas sobre aerolíneas.

## Consideraciones generales :octocat:

* La base de datos predeterminada para esta tarea es *medium*. Esta puede ser cambiada en la línea 10 de ```functions.py```, variable ```data_size```. (Pretendía crear un archivo de texto que pudiera ser modificado desde la misma consola (opción *Configurables* del Menú), sin embargo esta idea del programa no la completé, dejando la opción de todas formas -no entrega error si es seleccionada-).
* Una vez creada la variable ```data_size```, la variable ```ruta``` completa la dirección del archivo, la que es utilizada como variable global en la función ```load_database```. 
* Solo se guardaran en ```output.txt``` las consultas ingresadas directamente (: ([#257](https://github.com/IIC2233/syllabus/issues/257))
* En ```favourite_airport``` solo se contabilizan los aeropuertos de destino a los que los pasajeros llegaron más veces ([#250](https://github.com/IIC2233/syllabus/issues/250)).
* Los inputs ingresados por el usuario son verificados con la función ```revisar_input()```, la que a partir de una condición, revisa si el dato ingresado cumple con ella, y si no, hace un llamado recursivo hasta que lo haga.
* En ```popular_airports``` se retorna una tupla con el resultado de la consulta. (No revisé antes la *issue* [#199](https://github.com/IIC2233/syllabus/issues/199) :O)
* En 4 funciones utilicé foreach de una manera poco "legal" (me enteré algo tarde). Esto se explica un poco mejor en la sección que sigue (:

Nota: Algunas de estas consideraciones tienen una *issue* enlazada, ya que leí en algunas de ellas que idealmente las mencionáramos en el *Readme* si hacíamos cierta consideración, y me entusiasmé un poco :sweat_smile:

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 1 (Consultas que retornan otra base de datos): Hecha completa (```functions.py```)
   * ```load_database``` (110)
   * ```filter_flights``` (152) -> ```distancia_vuelo```
   * ```filter_passengers``` (162)
   * ```filter_passengers_by_age``` (173)
   * ```filter_airports_by_country``` (182)
   * ```filter_airports_by_distance``` (186) 
   
* Parte 2 (Consultas que no retornan otra base de datos): Hecha completa (```functions.py```)
   * ```favourite_airport``` (215) -> ```viajes_por_pasajero(*foreach*)``` ```mas_repetido```
   * ```passenger_miles``` (225) -> ```viajes_por_pasajero(*foreach*)```
   * ```popular_airports(*foreach*)(*Doitwell*)``` (242) -> ```calcular_popular```
         * (*Doitwell*): Esta función supera el máximo de 15 líneas (tiene 17). No lo noté antes, y no sé por qué me extendí demasiado. Una forma correcta sería cambiar:
         
         if avg:
              lista = sorted(list(diccionario_aeropuertos), key=lambda i:
              calcular_popular(diccionario_aeropuertos[i].split(" ")), reverse=True)[
                      :topn]
          else:
              lista = sorted(list(diccionario_aeropuertos), key=lambda i:
              calcular_popular(diccionario_aeropuertos[i].split(" "), False),
                             reverse=True)[:topn]
          return tuple(lista)
          
       Y dejarlo como:
         
         lista = sorted(list(diccionario_aeropuertos), key=lambda i:
              calcular_popular(diccionario_aeropuertos[i].split(" ")), avg),
                             reverse=True)[:topn]
         return tuple(lista)
         
         
   * ```airport_passengers(*foreach*)``` (268) 
   * ```furthest_distance(*foreach*)``` (285) 

* Parte 3 (Interacción con consola): Hecha completa (```main.py```, ```functions.py```)
   * Abrir archivo con consultas (19) -> ```main.py```
      Nota: Se tomará queries.txt como archivo predeterminado presionando [Enter]
   * Ingresar directamente consulta por consola (48) -> ```main.py```, ```guardar_consulta```
   * Leer ```archivo output.txt``` (56) -> ```main.py```

*(*foreach*): Las funciones marcadas con esto hacen referencia a que en ellas fue utilizada de manera "poco legal" el foreach. Cuando lo comencé a utilizar, creí que no habría problema, ya que en el fondo no estaba cambiando el input de la función, más bien, estaba guardando datos en un diccionario "externo". Al revisar [#308](https://github.com/IIC2233/syllabus/issues/308) noté que esto no era correcto (estando de acuerdo en que realmente no cumplía la función principal del foreach, como imprimir datos, por ejemplo). Sin embargo, en la misma *issue* nos comentan que utilizar ```map``` en estos casos sí es posible (:

En general, el uso del *foreach* estaba expresado de la siguiente forma:

    def funcion(iterable):
         diccionario = dict()
         foreach(lambda i: diccionario.update({i.llave:
            (diccionario.get(i.llave, "") + " " + i.valor).strip(
            )}), iterable)

Generando así un diccionario que ahora tiene valores "agrupados" de iterable. Utilizando map es posible cambiar la forma:

    foreach(func, iter)
    
 Y dejarla como un *mapeo*:
 
    [n for n in map(func, iter)]
    
Es decir, lo expresado anteriormente quedaría de la forma:

    def funcion(iterable):
      diccionario = dict()
      [n for n in map(lambda i: diccionario.update({i.llave:
         (diccionario.get(i.llave, "") + " " + i.valor).strip(
         )}), iterable)]
         
Adaptándose de una mejor manera a las reglas del enunciado. Pido disculpas por no notar esto antes, al momento de leer la *issue* no me daba el tiempo de revisar otra forma sin correr el peligro de entregar la tarea incompleta. Agradecería demasiado que estas funciones puedieran ser revisadas (aunque entendería completamente una disminución en el puntaje). ¡Muchas gracias!

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```collections```-> ```namedtuple``` (en el programa lo importé desde ```functools```, pero funcionó igualmente :O -en esta librería se importa parte de  ```collections``` (:-)
2. ```iic2233_utils```-> ```parse, foreach```
3. ```datetime```-> ```datetime```
4. ```itertools```-> ```tee, count```
5. ```functools```-> ```reduce```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```functions```-> Contiene todas las funciones creadas para la tarea.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Más que un supuesto, utilizo este espacio para intentar justificar por qué las funciones ```leer_output_txt()``` y ```guardar_output_txt``` exceden las 15 líneas :O. Fueron de las últimas funciones que hice, y disminuir la cantidad de líneas creí que sería algo forzado, porque su utilidad se adaptan a la forma irregular de presentar los datos en el archivo ```output.txt```. Aún así, podría haber hecho pequeñas funciones para ocupar menos espacio, o utilizar `foreach` cuando escribo en el archivo :O. Pido disculpas por esto, y estaría muy agradecido si estás fueran consideradas al estar más relacionada como funciones de interacción con la consola.


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. (https://stackoverflow.com/questions/1740726/turn-string-into-operator): Este código es implementado en ```operacion()``` de ```functions.py```, y es utilizado para interpretar una operación con simbolos o indicaciones (como "<" u "OR") y entrega el resultado de esta operación.
2. (https://stackoverflow.com/questions/1518522/find-the-most-common-element-in-a-list): Es implementado en ```mas_repetido()``` de ```functions.py```, y se utiliza para determinar el elmento más común de una lista.
3. ([Contenidos Semana 2: Reduce](https://github.com/IIC2233/contenidos/blob/master/semana-02/4-lambda-map-filter-reduce.ipynb)): En este *notebook de jupyter* de los contenidos del curso se encuentra una forma de aplanar listas de listas, método que es utilizado en ```furthest_distance``` de ```functions.py```.



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
