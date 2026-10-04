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
