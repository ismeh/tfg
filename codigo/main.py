# -*- coding: utf-8 -*-
import procesamiento_datos
import constantes
import pandas as pd
import numpy as np
import os

"""Primera entrega"""
def grafica_umbral_tiempo_respuesta(data):
    lista_ms = np.array([300, 400, 500, 600, 700, 800, 900])
    data['diff_time'] = (pd.to_datetime(data['Tiempo de la pulsación'])
                         -
                         pd.to_datetime(data['Tiempo de aparición de la letra observada']))
    balance_tiempos = procesamiento_datos.balance_tiempo_respuesta(lista_ms, data)
    procesamiento_datos.grafica_barras(balance_tiempos, "Balance de tiempos de respuesta", lista_ms)

def grafica_balance_pulsaciones(data):
    num_respuestas = len(data)
    num_pulsaciones_izq = data['Tecla elegida'].where(data['Tecla elegida'] == 'q').count()
    num_pulsaciones_dch = num_respuestas-num_pulsaciones_izq

    procesamiento_datos.grafica_barras([[num_pulsaciones_izq], [num_pulsaciones_dch]],
                                       "Balance de pulsaciones", [''],
                                       ['Izquierda', 'Derecha'], 'upper left')



if __name__ == "__main__":
    ruta_datos = constantes.DATA_DIR + constantes.LOCAL_DATA
    os.chdir(ruta_datos)
    local_data = procesamiento_datos.juntar_datos(".")

    # grafica_umbral_tiempo_respuesta(local_data)
    # grafica_balance_pulsaciones(local_data)

    local_data.sort_values(by=['ID del participante', 'Trial', 'Respuesta'], inplace=True)
    local_data.set_index(np.arange(local_data.shape[0]), inplace=True)
    
    # print(local_data)

    #ñadir tiempo de respuesta
    local_data['diff_ti_tp'] = pd.to_datetime(local_data['Tiempo de la pulsación']) - pd.to_datetime(local_data['Tiempo de inicio'])
    local_data['diff_ta_tp'] = pd.to_datetime(local_data['Tiempo de la pulsación']) - pd.to_datetime(local_data['Tiempo de aparición de la letra observada'])

    # print(local_data)

    #Imprimir nombre de archivos
    os.chdir("../" + constantes.DATA_DIR + constantes.MUSE_DATA)

    archivos_muse = os.listdir()
    #alfabetic sorting
    # archivos_muse.sort()
    # print(archivos_muse)
    muse_data = procesamiento_datos.leer_datos(archivos_muse[0])
    print(muse_data.shape)
    print(muse_data.columns)
    print(muse_data.head())
    print(muse_data[0,10])

    # Comprobar tasa de muestreo (muse_data)

#%%
