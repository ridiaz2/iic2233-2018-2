# Entregable Tarea 3

A continuación se explica a grandes rasgos en qué consistirá el algoritmo para calcular la demanda (:

### En general se tiene que:

* La potencia total en una casa *i* está dada por:

   *Demanda(i) = Consumo(i) + (Consumo_nodos_hijos + Pérdida_en_conexión)(i)*
   
   donde *Consumo_nodos_hijos* corresponde a la sumatoria de el consumo que tiene cada casa conectada a esta, y *Pérdida_en_conexión* hace referencia a la sumatoria de los gastos de energía que existe cuando esta pasa por el cable que conecta ambas casas.
   
* Básicamente el algoritmo funcionará considerando la estrategia **DFS**, de esta forma, se irían guardando en un *diccionario* (por ejemplo) todos los caminos. Considerando que cada parte del grafo tiene sus nodos hijos registrados, puede parecer "fácil" obtener los datos de consumos. Como se dice en el enunciado, se lee desde abajo hacia arriba.
   
