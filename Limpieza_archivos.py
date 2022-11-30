import pandas as pd
from word2number import w2n
import dateutil.parser
import datetime
import re
import numpy as np
import random
import generar_informe as inf


def extract(nombres):
    # SE SACAN LOS DATAFRAMES
    archivos = []
    for i in range(len(nombres)):

        nombre = 'Datasets_pizza_mod/' + nombres[i]
        if i in [0, 1]:
            archivos.append(pd.read_csv(nombre, encoding='utf-8', sep=';'))
        else:
            archivos.append(pd.read_csv(nombre, encoding='utf-8'))

    return archivos


def transfrom_orders(df):
    '''
    Vamos a crear una nueva columna con la fecha + tiempo
    Depende de si hay date en la de la izquierda o no, se incluye

    1. Mirar que no haya nulos en date -> en time la hora estará en 'date'

    2. En los valores de unix les falta una hora y se quedan con la hora de 'time'

    3. El resto se comprueba donde hay una hora fiable (no 00:00:00) -> miramos 'time'
       Si time no es fiable, la hora es la de 'date'

    4. fill na con los valores de alrededor
    '''

    df.sort_values(by=['order_id'], inplace=True)
    indice = df.index

    for i in range(len(indice)):
        fila = df.loc[indice[i]]

        if (str(fila['time']) != 'nan') and dateutil.parser.parse(re.sub(' AM| PM', '', str(df.loc[indice[i], 'time']))).strftime('%H:%M:%S') == '00:00:00':
            fila['time'] = (np.nan)
        if str(fila['date']) != 'nan':
            fecha = fila['date']

            try:
                fecha = float(fecha)
                unix = True
            except ValueError:
                fecha = str(fecha)
                unix = False

            if unix:
                fecha_n = datetime.datetime.fromtimestamp(fecha)

                if str(fila['time']) != 'nan':

                    time = dateutil.parser.parse(
                        re.sub(' AM| PM', '', fila['time'])).time()
                    fecha_n += datetime.timedelta(hours=time.hour,
                                                  minutes=time.minute, seconds=time.second)
                else:
                    # Hay que mirar que date no te da una hora -> mirar que hora da date
                    # Si da 00:00:00, la hora es la del anterior
                    if fecha_n.time() == datetime.time(0, 0, 0):
                        time_anterior = dateutil.parser.parse(
                            re.sub(' AM| PM', '', str(df.loc[indice[i-1], 'time']))).time()
                        fecha_n += datetime.timedelta(hours=time_anterior.hour,
                                                      minutes=time_anterior.minute, seconds=time_anterior.second)
                df.loc[indice[i], 'date'] = fecha_n.date().strftime('%d/%m/%Y')

                df.loc[indice[i], 'time'] = fecha_n.time()
            else:
                if fila['date'].find('-') == 4:
                    fecha_n = dateutil.parser.parse(
                        fila['date'], yearfirst=True)
                elif fila['date'].find('-') == 2:
                    fecha_n = dateutil.parser.parse(
                        fila['date'], dayfirst=True)
                else:
                    fecha_n = dateutil.parser.parse(fila['date'])
                # Vamos a mirar si hay que ver si es con el año antes ->
                if str(fila['time']) != 'nan':
                    time = dateutil.parser.parse(
                        re.sub(' AM| PM', '', fila['time'])).time()
                    fecha_n += datetime.timedelta(hours=time.hour,
                                                  minutes=time.minute, seconds=time.second)
                else:
                    if fecha_n.time() == datetime.time(0, 0, 0):
                        time_anterior = dateutil.parser.parse(
                            re.sub(' AM| PM', '', str(df.loc[indice[i-1], 'time']))).time()
                        fecha_n += datetime.timedelta(hours=time_anterior.hour,
                                                      minutes=time_anterior.minute, seconds=time_anterior.second)
                df.loc[indice[i], 'date'] = fecha_n.date().strftime('%d/%m/%Y')
                if fecha_n.date().year == 2017:
                    print(i, fecha_n.date())
                df.loc[indice[i], 'time'] = fecha_n.time()
        else:
            if str(fila['time']) != 'nan':
                df.loc[indice[i], 'time'] = dateutil.parser.parse(
                    re.sub(' AM| PM', '', fila['time'])).time()
            else:
                time_anterior = dateutil.parser.parse(
                    re.sub(' AM| PM', '', str(df.loc[indice[i-1], 'time']))).time()
                df.loc[indice[i], 'time'] = time_anterior

    # Ahora se van a cambiar los nan -> backfill con date y time (salvo time not nan)

    df['date'].fillna(method='ffill', inplace=True)
    df['time'].fillna(method='ffill', inplace=True)

    count = 0
    '''
    for i in range(len(indice) - 1):

        fecha1 = df.loc[indice[i], 'date']
        hora1 = df.loc[indice[i], 'time']
        total1 = fecha1 + datetime.timedelta(hours=hora1.hour,
                                             minutes=hora1.minute, seconds=hora1.second)
        fecha2 = df.loc[indice[i+1], 'date']
        hora2 = df.loc[indice[i+1], 'time']
        total2 = fecha2 + datetime.timedelta(hours=hora2.hour,
                                             minutes=hora2.minute, seconds=hora2.second)

        if total1 > total2:
            count += 1

    if count != 0:
        print('Ha habido {} errores'.format(count))
    '''
    df.to_csv('Datasets_pizza_mod/orders_fixed.csv', index=False)
    print('Se ha arreglado orders_mod.csv')
    pass


def transform_order_details(df, pizzas):

    # Se va a rellenar el tipo de pizza con una aleatoria (si hay más en ese pedido, no se puede repetir)
    # Primero se la cantidad
    df.sort_values(by=['order_details_id'], inplace=True)
    indice = df.index

    for i in range(len(indice)):
        fila = df.loc[indice[i]]

        # Pasamos los nan a 1 porque es el valor que más se repite

        if str(fila['quantity']) == 'nan':
            df.loc[indice[i], 'quantity'] = 1
        else:
            try:
                df.loc[indice[i], 'quantity'] = abs(int(fila['quantity']))
            except ValueError:
                df.loc[indice[i], 'quantity'] = w2n.word_to_num(
                    str(fila['quantity']))

        # Ahora vamos a arreglar la pizza pedida
        # Si es null, se asigna una aleatoria (siempre y cuando no esté repetida en el pedido)

        if str(fila['pizza_id']) != 'nan':
            # Vamos a limpiar con regex

            '''
            Tipos:
                - Sub - por _
                - Sub '' por _
                - Sub @ por a
                - Sub 3 por e
                - Sub 0 por o
            '''

            pizza = re.sub('-', '_', fila['pizza_id'])
            pizza = re.sub(' ', '_', pizza)
            pizza = re.sub('@', 'a', pizza)
            pizza = re.sub('3', 'e', pizza)
            pizza = re.sub('0', 'o', pizza)

            if pizza not in pizzas:
                print('ERROR')

            df.loc[indice[i], 'pizza_id'] = pizza
            # Comprobamos que todas están en la lista de pizzas

    for k in range(len(indice)):
        if str(df.loc[indice[k], 'pizza_id']) == 'nan':
            # Habría que mirar que la pizza no está ya en el pedido
            pedido = (df[df['order_id'] == fila['order_id']].dropna())
            pedido = pedido['pizza_id'].unique().tolist()

            for pizza in pedido:
                pizzas.remove(pizza)

            if len(pizzas) != 0:
                pizzaf = random.choice(pizzas)

            df.loc[indice[k], 'pizza_id'] = pizzaf

            for pizza in pedido:
                pizzas.append(pizza)

    df.to_csv('Datasets_pizza_mod/order_details_fixed.csv', index=False)
    print('Se ha arreglado order_details_mod.csv')


def lista_pizzas():
    df = pd.read_csv('Datasets_pizza_fixed/pizzas.csv', encoding='utf-8')
    lista_pizzas = list(df['pizza_id'].unique())
    return lista_pizzas


def main(nombres):

    archivos = extract(nombres)
    string, datsets = inf.generar_informe_datos(archivos, nombres)
    with open('informe_datos_2016.txt', 'w') as f:
        f.write(string)
    archivos[1] = transfrom_orders(archivos[1])
    pizzas = lista_pizzas()
    archivos[0] = transform_order_details(
        archivos[0], pizzas)


if __name__ == "__main__":
    pd.options.mode.chained_assignment = None
    nombres = ['order_details_mod.csv', 'orders_mod.csv']
    main(nombres)

    pass
