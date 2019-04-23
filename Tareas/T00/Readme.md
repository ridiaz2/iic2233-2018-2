# Tarea 0: DCCorreos :school_satchel:


A continuación, se presentan algunas consideraciones y datos de la _unica_ y _fabulosa_ Tarea 0 de Programación Avanzada, cuya finalidad es rehacer el sistema de correos electrónicos de los ayudantes del curso, tras el ataque cibernético del Dr. H4.

## Consideraciones generales :octocat:

* Tengo entendido que los archivos deberían estar en snake_case, sin embargo, al traspasar algunos de estos a la carpeta donde está clonado este repositorio, los cambié a una combinación entre CamelCase y snake_case.
* Pretendía crear una librería propia donde estuvieran todas las funciones utilizadas por más de un archivo, sin embargo, no pude completar esta acción, por lo que existe una cantidad innecesaria de importaciones al principio de cada librería.
* En el apartado ```Extra``` se adjuntan algunas explicaciones de algunas funciones, ya que no las redacté al momento de hacer la tarea.
Pido disculpas por estos detalles, y los tendré en consideración para la próxima tarea.

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 1 (Registro e inicio de sesión): Hecha completa (```Menu.py```)
* Parte 2 (Correos y Bandeja de Entrada): Hecha completa (```Correo.py```, ```Bandeja_de_Entrada.py```)
* Parte 3 (Calendario): Hecha completa (```Calendario.py```, ```Eventos.py```)
* Parte 4 (Encriptación): Hecha completa (```Encriptacion.py```)

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```Menu.py```.
Nota: Se explica un poco más de su funcionamiento en el apartado de ```Librerías propias```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```collections```-> ```namedtuple```
2. ```datetime```-> ```datetime, timedelta```
3. ```random```-> ```randint```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```Bandeja_de_Entrada```-> Contine a ```bandeja(usuario, datos)``` como base de la plataforma de correos recibidos, y otras funciones que son principalmente utilizadas para visualizar la bandeja de entrada del usuario.
2. ```Correo```-> Contiene a ```plataforma_correo(usuario)``` que enlaza a otras funciones contenidas en la librería, y que sirven para escribir y enviar nuevos mensajes de correo. Además incluye algunas funciones que son utilizadas para verificar inputs, entre otros.
3. ```Calendario```-> Contiene a ```buscador_evento(datos, usuario)```, función central utilizada en la búsqueda de eventos. Además, contiene la clase ```Evento```.
4. ```Eventos```-> Contiene a ```evento_nuevo()```, que permite crear un nuevo evento, utilizando funciones de la librería, y otras externas (de ```Calendario``` por ejemplo).
5. ```Encriptacion``` -> Contiene a ```encriptar(mensaje)``` y ```desencriptar(codigo)``` (Utilizadas por ```Correo``` y otras funciones utilizados en el proceso de encriptación de los correos.
6. ```Menu``` -> Es el módulo principal de la tarea, e incluye funciones que muestran el menú principal y el menú de inicio de sesión, junto a otras utilizadas por estos. Este módulo enlaza a las otras librerías (incluyendo ```Encriptacion```, enlazada a través de ```Bandeja_de_Entrada``` y ```Correo```).

Nota: Una pequeña explicación de las distintas funciones se adjunta al final de este archivo, ya que no las expliqué en cada módulo (pido disculpas por esto, ya que se explicita que no debería hacerlo).

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Consideré que un evento del Calendario puede tener igual nombre y fecha, siempre y cuando tenga propietarios distintos. Creo que tiene sentido que un propietario no cree eventos duplicados, mientras que alguien distinto puede crear eventos similares (incluso si ya está invitado a uno idéntico). Esto se verifica a través de un identificador que une las fechas, el título y el usuario del propietario.


-------



**EXTRA:**
Algunas funciones no están bien explicadas en los módulos de la Tarea, por lo que se adjuntan algunas explicaciones en caso de no quedar completamente claro su funcionamiento.
1. ```Bandeja_de_Entrada:```
* obtener_datos(): carga los datos de los archivos que contienen los correos enviados.
* obtener_recibidos(usuario, datos): filtra los datos para entregar solo aquellos que contengan al usuario entre los destinatarios.
* es_numero(numero, largo): función de verificación.
* resumen_destinatarios(destinatarios, opcion="destinatarios"): Muestra de una forma más "amigable" la lista de invitados. Una variación de esta función es utilizada en los eventos de calendario cuando opcion="invitados" por ejemplo.
* mostrar_correo(correo): imprime en pantalla los datos del correo. Permite ingresar algunas opciones como volver a pasos anteriores o -eventualmente- imprimir la lista completa de invitados.
* bandeja(usuario, recibidos): es la plataforma principal del módulo, y el enlace al menú principal.

2. ```Correo:```
* obtener_etiquetas(numeros): retorna las etiquetas correspondientes a los números seleccionados por el usuario.
* imprimir_mensaje(mensaje, caracter=" ", numero=78): permite imprimir de una manera más "amigable" aquellos mensajes ingresados. Esto a partir de un límite de carácteres por línea (78 como predeterminado), con un caracter específico (" " como predeterminado) como separador de líneas para evitar discontinuidades de palabras, por ejemplo.
* dudas_input(): utilizado recurrentemente para notificar que cierto input no es soportado por la plataforma.
* dudas_caracteres(apartado, largo, texto, minimo=0): permite notificar ciertas restricciones de caracteres en algún apartado en específico, considerando el largo máximo, el texto a evaluar y opcionalmente un largo mínimo.
* error_usuario(usuario): retorna True si el nombre de usuario es válido, y False en cualquier otro caso.
* error_destinatarios(destinatarios): notifica posibles errores dentro de los destinatarios, y da la opción de corregirlos.
* dudas_etiquetas(etiquetas): permite validar si el input de las etiquetas es soportado por la plataforma.
* modificar_correo(usuario, destinatarios, asunto, mensaje, etiquetas, opcion): permite modificar datos del correo antes de enviarlo.
* enviar_correo(usuario, destinatarios, asunto, mensaje, etiquetas): guarda el correo en la base de datos.
* plataforma_correo(usuario): es la plataforma principal del módulo, y el enlace al menú principal.

3. ```Calendario:```
* transformar_fecha_inverso(fecha): transforma una instancia datetime.datetime en un string de la forma YY-MM-DD hh:mm:ss.
* archivo_perteneciente(evento): entrega un string de la forma "ij", donde i indica el archivo en donde se encuentra el evento, y j la línea de ubicación.
* transformar_fecha(fecha, orden=False): transforma un string de la forma YY-MM-DD hh:mm:ss a una instancia datetime.datetime. Si orden==True, entonces la forma del string es DD-MM-YY hh:mm:ss.
* generar_id(lista): genera una id utilizando las fechas, el título y el nombre de usuario del propietario del evento.
* Evento: clase creada a partir de una namedtuple.
* obtener_eventos(): obtiene los datos de los archivos que contienen la información de los eventos.
* fechas_coinciden(fecha, fecha_i, fecha_f): esta función no es utilizada en la tarea, pero su idea principal era permitir al usuario buscar fechas de eventos con palabras.
* error_fecha(fecha): permite reconocer si el input de la fecha es soportado por la plataforma.
* ordenar_eventos(evento): es utilizado como key en sorted() para ordenar los datos de los eventos.
* buscar_fecha(mes, fecha): permite expresar una fecha indicando el día.
* cero(fecha): agrega un cero a un string (de número) si este es de un solo dígito (permite por ejemplo pasar de 27-8-2018 a 27-08-2018)
* mostrar_fecha(fecha_i, fecha_f): permite imprimir las fechas de una manera más "amigable", donde la forma de retornar el string dependerá de si ambas fechas coinciden en el mismo día.
* modificar_evento_editor(evento, opcion): permite modificar ciertos atributos de un evento ya existente.
* editar_evento(evento): menú y plataforma principal de edición de eventos.
* mostrar_info_evento(evento, crear_evento=False, editor=False, usuario=""): permite mostrar la información del evento, donde crear_evento y editor indicarán el lugar en donde se utilizó la función. usuario es utilizado para verificar si es posible editar el evento.
* mostrar_eventos(datos, buscador=False, usuario=""): muestra los resultados de búsqueda.
* buscador_evento(datos, usuario): es la plataforma principal del módulo, y el enlace al menú principal.

4. ```Eventos:```
* comparar_fechas(fecha_i, fecha_f): revisa si la fecha de cierre ocurre después de la de inicio.
* modificar_evento(usuario, nombre, fecha_i, fecha_f, descripcion, invitados, etiquetas, opcion): permite modificar datos del evento antes de crearlo.
* crear_evento(usuario, nombre, fecha_i, fecha_f, descripcion, invitados, etiquetas): permite guardar el evento en la base de datos.
* evento_nuevo(usuario, datos): es la plataforma principal del módulo, y el enlace al menú principal.

5. ```Encriptacion:```
* intercambio_0_1(numero): si recibe un 0 -> retorna un 1, si recibe un 1 -> retorna un 0.
* cifrado_cesar(caracter, cifrar=True): realiza el algoritmo correspondiente al Cifrado César. Si cifrar==True, la función aplica el cifrado. En caso de ser False, se aplica el proceso inverso.
* caracter_a_binario(caracter, numerico=False): transforma un caracter a binario. Si numerico==False, el caracter pasa por ASCII antes de binario.
* binario_a_caracter(binario): transforma de binario a número, para luego entregar un caracter.
* obtener_cadena_aleatoria(): retorna una cadena aleatoria de 10 dígitos.
* clave(): retorna la clave, que en el caso de la tarea es "2233"
* obtener_cadena_inicio(cadena_aleatoria): retorna una cadena que une la clave con la cadena aleatoria hasta completar 256 dígitos.
* obtener_lista(cadena_inicio, largo_mensaje): realiza el paso 5 de la encriptación.
* binario_a_mensaje(binario): recibe un codigo en binario, y retorna el mensaje correspondiente.
* encriptar(mensaje): retorna un código producto de la encriptación del mensaje.
* desencriptar(codigo): traduce el codigo como un mensaje y lo retorna.

6. ```Menu:``` 
* menu_principal(): función principal correspondiente al menú de inicio, que se muestra al iniciar el programa.
* abrir_datos_usuarios(): obtiene los datos ubicados en los archivos correspondientes a los usuarios y sus contraseñas.
* validar_usuario(datos, usuario): verifica si el usuario es válido.
* agregar_usuario(usuario, contraseña): guarda al usuario creado en la base de datos.
* nuevo_usuario(datos): plataforma para crear un usuario nuevo.
* menu_inicio(): plataforma de inicio de sesión.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. (http://code.activestate.com/recipes/65117-converting-between-ascii-numbers-and-characters/): Más que una referencia, es el sítio en donde encontré las funciones ord() y chr() para hacer la transformaciones en ASCII. Son utilizadas en ```Encriptacion.py```.
2. (http://daniel.blogmatico.com/python-de-binario-a-decimal-y-de-decimal-a-binario/): Al igual que la anterior, en esta página encontré un uso de la función int() que permite transformar de binario a decimal. Es utilizada en ```Encriptacion.py```.



## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
