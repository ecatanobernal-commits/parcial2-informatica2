import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio


def validar_entero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo and valor <= maximo:
                return valor
            print(f"El número debe estar entre {minimo} y {maximo}")
        except ValueError:
            print("Debe ingresar un número entero")


def validar_opcion(mensaje, opciones):
    while True:
        texto = input(mensaje)
        if texto in opciones:
            return texto
        print("Opción no válida. Opciones:", opciones)


class ArchivoCSV:
    def __init__(self, nombre, ruta):
        self.__nombre = nombre
        self.__ruta = ruta
        self.__tabla = pd.read_csv(ruta)
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
        libreta = io.StringIO()
        self.__tabla.info(buf=libreta)
        return f"""
========== ARCHIVO CSV: {self.__nombre} ==========
Ruta: {self.__ruta}

----- info() -----
{libreta.getvalue()}
----- describe() -----
{self.__tabla.describe().to_string()}
"""

    def graficar(self, condicion, canal, canal_x, canal_y):
        datos = self.__tabla[self.__tabla["condition"] == condicion]

        fig = plt.figure(figsize=(12, 8))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 3, (4, 5))
        ax3 = fig.add_subplot(2, 3, 6)

        ax1.stem(datos.index, datos[canal])
        ax1.axvline(0, color="black", label="t = 0 ms (estímulo)")
        ax1.set_title(f"Stem del canal {canal} - condición {condicion}")
        ax1.set_xlabel("Tiempo (ms)")
        ax1.set_ylabel("Amplitud (µV)")
        ax1.legend()
        ax1.grid(True)

        ax2.hist(datos[canal], bins=30)
        ax2.set_title(f"Histograma del canal {canal}")
        ax2.set_xlabel("Amplitud (µV)")
        ax2.set_ylabel("Frecuencia")
        ax2.grid(True)

        ax3.scatter(datos[canal_x], datos[canal_y])
        ax3.set_title(f"{canal_x} vs {canal_y}")
        ax3.set_xlabel(f"{canal_x} (µV)")
        ax3.set_ylabel(f"{canal_y} (µV)")
        ax3.grid(True)

        fig.tight_layout()
        nombre_imagen = f"{self.__nombre}_condicion{condicion}_{canal}.png"
        fig.savefig(nombre_imagen)
        plt.show()
        return nombre_imagen

    def diferencia_interhemisferica(self, canal_izq, canal_der):
        nueva = canal_izq + "-" + canal_der
        self.__tabla[nueva] = self.__tabla[canal_izq] - self.__tabla[canal_der]
        return nueva

    def promedio_por_condicion(self, columna):
        return self.__tabla.groupby("condition")[columna].mean()


def sumar(a, b):
    return a + b


def restar(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


class ArchivoMAT:
    def __init__(self, nombre, ruta, fs=250):
        self.__nombre = nombre
        self.__ruta = ruta
        self.__fs = fs
        self.__variables = sio.whosmat(ruta)
        dicc = sio.loadmat(ruta)
        llave = self.__variables[0][0]
        self.__matriz = dicc[llave]

    def verNombre(self):
        return self.__nombre

    def verRuta(self):
        return self.__ruta

    def verFs(self):
        return self.__fs

    def verForma(self):
        return self.__matriz.shape

    def __str__(self):
        texto = f"\n========== ARCHIVO MAT: {self.__nombre} ==========\n"
        texto += f"Ruta: {self.__ruta}\n\n"
        texto += "Variable\tDimensiones\t\tTipo\n"
        texto += "--------------------------------------------\n"
        for variable in self.__variables:
            texto += f"{variable[0]}\t\t{variable[1]}\t\t{variable[2]}\n"
        canales, puntos, epocas = self.__matriz.shape
        texto += f"""
Eje 0: {canales} canales
Eje 1: {puntos} puntos por época ({puntos / self.__fs} s a {self.__fs} Hz)
Eje 2: {epocas} épocas
Tipo de dato en NumPy: {self.__matriz.dtype} (en MATLAB se llama 'single')
"""
        return texto

    def matriz2D(self):
        canales, puntos, epocas = self.__matriz.shape
        return np.reshape(self.__matriz, (canales, puntos * epocas), order="F")

    def operar(self, funcion, canales, pmin, pmax):
        matriz = self.matriz2D()
        tiempo = np.arange(pmin, pmax) / self.__fs

        resultado = matriz[canales[0], pmin:pmax]
        for c in canales[1:]:
            resultado = funcion(resultado, matriz[c, pmin:pmax])

        if funcion == multiplicar:
            unidad = "µV⁴"
        else:
            unidad = "µV"

        fig = plt.figure(figsize=(12, 8))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        for c in canales:
            ax1.plot(tiempo, matriz[c, pmin:pmax], label=f"Canal {c}")
        ax1.set_title(f"Canales {canales} - puntos {pmin} a {pmax}")
        ax1.set_xlabel("Tiempo (s)")
        ax1.set_ylabel("Amplitud (µV)")
        ax1.legend()
        ax1.grid(True)

        ax2.plot(tiempo, resultado, color="black", label=f"Resultado de {funcion.__name__}")
        ax2.set_title(f"Resultado de {funcion.__name__} de los canales {canales}")
        ax2.set_xlabel("Tiempo (s)")
        ax2.set_ylabel(f"Amplitud ({unidad})")
        ax2.legend()
        ax2.grid(True)

        fig.tight_layout()
        nombre_imagen = f"{self.__nombre}_{funcion.__name__}_{pmin}-{pmax}.png"
        fig.savefig(nombre_imagen)
        plt.show()
        return nombre_imagen

    def promedio_desviacion(self, eje1, eje2):
        promedio = np.mean(self.__matriz, axis=(eje1, eje2))
        desviacion = np.std(self.__matriz, axis=(eje1, eje2))
        print("Forma original de la matriz:", self.__matriz.shape)
        print("Forma final del promedio:", promedio.shape)
        print("Forma final de la desviación:", desviacion.shape)

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(1, 1, 1)
        ax.boxplot([promedio, desviacion])
        ax.set_xticklabels(["Promedio", "Desviación estándar"])
        ax.set_title(f"{self.__nombre}: promedio y desviación sobre los ejes {eje1} y {eje2}")
        ax.set_xlabel("Medida")
        ax.set_ylabel("Amplitud (µV)")
        ax.grid(True)

        nombre_imagen = f"{self.__nombre}_boxplot_ejes{eje1}{eje2}.png"
        fig.savefig(nombre_imagen)
        plt.show()
        return promedio.shape


class Sistema:
    def __init__(self):
        self.__csv = {}
        self.__mat = {}

    def ingresarCSV(self, archivo):
        self.__csv[archivo.verNombre()] = archivo

    def ingresarMAT(self, archivo):
        self.__mat[archivo.verNombre()] = archivo

    def verCSV(self, nombre):
        return self.__csv.get(nombre, False)

    def verMAT(self, nombre):
        return self.__mat.get(nombre, False)

    def verNombresCSV(self):
        return list(self.__csv.keys())

    def verNombresMAT(self):
        return list(self.__mat.keys())

    def existe(self, nombre):
        return nombre in self.__csv or nombre in self.__mat

    def buscar(self, texto):
        encontrados = []
        for nombre in self.__csv:
            if texto.lower() in nombre.lower():
                encontrados.append("CSV: " + nombre)
        for nombre in self.__mat:
            if texto.lower() in nombre.lower():
                encontrados.append("MAT: " + nombre)
        return encontrados
