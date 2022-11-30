# MavenPizzas
Se han realizado varias documentos y predicciones para Maven Pizzas de cara a preparar los años próximos. Todos los archivos necesarios se encuentran en las diferentes ramas de este repositorio. 
Para la ejecución correcta de todos los archivos hay que saber qué archivos requiere de otros. A continuación una pequeña guía. 

  - Ingredient_Prediction.py -> requiere generar_informe y los csv de datasets_pizza. Carga los     archivos en esa misma carpeta. 
  - generar_informe.py -> requiere una lista con los dataframes y otra con sus nombres               respectivamente
  - Informe_Estimacion_xml.py -> requiere los archivos de la carpeta Datasets_pizza, incluyendo     la estimación realizada. También requiere generar_informe.py. Carga los resultados en la         misma carpeta donde se encuentre el archivo. 
  - Limpieza_archivos.py -> requiere los archivos nombre_mod.csv de la carpeta                       Datasets_pizza_mod y cargará los resultados en la misma carpeta. 
  - MavenPizza_Report_PDF.py -> requiere la carpeta Datasets_pizza_fixed*, graficas (las crea en     el propio archivo, pero no las guarda, ya que las de la carpeta son las de los datos) y         logo_MavenPizzas.jpg y carga los resultados en la misma carpeta en la que se encuetre el         archivo. 
  - MavenPizza_Report_Excel.py -> requiere la carpeta Datasets_pizza_fixed* y guarda los             resultados en la misma carpeta donde se encuentre el archivo.

* Nota Datasets_pizza_fixed: es una ejecución propia de Limpieza_archivos.py, pero como ese       archivo contiene aleatoriedad en la asignación de las pizzas para los nan, los resultados no     serían siempre los mismos. Por ello, Limpieza_archivos.py guarda los resultados en               Datasets_pizza_mod. Datasets_pizza_fixed no se debe cambiar. 
