# FoodExpress (muestreo)
Estudiante: Diego Torres Durante

## Contexto
Origen de los datos: Esta tabla representa una muestra extraída y adaptada de conjuntos de datos clásicos de logística y predicción de tiempos de entrega de plataformas comerciales (similares a los datasets de Food Delivery Time Prediction en Kaggle).

Contexto del Sistema: Son el equipo de ingeniería de "FoodExpress", una aplicación de entrega de comida. Tienen un clúster de bases de datos con 5 millones de registros de pedidos entregados el último año. La gerencia quiere entrenar un algoritmo que prediga el "Tiempo Estimado de Entrega" para mostrárselo al cliente en la pantalla de carga.

Dado que su servidor de entrenamiento no tiene suficiente memoria RAM para cargar 5 millones de registros, tienen que diseñar una consulta para extraer una muestra de entrenamiento de solo 10,000 registros.

Tabla de Datos Crudos: Esta hoja representa una vista previa microscópica de lo que hay en la base de datos total.


| ID_Pedido | Zona_Ciudad | Transporte | Clima     | Tiempo_Entrega (Min) | Calificacion_App | Queja_Soporte |
| --------- | ----------- | ---------- | --------- | -------------------- | ---------------- | ------------- |
| 1001      | Centro      | Moto       | Despejado | 15                   | 5                | No            |
| 1002      | Suburbio    | Auto       | Lluvia    | 48                   | 1                | Sí            |
| 1003      | Centro      | Bici       | Despejado | 22                   | N/A              | No            |
| 1004      | Centro      | Moto       | Despejado | 12                   | N/A              | No            |
| 1005      | Periferia   | Auto       | Lluvia    | 65                   | 1                | Sí            |
| 1006      | Centro      | Bici       | Despejado | 25                   | N/A              | No            |
| 1007      | Suburbio    | Moto       | Despejado | 30                   | N/A              | No            |
| 1008      | Centro      | Moto       | Despejado | 18                   | 4                | No            |
| 1009      | Periferia   | Moto       | Lluvia    | 55                   | 1                | Sí            |
| 1010      | Centro      | Bici       | Despejado | 20                   | N/A              | No            |
| 1011      | Suburbio    | Auto       | Despejado | 35                   | N/A              | No            |
| 1012      | Centro      | Moto       | Despejado | 14                   | 5                | No            |
| 1013      | Periferia   | Auto       | Despejado | 45                   | N/A              | No            |
| 1014      | Centro      | Bici       | Lluvia    | 40                   | 2                | Sí            |
| 1015      | Suburbio    | Moto       | Lluvia    | 50                   | 1                | Sí            |
| 1016      | Centro      | Moto       | Despejado | 16                   | N/A              | No            |
| 1017      | Periferia   | Auto       | Lluvia    | 60                   | 1                | Sí            |
| 1018      | Centro      | Moto       | Despejado | 13                   | 5                | No            |
| 1019      | Suburbio    | Bici       | Despejado | 28                   | N/A              | No            |
| 1020      | Centro      | Moto       | Despejado | 17                   | N/A              | No            |

## Respuestas
Instrucciones: Basándose puramente en la inspección visual de esta muestra y en los conceptos de técnicas de muestreo, debatan en equipo las siguientes tres propuestas de extracción que hicieron distintos desarrolladores de la empresa. Respondan detalladamente cada pregunta.

Pregunta 1:

- Un desarrollador Junior sugiere que, para que el algoritmo aprenda mejor, la consulta de extracción debería ignorar los campos vacíos usando la lógica WHERE Calificacion_App IS NOT NULL.
    
- Observen la tabla: ¿Qué característica comparten casi todos los registros que SÍ tienen una calificación? ¿Qué sesgo (bias) exacto introducirían al muestreo si aceptan esta propuesta y cómo afectaría las predicciones en producción? La mayoría de los casos serían quejas negativas en días lluviosos, con un tiempo mayor a 40 minutos, es la característica que se comparten con los registros con calificaciones, por lo tanto, no se balancearía con la otra cantidad de registros donde las cosas salen bien y el usuario se va contento pero no da una reseña.
    

Pregunta 2:

- Supongan que la variable Transporte = Bici representa solo el 3% de los 5 millones de registros en la base de datos real. Si utilizan un Muestreo Aleatorio Simple para extraer su muestra de 10,000 registros, ¿cuál es el peligro algorítmico al que se enfrentan con respecto a las bicicletas? Si se hace un muestreo aleatorio, al ser tan poco el porcentaje de registros donde el transporte hay bici, puede que en la muestra no aparezcan datos de bicicletas, en un muestreo aleatorio no se conserva un porcentaje representativo.
    

Pregunta 3:

- Saben por los reportes de operaciones que la variable clave que destruye los tiempos de entrega es el Clima. En la base de datos total, el 85% de los pedidos se hacen en clima "Despejado" y el 15% en clima "Lluvia". Para garantizar que su algoritmo aprenda correctamente a predecir, diseñen una extracción basada en Muestreo Estratificado.
    
- Describan la regla matemática: De su muestra final de 10,000 registros, ¿cuántos registros exactos deben provenir del clima "Despejado", cuántos del clima "Lluvia", y por qué esto es superior a la extracción aleatoria simple?
    8,500 despejado, 1500 lluvia, se conserva un ratio de porcentajes representativo de la población y evita sesgos.

Entregable: Documento con las respuestas.
