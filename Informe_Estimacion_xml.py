import lxml.etree as et
import pandas as pd
import Ingredient_Prediction as ip
import generar_informe as inf


def extract_data():
    # Hay que sacar la recomendacion de ingredientes
    nombres = ['data_dictionary.csv', 'order_details.csv',
               'orders.csv', 'pizza_types.csv', 'pizzas.csv']
    archivos = []
    for i in range(len(nombres)):
        archivos.append(pd.read_csv(
            f"Datasets_pizza/{nombres[i]}", encoding="utf-8"))

    datos_finales = pd.read_csv(
        'Datasets_pizza/Prediccion_ingredientes_Final_2015.csv', encoding='utf-8')

    # Se sacan los informes de cada DataFrame
    informe, informes = inf.generar_informe_datos(archivos, nombres)

    return datos_finales, informes


def xml_estimacion(datos_finales):
    ingredientes = datos_finales[datos_finales.columns[0]]
    root = et.Element("Data")
    root.attrib[
        "Título"] = "Estimacion de ingredientes semanales para Maven Pizzas (2015)"

    for i in range(len(datos_finales["Recomendado"])):
        ingrediente = et.SubElement(root, "Ingrediente")
        ingrediente.attrib["Nombre"] = ingredientes[i]
        ingrediente.attrib["Cantidad"] = str(datos_finales["Recomendado"][i])

    tree = et.ElementTree(root)

    with open("Estimacion_Ingredientes.xml", "wb") as file:
        tree.write(file,
                   xml_declaration=True, pretty_print=True, encoding="utf-8")

    print("Acabado xml estimacion ingredientes")
    pass


def xml_informe(informes):

    root = et.Element("Información")
    root.attrib["Título"] = "Informes de los DataFrames de Maven Pizzas"

    for i in informes.keys():
        df = et.SubElement(root, "DataFrame")
        df.attrib["Nombre"] = i

        for j in informes[i].columns:
            columna = et.SubElement(df, "Columna")
            columna.attrib["Columna"] = j
            for k in informes[i].index:
                atributo = et.SubElement(columna, "Atributo")
                atributo.attrib[k] = str(informes[i][j][k])

    tree = et.ElementTree(root)

    with open("Informe_Datasets.xml", "wb") as file:
        tree.write(file,
                   xml_declaration=True, pretty_print=True, encoding="utf-8")

    print("Acabado xml informes")
    pass


def main():
    datos_finales, informes = extract_data()

    xml_estimacion(datos_finales)
    xml_informe(informes)
    pass


if __name__ == "__main__":
    main()
