# -*- coding: utf-8 -*-
import procesamiento_datos
import constantes
import pandas as pd
import numpy as np
import os

"""Primera entrega"""
def grafica_umbral_tiempo_respuesta(data):
    lista_ms = np.array([300, 400, 500, 600, 700, 800, 900])
    data['diff_time'] = pd.to_datetime(data['Tiempo de la pulsación']) - pd.to_datetime(
        data['Tiempo de aparición de la letra observada'])
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
    data_local = procesamiento_datos.juntar_datos(".")

    # grafica_umbral_tiempo_respuesta(data_local)
    # grafica_balance_pulsaciones(data_local)
    print(data_local)
    print(np.arange(data_local.shape[0]))
    data_local.sort_values(by=['ID del participante', 'Trial', 'Respuesta'], inplace=True)
    data_local.set_index(np.arange(data_local.shape[0]), inplace=True)
    # print(data_local)
