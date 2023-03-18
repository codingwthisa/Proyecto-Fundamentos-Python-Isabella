import pandas as pd
from sodapy import Socrata
import numpy as np

def get_data(departamento, municipio, cultivo, cantidad):
    # Validar que la cantidad ingresada no sea mayor a 2000
    if cantidad > 2000 and cantidad == 0:
        print("Error: la cantidad de registros ingresada debe ser menor o igual a 2000 y diferente de 0")
    else:
        client = Socrata("www.datos.gov.co", None)
        results = client.get("ch4u-f3i5", limit=cantidad)

        # Crear un DataFrame a partir de los resultados
        results_df = pd.DataFrame.from_records(results)

        # Filtrar el DataFrame para mostrar solo las filas que cumplen con los criterios de búsqueda
        filtered_df = results_df.loc[(results_df['departamento'] == departamento) &
                                 (results_df['municipio'] == municipio) &
                                 (results_df['cultivo'] == cultivo)][['departamento', 'municipio', 'cultivo', 'estado', 'topografia', 'ph_agua_suelo_2_5_1_0', 'f_sforo_p_bray_ii_mg_kg', 'potasio_k_intercambiable_cmol_kg']]

        filtered_df = filtered_df.rename(columns={
    'departamento':'Departamento',
    'municipio':'Municipio',
    'cultivo':'Cultivo',
    'estado': 'Estado',
    'tiempo_establecimiento':'Tiempo Establecimiento',
    'topografia': 'Topografia',
    'ph_agua_suelo_2_5_1_0':'pH agua:suelo 2,5:1,0',
    'f_sforo_p_bray_ii_mg_kg':'Fósforo (P) Bray II mg/kg',
    'potasio_k_intercambiable_cmol_kg':'Potasio (K) intercambiable cmol/kg'
    })
    
        # Verificar si hay filas en el DataFrame resultante
        if filtered_df.empty:
            return None

        # Eliminar los símbolos '<' y '>' de las columnas numéricas
        filtered_df.loc[:,'pH agua:suelo 2,5:1,0'] = filtered_df['pH agua:suelo 2,5:1,0'].str.replace('<', '').str.replace('>', '').str.replace(',', '.').astype(float)
        filtered_df.loc[:,'Fósforo (P) Bray II mg/kg'] = filtered_df['Fósforo (P) Bray II mg/kg'].str.replace('<', '').str.replace('>', '').str.replace(',', '.').astype(float)
        filtered_df.loc[:,'Potasio (K) intercambiable cmol/kg'] = filtered_df['Potasio (K) intercambiable cmol/kg'].str.replace('<', '').str.replace(',', '.').astype(float)

        # Calcular la mediana de las variables edáficas para cada fila del DataFrame filtrado
        mediana_pH = np.median(filtered_df['pH agua:suelo 2,5:1,0'])
        mediana_P = np.median(filtered_df['Fósforo (P) Bray II mg/kg'])
        mediana_K = np.median(filtered_df['Potasio (K) intercambiable cmol/kg'])

        # Mostrar todas las columnas del DataFrame filtrado
        pd.set_option('display.max_columns', None)
        # Imprimir el dataframe filtrado en el archivo de texto
   # Escribir los resultados en el archivo 'resultados.txt'
    with open('resultados.txt', 'w') as file:
        file.write(filtered_df.to_string())
        file.write(f"\nMediana pH: {mediana_pH:.2f}")
        file.write(f"\nMediana Fósforo (P) Bray II mg/kg: {mediana_P:.2f}")
        file.write(f"\nMediana Potasio (K) intercambiable cmol/kg: {mediana_K:.2f}")

    # Guardar el DataFrame filtrado en un archivo excel
    filtered_df.to_excel('resultado.xlsx', index=False)

    print(f"Se han guardado los resultados en el archivo 'resultados.txt' con éxito.")



    return filtered_df.to_string()
    