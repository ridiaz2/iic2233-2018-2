# Tarea 4: DCCurve :school_satchel:


A continuación, se presentan algunas consideraciones y datos de la _unica_ y _fabulosa_ Tarea 4 de Programación Avanzada, que presenta una juego basado en servidor y clientes.



## Consideraciones generales :octocat:

* En general, para este documento, se referirá a `cliente.py` al archivo ubicado en `cliente/cliente.py`, y a `servidor.py` como el archivo `servidor/servidor.py`
* Las variables `HOST` y `PORT` son modificables y permiten indicar la IP y el Puerto, respectivamente. Estas se encuentran en:
      * Líneas 16 y 17 --> `cliente.py`
      * Líneas 21 y 22 --> `servidor.py`
* Se utilizó la [Ayudantía de Networking](https://github.com/IIC2233/syllabus/tree/master/Ayudantias/S13%20-%20Networking) como base para el desarrollo de la tarea. Los créditos no fueron modificados y se encuentran en la primera línea de `servidor.py` y `cliente.py`.


### Cosas implementadas y no implementadas :white_check_mark: :x:

* A grandes rasgos, todo fue implementado, excepto la parte de los poderes (con excepción de que si pasan por el icono, este sí desaparece). Esta tarea la estoy entregando con atraso D: así que no alcanzo a escribir un Readme perfecto ante de las 23:59, sin embargo, dejo este [enlace](https://github.com/ridiaz2/Repositorio-u-/blob/master/T04/Readme.md) (de un Readme que iré modificando) donde se especifica el funcionamento del juego paso a paso.

## Ejecución :computer:
* El módulo principal del cliente está en: ```cliente/cliente.py```.
* El módulo principal para iniciar el servidor está en: `servidor/servidor.py`.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. `PyQt5`
2. `threading`
3. `socket`
4. `json`
5. `os`
6. `haslib`
7. `pickle`
8. `time`
9. `random`
10. `itertools`
11. `sys`
12. `datetime`


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. `servidor/`
   * `backend`
   * `excepciones`
   * `parameters`

2. `cliente/`
   * `backend`
   * `excepciones`
   * `frontend`
   * `juego`
   * `parameters`

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. (https://github.com/IIC2233/syllabus/tree/master/Ayudantias/S13%20-%20Networking): Ayudantía de Networking como base para la tarea.


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md)
