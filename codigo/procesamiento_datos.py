# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

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

"""Función para extraer los datos en función del tamaño de la ventana temporal.
   Dado una ruta de archivo extraemos datos de cada respuesta, para ello utilizamos los tiempos de pulsación como punto 
   final y retrocedemos tantos segundos como indique el tamaño de la ventana temporal.
   
    Devuelve un dataframe con los datos extraidos.
   """

"""

"""
def extraer_ventana(muse_data, time_stamp, ms_prev, ms_post):
    tiempo_inicio = time_stamp - pd.Timedelta(milliseconds=ms_prev)
    tiempo_fin = time_stamp + pd.Timedelta(milliseconds=ms_post)

    ventana = muse_data[(muse_data['TimeStamp'] >= tiempo_inicio) & (muse_data['TimeStamp'] <= tiempo_fin)]

    return ventana

"""pre: Nos encontramos en el directorio de los datos de Muse"""
def balance_clases(ruta_datos):
    os.chdir("../Local")
    archivos_local = os.listdir()
    
    #Inicializar listas para almacenar los nombres de los ficheros y sus porcentajes
    porcentajes_clase_0 = []
    porcentajes_clase_1 = []
    total = []

    # Iterar sobre los archivos y contar las clases
    for archivo in archivos_local:
        # Leer el archivo CSV
        df = leer_datos(archivo)

        #Totales
        total_clase_0 = (df['Tecla elegida'] == 'p').sum()
        total_clase_1 = (df['Tecla elegida'] == 'q').sum()
        total_ocurrencias = total_clase_0 + total_clase_1

        # Calcular porcentajes
        porcentaje_clase_0 = (total_clase_0 / total_ocurrencias) * 100
        porcentaje_clase_1 = (total_clase_1 / total_ocurrencias) * 100

        porcentajes_clase_0.append(porcentaje_clase_0)
        porcentajes_clase_1.append(porcentaje_clase_1)
        total.append(total_ocurrencias)
        
    for idx, archivo in enumerate(archivos_local):
        archivos_local[idx] = re.search(r'\d+', archivo).group() 
        
    # Crear barras para Clase 0 y Clase 1
    x = range(len(archivos_local))  # Posiciones para el eje x
    bar_width = 0.4  # Ancho de las barras
    plt.figure(figsize=(12, 6))
    
    bars1 = plt.bar(x, porcentajes_clase_0, width=bar_width, label='Clase 0', color='blue', align='center')
    bars2 = plt.bar([p + bar_width for p in x], porcentajes_clase_1, width=bar_width, label='Clase 1', color='orange', align='center')

    # Añadir el total de respuestas entre las dos barras
    for i in range(len(archivos_local)):
        # Determinar el color del texto basado en los porcentajes
        color_texto = 'red' if porcentajes_clase_0[i] > 60 or porcentajes_clase_1[i] > 60 else 'black'
        
        plt.text(i + 0.2, max(porcentajes_clase_0[i], porcentajes_clase_1[i]) + 5,
                 f'{total[i]}', ha='center', va='bottom', color=color_texto)
        
    # Añadir porcentajes encima de las barras
    for bar in bars1:
        yval = int(bar.get_height())
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.0f}", ha='center', va='bottom', color='blue')
    
    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.0f}", ha='center', va='bottom', color='orange')

    # Dibujar las líneas de umbral
    plt.axhline(y=50, color='black', linestyle='--', label='Umbral 50%', alpha = 0.5)
    plt.axhline(y=60, color='red', linestyle='--', label='Umbral 60%', alpha = 0.5)

    # Añadir etiquetas y título
    plt.xticks([p + 0.2 for p in x], archivos_local, rotation=0, ha='center')
    plt.ylabel('Porcentaje (%)')
    plt.xlabel('Archivo')
    plt.title('Porcentaje de ocurrencias de Clase 0 y Clase 1 en cada fichero CSV')
    plt.ylim(0, 100)
    plt.grid(axis='y')
    
    # Añadir leyenda
    plt.legend()
    
    # Mostrar la gráfica
    plt.tight_layout()
    plt.show()
    # # Calcular los porcentajes
    # porcentaje_clase_0 = (total_clase_0 / total_observaciones) * 100
    # porcentaje_clase_1 = (total_clase_1 / total_observaciones) * 100

    # # Crear un DataFrame para las clases y los porcentajes
    # df_balance = pd.DataFrame({
    #     'Clase': ['Clase 0', 'Clase 1'],
    #     'Respuestas': [total_clase_0, total_clase_1],
    #     'Porcentaje': [porcentaje_clase_0, porcentaje_clase_1]
    # })

    # # Visualizar el balance de clases
    # fig, ax = plt.subplots()

    # # Crear gráfico de barras para el número de respuestas
    # df_balance.plot(kind='bar', x='Clase', y='Respuestas', ax=ax, color='skyblue', legend=False)

    # # Añadir los porcentajes encima de las barras
    # for i, (respuestas, porcentaje) in enumerate(zip(df_balance['Respuestas'], df_balance['Porcentaje'])):
    #     ax.text(i, respuestas + 50, f'{porcentaje:.2f}%', ha='center', fontsize=12)

    # # Título y etiquetas
    # plt.title('Balance de Clases: Número de Respuestas y Porcentajes')
    # plt.ylabel('Número de Respuestas')
    # plt.xlabel('Clases')
    # plt.xticks(rotation=0)

    # # Mostrar el gráfico
    # plt.show()
    os.chdir("../Muse")



    
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