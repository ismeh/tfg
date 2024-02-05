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



if __name__ == "__main__":
    ruta_datos = constantes.DATA_DIR + constantes.LOCAL_DATA
    os.chdir(ruta_datos)
    data_local = procesamiento_datos.juntar_datos(".")

    grafica_umbral_tiempo_respuesta(data_local)
