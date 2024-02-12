# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#Opciones de panda
pd.options.display.width = 0 #Display en función del tamaño de la pantalla
pd.set_option('display.max_rows', None) #Mostrar todas las filas

"""Función para leer los datos de un archivo csv"""
def leer_datos(archivo) -> pd.DataFrame:
    # Leer datos de un archivo csv, infer para que lea el header
    datos = pd.read_csv(archivo, header='infer')
    return datos

"""Junta todos los csv del directorio indicado en un dataframe"""
def juntar_datos(directorio) -> pd.DataFrame:
    datos = pd.DataFrame()
    archivos = os.listdir(directorio)
    for archivo in archivos:
        datos = pd.concat([datos, leer_datos(archivo)])
    return datos

"""
Devuelve una lista de tuplas con el número de respuestas lentas y rápidas
Si ['aparición de letra'] - ['pulsación'] > ms, se considera lento
    True -> Lentos
    False -> Rápidos
"""
def balance_tiempo_respuesta(lista_ms, datos):
    num_datos = len(datos)
    result = []
    lentos = []
    rapidos = []
    for ms in lista_ms:
        mask_lentos = datos['diff_time'] > pd.Timedelta(milliseconds=ms)
        num_lentos = mask_lentos.where(mask_lentos == True).count()
        # print(ms, mask_lentos.value_counts(), mask_lentos)
        # print(mask_lentos.value_counts())
        num_rapidos = num_datos - num_lentos
        lentos.append(num_lentos)
        rapidos.append(num_rapidos)

    # print(lista_ms)
    result.append(lentos)
    result.append(rapidos)
    return result

def grafica_barras(datos, titulo, etiquetas, atributos=('Lentas', 'Rápidas'), loc='upper center'):
    fig, ax = plt.subplots(layout='constrained')
    bar_color = ['b', 'r']

    x = np.arange(len(etiquetas)) # Posicion etiquetas
    ancho_barras = 0.25

    for idx, arr in enumerate(datos):
        offset = ancho_barras*idx
        barras = ax.bar(x=x+offset, height=arr, width=ancho_barras, label=atributos[idx], color=bar_color[idx])
        ax.bar_label(barras, padding=1)


    ax.set_xticks(x+ancho_barras/2, etiquetas) #Añadir etiquetas
    ax.set_title(titulo) #Titulo
    ax.set_xlabel('Umbral de tiempo de respuesta (ms)') #Etiqueta eje x
    ax.set_ylabel('Número de respuestas') #Etiqueta eje y
    ax.legend(loc=loc, ncols=3)
    plt.show()

# def grafica_barras_tr(datos, titulo, etiquetas, atributos=('Lentas', 'Rápidas')):
#     fig, ax = plt.subplots(layout='constrained')
#     bar_color = ['b', 'r']
#
#     x = np.arange(len(etiquetas))  # Posicion etiquetas
#     ancho_barras = 0.25
#
#     barras = ax.bar(x=x - ancho_barras / 2, height=datos[0], width=ancho_barras, label=atributos[0],color=bar_color[0])
#     ax.bar_label(barras, padding=1)
#     barras = ax.bar(x=x + ancho_barras / 2, height=datos[1], width=ancho_barras, label=atributos[1],color=bar_color[1])
#     ax.bar_label(barras, padding=1)
#
#     ax.set_xticks(x, etiquetas)  # Añadir etiquetas
#     ax.set_title(titulo)  # Titulo
#     ax.set_xlabel('Umbral de tiempo de respuesta (ms)')  # Etiqueta eje x
#     ax.set_ylabel('Número de respuestas')  # Etiqueta eje y
#     ax.legend(loc='upper center', ncols=3)
#     plt.show()