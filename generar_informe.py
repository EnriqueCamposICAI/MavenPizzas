import pandas as pd


def generar_informe_datos(dataframes: list, nombres: list) -> str and list:
    informe = "INFORME DATASETS\n"
    conj_informes = {}
    for i in range(len(dataframes)):

        informe += f"\nArchivo -> {nombres[i]}\n\n"
        df_resumen = pd.DataFrame(
            index=["Type", "Size", "Unique", "Null", "NaN"], columns=dataframes[i].columns)

        for k in range(len(dataframes[i].columns)):
            df_resumen.loc["Type", dataframes[i].columns[k]
                           ] = dataframes[i][dataframes[i].columns[k]].dtype
            df_resumen.loc["Null", dataframes[i].columns[k]
                           ] = dataframes[i][dataframes[i].columns[k]].isnull().sum()
            df_resumen.loc["NaN", dataframes[i].columns[k]
                           ] = dataframes[i][dataframes[i].columns[k]].isna().sum()
            df_resumen.loc["Unique", dataframes[i].columns[k]
                           ] = dataframes[i][dataframes[i].columns[k]].nunique()
            df_resumen.loc["Size", dataframes[i].columns[k]
                           ] = dataframes[i][dataframes[i].columns[k]].size
        informe += df_resumen.to_string() + "\n\n"

        conj_informes[nombres[i]] = df_resumen

    return informe, conj_informes


if __name__ == "__main__":

    pass
