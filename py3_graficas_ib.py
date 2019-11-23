import os
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from copy import deepcopy
from datetime import datetime, date, time, timedelta

def read_input_data(file_weather, file_product, SAMPLE=False):
    """
    """
    df_wt = pd.read_csv(file_weather)
    df_prod = pd.read_csv(file_product)

    # Convierte Date de string a datetime en ambos dataframes.
    df_wt['orig_fecha'] = pd.to_datetime(df_wt['date'], format='%Y-%m-%d')
    df_prod['orig_fecha'] = pd.to_datetime(df_prod['fecha'], format='%Y-%m-%d')

    # Merge procut and weather into a single dataframe. The merge is based on the
    # 'orig_fecha', i.e., we append the corresponding weather information
    # to each row in the product dataframe.
    df = df_prod.merge(df_wt, left_on='orig_fecha', right_on='orig_fecha', how='left')

    # There might be some rows, were the weather information is missing, we
    # will drop these rows, since there will be no data to correlate.
    df = df.dropna(how='any', subset=['tavg', 'tmin', 'tmax'])

    # Drop rows without orders.
    df = df[(df['venta_total_piezas'] != 0)]

    # Split data into year, month, week and weekday.
    df['year'] = df['orig_fecha'].dt.year
    df['month'] = df['orig_fecha'].dt.month
    df['week'] = df['orig_fecha'].dt.week
    df['weekday'] = df['orig_fecha'].dt.dayofweek

    # Up to this point we should have a cleaned up dataframe, ready to work with.

    if SAMPLE:
        df = df.sample(1000)
        df.to_csv('test.csv', sep=';')

    return df

def main():
    """
    """

    file_weather = 'MXM00076680.csv'
    file_product = 'Producto_agencia_20139.csv'
    dir_out= r'Plots_Scatter_clima'
    if not os.path.exists(dir_out):
        # os.makedirs(os.path.dirname(dir_out))
        os.makedirs(dir_out)
    # Read input data.
    df_data = read_input_data(file_weather, file_product, False)

    # Lets see whats going on with each product regardless of route, agency, etc.
    groups = df_data.groupby(['codigo_producto'], axis='rows')
    # group = ['codigo_producto', 'codigo_ruta']
    # groups = df_data.groupby(group, axis='rows')
    for grp_id, grp in groups:
        print(grp_id)
        fig, ax = plt.subplots(ncols=3, figsize=(20, 7))
        ax[0].scatter(grp['orig_fecha'], grp['tavg'], alpha=0.2)
        ax[0].set_title('date vs tavg')

        ax[1].scatter(grp['tavg'], grp['venta_total_piezas'], alpha=0.2)
        ax[1].set_title('tavg vs venta_total_piezas')

        ax[2].scatter(grp['tavg'], grp['venta_total_piezas'], alpha=0.2)
        ax[2].set_title('tavg vs log(venta_total_piezas)')
        ax[2].set_yscale('log')
        plt.legend()
        ou_name = os.path.join(dir_out, 'prod_id_{}.png'.format(grp_id))
        plt.savefig(ou_name)
        plt.close('all')
        # plt.show()


        # print('\n\n')
        # exit(0)

if __name__ == '__main__':
    main()
