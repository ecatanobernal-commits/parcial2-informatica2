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

    def __str__(self):
        # info() NO devuelve texto: lo imprime y devuelve None.
        # Por eso le damos una "libreta" en memoria (StringIO) para que escriba ahí,
        # y luego sacamos ese texto con getvalue().
        libreta = io.StringIO()
        self.__tabla.info(buf=libreta)
        # to_string() muestra todas las columnas (si no, pandas las corta con "...")
        return f"""
========== ARCHIVO CSV: {self.__nombre} ==========
Ruta: {self.__ruta}

----- info() -----
{libreta.getvalue()}
----- describe() -----
{self.__tabla.describe().to_string()}
"""

    def graficar(self, condicion, canal, canal_x, canal_y):
        # Máscara: nos quedamos solo con las FILAS de la condición elegida
        datos = self.__tabla[self.__tabla["condition"] == condicion]

        # Figura (la "cartulina") con 3 paneles, como en la imagen del enunciado:
        #   add_subplot(2, 1, 1)      -> 2 filas, 1 columna: el panel de ARRIBA, ancho
        #   add_subplot(2, 3, (4, 5)) -> 2 filas, 3 columnas: ocupa las casillas 4 y 5 (abajo izquierda)
        #   add_subplot(2, 3, 6)      -> casilla 6 (abajo derecha)
        fig = plt.figure(figsize=(12, 8))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 3, (4, 5))
        ax3 = fig.add_subplot(2, 3, 6)

        # a) STEM: un palito por muestra. X = tiempo (el índice), altura = voltaje del canal
        ax1.stem(datos.index, datos[canal])
        ax1.axvline(0, color="black", label="t = 0 ms (estímulo)")   # línea vertical en 0 ms
        ax1.set_title(f"Stem del canal {canal} - condición {condicion}")
        ax1.set_xlabel("Tiempo (ms)")
        ax1.set_ylabel("Amplitud (µV)")
        ax1.legend()
        ax1.grid(True)

        # b) HISTOGRAMA del mismo canal: cuántas muestras caen en cada rango de µV
        ax2.hist(datos[canal], bins=30)
        ax2.set_title(f"Histograma del canal {canal}")
        ax2.set_xlabel("Amplitud (µV)")
        ax2.set_ylabel("Frecuencia")
        ax2.grid(True)

        # c) SCATTER de dos columnas: un punto por instante (valor de canal_x, valor de canal_y)
        ax3.scatter(datos[canal_x], datos[canal_y])
        ax3.set_title(f"{canal_x} vs {canal_y}")
        ax3.set_xlabel(f"{canal_x} (µV)")
        ax3.set_ylabel(f"{canal_y} (µV)")
        ax3.grid(True)

        fig.tight_layout()   # separa los paneles para que los textos no se encimen
        nombre_imagen = f"{self.__nombre}_condicion{condicion}_{canal}.png"
        fig.savefig(nombre_imagen)
        plt.show()
        return nombre_imagen
