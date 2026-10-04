import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio


# ==========================================================
# FUNCIONES DE VALIDACIÓN
# ==========================================================
def validar_entero(mensaje, minimo, maximo):
    # Repite la pregunta hasta que el usuario escriba un entero dentro del rango
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo and valor <= maximo:
                return valor
            print(f"El número debe estar entre {minimo} y {maximo}")
        except ValueError:
            # int("hola") produce ValueError: lo atrapamos para que el programa no se caiga
            print("Debe ingresar un número entero")


def validar_opcion(mensaje, opciones):
    # Repite la pregunta hasta que el usuario escriba uno de los textos de la lista
    while True:
        texto = input(mensaje)
        if texto in opciones:
            return texto
        print("Opción no válida. Opciones:", opciones)


# ==========================================================
# CLASE PARA LOS ARCHIVOS CSV
# ==========================================================
class ArchivoCSV:
    def __init__(self, nombre, ruta):
        self.__nombre = nombre
        self.__ruta = ruta
        self.__tabla = pd.read_csv(ruta)
        # set_index devuelve una tabla NUEVA, por eso se vuelve a guardar en self.__tabla.
        # Desde aquí 'time_ms' ya no es columna: es el índice de las filas.
        self.__tabla = self.__tabla.set_index("time_ms")

    def verNombre(self):
        return self.__nombre

    def verRuta(self):
        return self.__ruta

    def verTabla(self):
        return self.__tabla

    def verColumnas(self):
        return list(self.__tabla.columns)
