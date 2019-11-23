import os
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from copy import deepcopy
from datetime import datetime, date, time, timedelta

def read_input_data(file_weather, file_product, file_location, SAMPLE=False):
    """
    """
    df_wt = pd.read_csv(file_weather)
    df_prod = pd.read_csv(file_product)
    df_loc = pd.read_csv(file_location)

    res = []

    # Convierte Date de string a datetime en ambos dataframes.
    df_wt['orig_fecha'] = pd.to_datetime(df_wt['date'], format='%Y-%m-%d')
    df_prod['orig_fecha'] = pd.to_datetime(df_prod['fecha'], format='%Y-%m-%d')

    # Merge procut and weather into a single dataframe. The merge is based on the
    # 'orig_fecha', i.e., we append the corresponding weather information
    # to each row in the product dataframe.
    df_wtprod = df_prod.merge(df_wt, left_on='orig_fecha', right_on='orig_fecha', how='left')
    df = df_wtprod.merge(df_loc, left_on='codigo_ruta', right_on='ID_RUTA', how='left')

    # There might be some rows, were the weather information is missing, we
    # will drop these rows, since there will be no data to correlate.
    df = df.dropna(how='any', subset=['tavg', 'tmin', 'tmax'])

    # Drop rows without orders.
    df = df[(df['venta_total_piezas'] >= 0)]

    # Split data into year, month, week and weekday.
    df['year'] = df['orig_fecha'].dt.year
    df['month'] = df['orig_fecha'].dt.month
    df['week'] = df['orig_fecha'].dt.week
    df['weekday'] = df['orig_fecha'].dt.dayofweek
    print(df.info())

    # # Up to this point we should have a cleaned up dataframe, ready to work with.
    # res.append([fecha, codigo_agencia, codigo_ruta, dia, codigo_producto, venta_total_piezas, storeday, id, date, prcp, tmin, tmax, tavg])
    # columns = ['fecha', 'codigo_agencia', 'codigo_ruta', 'codigo_producto' ,'venta_total_piezas', 'storeday', 'id', 'date', 'prcp', 'tmin', 'tmax', 'tavg']
    # df_res = pd.DataFrame(res, columns=columns)
    df.to_csv('test.csv', sep=';')



def main():
    """
    """

    file_weather = 'MXM00076680.csv'
    file_product = 'Producto_agencia_20139.csv'
    file_location = 'HHc_Clientes-20139.csv'
    dir_out= r'clima-venta'
    # if not os.path.exists(dir_out):
    #     # os.makedirs(os.path.dirname(dir_out))
    #     os.makedirs(dir_out)
    # # Read input data.
    df_data = read_input_data(file_weather, file_product, file_location, False)

    # Lets see whats going on with each product regardless of route, agency, etc.
    # groups = df_data.groupby(['codigo_producto'], axis='rows')
    # # group = ['codigo_producto', 'codigo_ruta']
    # # groups = df_data.groupby(group, axis='rows')


        # print('\n\n')
        # exit(0)

if __name__ == '__main__':
    main()
