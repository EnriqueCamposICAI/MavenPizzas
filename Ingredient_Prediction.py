from codecs import latin_1_encode
import pandas as pd
import re
import generar_informe as inf


def pizza_ingredientes(df_pizza_type):
    # En esta función se va a crear un dict con los ingredientes de cada pizza
    dict_pizza_types = {}
    # Aquí se va a guardar lo q se necesita de cada pizza para tamaño
    dict_ingredientes = {}

    for i in range(len(df_pizza_type.index)):
        ingredientes_pizza = df_pizza_type.loc[i, 'ingredients'].split(
            ', ')        # Se crea lista con ingredientes de pizza
        # Si no se añade Mozzarella (condiciones)
        if 'Mozzarella Cheese' not in ingredientes_pizza:
            ingredientes_pizza.append('Mozzarella Cheese')

        # Si no lleva ninguna salsa la pizza
        if 'Sauce' not in df_pizza_type.loc[i, 'ingredients']:
            ingredientes_pizza.append('Tomato Sauce')

        dict_pizza_types[df_pizza_type.loc[i,
                                           'pizza_type_id']] = ingredientes_pizza       # Se crea clave = pizza, valor = list(ingr)

        for k in range(len(ingredientes_pizza)):
            dict_ingredientes[ingredientes_pizza[k]] = [
                0, 0, 0, 0, 0]      # Se crea el dict de ingredientes

    return dict_pizza_types, dict_ingredientes


def orders_ids(df_orders, semana):

    df_orders_n = df_orders[df_orders['date'].isin(semana)]
    orders_id_semana = df_orders_n['order_id'].tolist()

    return orders_id_semana


def pizzas_det(orders_id_semana, df_order_det):

    df_orders_det_n = df_order_det[df_order_det['order_id'].isin(
        orders_id_semana)]
    orders_semana = df_orders_det_n['pizza_id'].tolist()
    quantity_semana = df_orders_det_n['quantity'].tolist()

    for i in range(len(orders_semana)):
        orders_semana[i] = re.split(r'_', orders_semana[i][::-1], 1)
        orders_semana[i][0], orders_semana[i][1] = orders_semana[i][1][::-
                                                                       1], orders_semana[i][0][::-1]
        orders_semana[i].append(quantity_semana[i])

    # Estos son los detalles de todas las pizzas de interés
    return orders_semana


def calc_ing(pizzas_det_semana, dict_pizza_types, dict_ingredientes):

    for order in pizzas_det_semana:             # Para cada pedido:
        # Se saca la lista de ingredientes de esa pizza
        ingredientes_pizza = dict_pizza_types[order[0]]
        # Para cada ingrediente en la lista:
        for ing in ingredientes_pizza:
            if order[1] == 's':
                dict_ingredientes[ing][0] += order[2]
            # Dependiendo del tamaño, se suma la cantidad en el dict de ing la posición correspondiente
            elif order[1] == 'm':
                dict_ingredientes[ing][1] += order[2]
            elif order[1] == 'l':
                dict_ingredientes[ing][2] += order[2]
            elif order[1] == 'xl':
                dict_ingredientes[ing][3] += order[2]
            elif order[1] == 'xxl':
                dict_ingredientes[ing][4] += order[2]

    # Se devuelven todos los ingredientes con las necesidades
    return dict_ingredientes


def extract(nombres):
    # SE SACAN LOS DATAFRAMES
    archivos = []
    for i in range(len(nombres)):
        archivos.append(pd.read_csv(
            f"Datasets_pizza/{nombres[i]}", encoding="utf-8"))

    return archivos


def transform(archivos, semana):
    # Se sacan los diccionarios de ingredientes y pizzas con sus ingredientes
    dict_pizza_types, dict_ingredientes = pizza_ingredientes(archivos[3])

    # Se sacan los order_ids de la semana
    orders_id_semana = orders_ids(archivos[2], semana)

    # Detalles de los pedidos de esa semana
    pizzas_det_semana = pizzas_det(orders_id_semana, archivos[1])

    dict_ingredientes = calc_ing(
        pizzas_det_semana, dict_pizza_types, dict_ingredientes)     # Se calculan los ingredientes

    return dict_ingredientes


def estimate(datos, ponderaciones):
    llaves = list(datos[0].keys())
    datos_est = []
    for i in range(len(datos)):
        dict_semana = {}

        for j in range(len(llaves)):
            suma = 0
            for k in range(len(ponderaciones)):
                suma += datos[i][llaves[j]][k]*ponderaciones[k]
            dict_semana[llaves[j]] = suma
        datos_est.append(dict_semana)

    return datos_est


def estimacion_std(archivos):

    datos_semanas = []

    # Seleccionar primer día
    dia = pd.Timestamp('1/1/2015')

    while pd.Timestamp(dia).weekday() != 0:
        dia = dia + pd.Timedelta(days=1)

    semana_pas = [dia + pd.Timedelta(days=i) for i in range(0, 7)]

    cont = 0
    while (semana_pas[0] + pd.Timedelta(days=7)) < pd.Timestamp('1/1/2016'):
        cont += 1
        semana = [semana_pas[j].strftime('%d/%m/%Y') for j in range(7)]
        datos_semanas.append(transform(
            archivos, semana))

        semana_pas = [semana_pas[j] + pd.Timedelta(days=7) for j in range(7)]

    # Se crea un dataframe donde mostrar los datos

    # Falta hacer la media de los ingredientes, pero no se puede dar una sol exacta.

    ponderaciones = [50/50, 78.5/50, 113/50,
                     153.9/50, 201.1/50]  # 1 ración = s

    # Calculamos la estimación para cada ingrediente / semana

    datos_est = estimate(datos_semanas, ponderaciones)

    dataframe = pd.DataFrame(datos_est).transpose()

    dataframe.columns = [f'Semana {i}' for i in range(
        1, len(dataframe.columns)+1)]

    dataframe['Media Sem'] = dataframe.mean(axis=1)
    dataframe['Max'] = dataframe.max(axis=1)
    dataframe['Des. Est.'] = dataframe.std(axis=1)
    dataframe['Recomendado'] = (
        (dataframe['Media Sem'] + dataframe['Des. Est.'])).astype(int)
    dataframe.rename({'Unamed: 0': 'Ingredientes'}, axis=1, inplace=True)

    # Se ha sacado la media de los ingredientes por semana, y se ha calculado la desviación estándar
    # Si calculamos la media + desviación estándar, tendremos una estimación de lo que se necesita para la semana siguiente
    # Acertaremos en un 88% de las semana / ingrediente

    return dataframe


def load(dataframe):

    dataframe.sort_values(by='Recomendado', ascending=False,
                          inplace=True)
    print(dataframe)
    dataframe.astype(int).to_csv(
        "Datasets_pizza/Prediccion_ingredientes_Final_2015.csv")     # Se guarda el csv

    #texto = "En este archivo se encuentra una prediccion con las cantidades que deberia tener Maven Pizzas\npara cada semana en funcion de los datos de las semanas de 2015. El dato por ingrediente recomendado consiste\nen la suma de la media de todas las semanas mas la desviacion tipica.\nEsto confiere alrededor del 88% de los datos, sugiriendo una buena prediccion. Las cantidad son raciones para una pizza pequeña\n\n"
    # with open('Prediccion_Pizzas_Final', 'w') as file:
    #    file.write(texto)
    #    file.write(dataframe['Recomendado'].to_string())


def main():
    ### EXTRACT ###
    nombres = ['data_dictionary.csv', 'order_details.csv',
               'orders.csv', 'pizza_types.csv', 'pizzas.csv']

    archivos = extract(
        nombres)

    # informe_datasets = inf.generar_informe_datos(
    #    [df_data_dict, df_order_det, df_orders, df_pizza_type, df_pizzas], nombres)

    # with open("Informe_datasets.txt", "w") as file:
    #    file.write(informe_datasets)

    ### AHORA SE CALCULARÁ UNA MEDIA DE LOS INGREDIENTES POR DÍA DE LA SEMANA ###

    # Hay que calcular los ingredientes para cada semana
    # Se hace la media con las semanas contadas

    # Arriba tenemos la forma de sacar los ingredientes de una semana,
    # así que sacaremos una lista con los ingredientes de cada semana y luego haremos la media

    datos_finales = estimacion_std(
        archivos)

    load(datos_finales)


if __name__ == "__main__":

    main()
    pass
