import pandas as pd
from fpdf import FPDF
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import re
import warnings


def generarPDF(tabla_ingredientes, medidas_basicas, dinero):

    exec_report = FPDF()
    exec_report.add_page()
    exec_report.set_margins(20, 20, 20)
    exec_report.set_font('Arial', 'BU', 18)

    exec_report.cell(
        170, 16, txt='EXECUTIVE REPORT - MAVEN PIZZAS 2016', ln=1, align='C')
    exec_report.ln(6)
    exec_report.image('logo_MavenPizzas.jpg', x=70, w=80)
    exec_report.set_font('Arial', 'B', 12)
    exec_report.ln(12)
    exec_report.cell(w=170, h=10, txt='Abstract', ln=1, align='L')
    exec_report.set_font('Arial', '', 12)
    exec_report.multi_cell(
        w=170, h=6, txt='Este reporte ejecutivo recoge los datos de la empresa Maven Pizzas para el año 2016. En él, se han incluido diferentes medidas básicas para explicar el rendimiento de la empresa para el curso, además de un número de gráficas que ayudarán a postularse de cara al futuro y mejorar su posición en el mercado. Cabe destacar que los datos de ese año estaban corruptos, así que la información dada solamente se puede tomar como una aproximación, y no como hechos verídicos. Para obtener unos resultados más realistas, comparar estos datos con reportes ejecutivos de años anteriores. En el tratado de datos se han realizado algunas aproximaciones:\n    - Orders_mod.csv -> Las fechas y horas que faltaban se han tomado respecto a los valores anteriores y siguientes, respetando siempre que se siga el orden de los pedidos, variable que no estaba corrupta. Se ha procedido a leer los diferentes tipos de fechas.\n    - Order_details_mod.csv -> se han corregido todas las erratas de escritura, y leído correctamente las cantidades. Para las pizzas que faltaban en un pedido se ha escogido una aleatoria de la carta, comprobando que no estaba ya en el pedido.\n', align='J')

    exec_report.set_font('Arial', 'B', 12)
    exec_report.cell(
        w=170, h=12, txt='Medidas Básicas del curso 2015', ln=1, align='L')
    exec_report.set_font('Arial', '', 12)
    exec_report.multi_cell(
        w=170, h=6, txt=f'    - Pedidos totales -> {medidas_basicas[0]}\n    - La media de pedidos diarios -> {round(medidas_basicas[3],2)}\n    - El día con más pedidos fue el {medidas_basicas[1]} con {medidas_basicas[2]} pedidos\n    - El dinero generado es ${dinero}', align='J')
    # Escribir aquí

    exec_report.add_page()
    exec_report.set_font('Arial', 'B', 12)
    exec_report.cell(
        w=170, h=12, txt='Cantidad de Pedidos por pizza', ln=1, align='L')
    exec_report.set_font('Arial', '', 12)
    exec_report.multi_cell(
        w=170, h=6, txt='Aquí podemos ver una gráfica con las pizzas más pedidas. Podemos ver grandes ventas de las 6, primeras (Classic Deluxe, Hawaiian, Pepperoni, Barbacue Chicken, Thai Chihcken y California Chicken). Sin embargo, la que peores resultados da es la Brie Carre, por lo que se debería pensar si se debiera seguir ofreciendo.', align='J')
    exec_report.image('Graficas/grafica_pizza_tipo.jpg', w=170)

    exec_report.ln(6)

    exec_report.set_font('Arial', 'B', 12)
    y = exec_report.get_y()
    exec_report.cell(
        w=170, h=12, txt='Cantidad de Pedidos por Tamaño', ln=1, align='L')
    exec_report.set_font('Arial', '', 12)
    exec_report.multi_cell(
        w=80, h=6, txt='En este caso vemos las pizzas divididas por el tamaño que se han pedido. Se puede ver cómo hay una gran diferencia respecto a los tamaño XL y XXL. Esto es porque actualmente la empresa solamente ofrece pizzas XL y XXL en el tipo Greek, por lo que se debería considerar añadirlas al resto de pedidos.', align='J')
    exec_report.image('Graficas/grafica_pizza_tamano.jpg', x=110, y=y, w=80)

    exec_report.add_page()

    exec_report.set_font('Arial', 'B', 12)
    y = exec_report.get_y()
    exec_report.cell(
        w=170, h=12, txt='Horas de los pedidos', ln=1, align='L')
    exec_report.set_font('Arial', '', 12)
    exec_report.multi_cell(
        w=80, h=6, txt='En este gráfico se muestra en qué momento del día se han realizado los pedidos, pudiendo saber los momentos de más necesidad de personal o incluso de cambios en horarios. Por ejemplo, hasta las 11 AM no hay muchos pedidos y depués de las 10 PM decae bastante.', align='J')

    exec_report.image('Graficas/grafica_pizza_horas.jpg', x=110, y=y, w=80)

    exec_report.ln(6)

    exec_report.set_font('Arial', 'B', 12)
    y = exec_report.get_y()
    exec_report.cell(
        w=170, h=12, txt='Meses de los pedidos', ln=1, align='L')
    exec_report.set_font('Arial', '', 12)
    exec_report.multi_cell(
        w=80, h=6, txt='En este gráfico se muestra en qué meses del año se ha realizado cada pedido. Como se puede observar, no hay valores muy dispares por lo que se puede on¡bservar que no ha habido grandes decaídas en el número de pedidos duarnte el año.', align='J')
    exec_report.image('Graficas/grafica_pizza_mes.jpg', x=110, y=y, w=80)

    exec_report.add_page()

    exec_report.set_font('Arial', 'B', 12)
    y = exec_report.get_y()
    exec_report.cell(
        w=170, h=12, txt='Tabla con estimación de ingredientes', ln=1, align='L')
    exec_report.set_font('Arial', '', 12)
    exec_report.multi_cell(
        w=170, h=6, txt='En esta tabla se muestra una estimación de los ingredientes que serán necesarios semanalmente para poder trabajar correctamente. Se ha realizado calculando la cantidad de raciones de ingredientes que se han utilizado en cada semana y luego su media (media de ventana deslizante), a la que se ha sumado la desviación típica. El resultado debería cumplir en el 88% de las semanas.', align='J')
    exec_report.ln(3)
    y = exec_report.get_y()
    exec_report.multi_cell(
        w=80, h=6, txt=tabla_ingredientes[0], align='L')
    exec_report.set_xy(110, y)
    exec_report.multi_cell(
        w=80, h=6, txt=tabla_ingredientes[1], align='L')
    exec_report.ln(3)
    exec_report.set_font('Arial', 'B', 12)
    exec_report.cell(
        w=170, h=6, txt='*NOTA: el número corresponde con raciones de pizzas pequeñas', ln=1, align='L')
    exec_report.set_author('Enrique Campos Alonso')
    exec_report.set_keywords('MavenPizza, Executive, Report, 2016, Pizza')

    exec_report.output('MavenPizza_Report.pdf', dest='F')


def extract(archivos):
    # SE SACAN LOS DATAFRAMES
    archivos_nuevos = []
    for i in range(len(archivos)):
        archivos_nuevos.append(pd.read_csv(
            f"Datasets_pizza_fixed/{archivos[i]}", encoding="utf-8"))

    return archivos_nuevos


def pedidos(archivos):
    # Número pedidos al año
    # Contar número de filas de orders.csv

    pedidos_año = archivos[2].shape[0]

    # Día con más pedidos
    dia_pedidos_max = archivos[2].mode()['date'][0]
    cuenta_pedidos_moda = archivos[2]['date'].value_counts()[dia_pedidos_max]

    # Media de pedidos por día
    media_pedidos = archivos[2]['date'].value_counts().mean()

    return [pedidos_año, dia_pedidos_max, cuenta_pedidos_moda, media_pedidos]


def dinero_ganado(archivos):
    # Se recorre el df de order_details.csv y se busca el nombre de la pizza por la cantidad

    money = 0
    archivos[4].index = archivos[4]['pizza_id']
    for i in range(len(archivos[1].index)):
        row = archivos[1].iloc[i]
        pedido = row['pizza_id']
        money += archivos[4].loc[pedido, 'price'] * row['quantity']

    return money


def ingredientes():
    pred_ingredientes = pd.read_csv(
        "Datasets_pizza_fixed/Prediccion_ingredientes_Final_2016.csv", encoding="utf-8")
    pred_ingredientes.rename(
        columns={'Unnamed: 0': 'Ingrediente'}, inplace=True)
    pred_ingredientes.set_index(pred_ingredientes['Ingrediente'], inplace=True)

    indice = pred_ingredientes.index

    string1 = ''
    for i in range(33):
        string1 += f'   - {indice[i]} => {pred_ingredientes.loc[indice[i], "Recomendado"]}\n'

    string2 = ''
    for i in range(33, 66):
        string2 += f'   - {indice[i]} => {pred_ingredientes.loc[indice[i], "Recomendado"]}\n'

    return [string1, string2]


def graficos_per_pizzas(archivos):

    dict_tipo_pizzas = {}
    dict_tamaño_pizzas = {'S': 0, 'M': 0, 'L': 0, 'XL': 0, 'XXL': 0}

    for i in range(len(archivos[1].index)):
        pizza = re.split(
            r'_', archivos[1].loc[i, 'pizza_id'][::-1], 1)

        tamaño_pizza = pizza[0][::-1].upper()
        tipo_pizza = pizza[-1][::-1]
        cantidad = archivos[1].loc[i, 'quantity']

        if tipo_pizza in dict_tipo_pizzas:
            dict_tipo_pizzas[tipo_pizza] += cantidad
        else:
            dict_tipo_pizzas[tipo_pizza] = cantidad

        dict_tamaño_pizzas[tamaño_pizza] += cantidad

    nombres = {}

    for i in range(archivos[3].shape[0]):
        nombres[archivos[3].loc[i, 'pizza_type_id']
                ] = archivos[3].loc[i, 'name']

    diccionario_pizzas_n = {}

    for key in dict_tipo_pizzas:
        diccionario_pizzas_n[re.sub(
            r'The | Pizza', "", nombres[key])] = dict_tipo_pizzas[key]

    pal = sns.color_palette('Spectral', len(diccionario_pizzas_n))

    df_tipo = pd.DataFrame(diccionario_pizzas_n.items(), columns=[
        'Pizza', 'Cantidad'])

    grafico_tipo = sns.barplot(
        data=df_tipo, x='Cantidad', y='Pizza', palette=pal, order=df_tipo.sort_values('Cantidad', ascending=False).Pizza, orient='h')
    grafico_tipo.set_xticklabels(grafico_tipo.get_xticklabels())
    grafico_tipo.bar_label(
        grafico_tipo.containers[0], fontsize=9, rotation='horizontal', padding=3)
    grafico_tipo.spines['right'].set_visible(False)
    grafico_tipo.spines['top'].set_visible(False)

    plt.show()

    pal2 = sns.color_palette('viridis', len(dict_tamaño_pizzas))

    df_tamaño = pd.DataFrame(dict_tamaño_pizzas.items(), columns=[
        'Tamaño', 'Cantidad'])
    rank = df_tamaño['Cantidad'].argsort().argsort()

    grafico_tamaño = sns.barplot(
        data=df_tamaño, x='Tamaño', y='Cantidad', palette=np.array(pal2[::-1])[rank])
    grafico_tamaño.bar_label(grafico_tamaño.containers[0], fontsize=12)
    grafico_tamaño.spines['right'].set_visible(False)
    grafico_tamaño.spines['top'].set_visible(False)
    plt.show()

    return [grafico_tipo, grafico_tamaño]


def graficos_per_tiempo(archivos):

    dict_horas = {'00': 0, '01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0, '07': 0, '08': 0, '09': 0, '10': 0,
                  '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0, '23': 0}
    dict_meses = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0,
                  '06': 0, '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0}

    for i in range(len(archivos[2].index)):
        hora = archivos[2].loc[i, 'time'].split(':')[0]
        mes = archivos[2].loc[i, 'date'].split('/')[1]

        if hora in dict_horas:
            dict_horas[hora] += 1
        else:
            dict_horas[hora] = 1

        if mes in dict_meses:
            dict_meses[mes] += 1
        else:
            dict_meses[mes] = 1

    df_horas = pd.DataFrame(dict_horas.items(), columns=['Hora', 'Cantidad'])
    pal = sns.color_palette('Spectral', len(dict_horas))
    rank = df_horas['Cantidad'].argsort().argsort()
    grafico_horas = sns.barplot(
        data=df_horas, x='Hora', y='Cantidad', palette=np.array(pal[::-1])[rank])
    grafico_horas.bar_label(
        grafico_horas.containers[0], fontsize=8, rotation='vertical', padding=3)
    grafico_horas.spines['right'].set_visible(False)
    grafico_horas.spines['top'].set_visible(False)
    plt.show()

    df_meses = pd.DataFrame(dict_meses.items(), columns=['Mes', 'Cantidad'])
    pal2 = sns.color_palette('Spectral', int(df_meses['Cantidad'].max()/25))
    rank2 = df_meses['Cantidad'].argsort().argsort()
    grafico_meses = sns.barplot(
        data=df_meses, x='Mes', y='Cantidad', palette=np.array(pal2)[rank2])
    grafico_meses.bar_label(grafico_meses.containers[0], fontsize=8)
    grafico_meses.spines['right'].set_visible(False)
    grafico_meses.spines['top'].set_visible(False)
    plt.show()

    return [grafico_horas, grafico_meses]


def main():
    nombres = ['data_dictionary.csv', 'order_details_fixed.csv',
               'orders_fixed.csv', 'pizza_types.csv', 'pizzas.csv']

    archivos = extract(nombres)

    ingred = ingredientes()

    graficos_tiempo = graficos_per_tiempo(archivos)
    graficos_pizzas = graficos_per_pizzas(archivos)
    medidas_basicas = pedidos(archivos)
    dinero = round(dinero_ganado(archivos), 2)

    generarPDF(ingred, medidas_basicas, dinero)


if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    # Hay que tener en cuenta que limpieza datos tiene parte de aleatoriedad. Hay que tener
    # cuidado cada vez que se ejecuta porque las gráficas del PDF pueden cambiar
    # Esto también cambiará la prediccion de ingredientes.
    # Se va a guardar un csv con una limpieza que se tomará para guardar los datos que se usen en PDF y excel
    main()
    pass

'''
Se va a relalizar un reporte ejecutivo para Maven Pizzas con los datos de 2015.
Información que se va a mostrar:
 - Número de pedidos al año (media + max día) --..
 - Barplot con cada tipo de pizza y su cantidad de pedidos --
 - Gráfico con porcentaje de tamaño de pizza --
 - Dinero generado --
 - Tabla con ingredientes necesarios por semana (importar desde el otro doc) --
 - Horas de pedidos por día (rango de 1h) --
 - Gráfica con pedidos mensuales --
 - Gráfica ingredientes --
'''
