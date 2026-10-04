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

    def diferencia_interhemisferica(self, canal_izq, canal_der):
        # Resta columna a columna (fila por fila): izquierdo - derecho, en µV.
        # El resultado queda guardado como una columna NUEVA de la tabla.
        nueva = canal_izq + "-" + canal_der
        self.__tabla[nueva] = self.__tabla[canal_izq] - self.__tabla[canal_der]
        return nueva

    def promedio_por_condicion(self, columna):
        # groupby agrupa las filas por condición y saca el promedio de cada grupo
        return self.__tabla.groupby("condition")[columna].mean()


# ==========================================================
# FUNCIONES DE OPERACIÓN (se le pasan como argumento al método operar)
# ==========================================================
def sumar(a, b):
    return a + b


def restar(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


# ==========================================================
# CLASE PARA LOS ARCHIVOS .MAT
# ==========================================================
class ArchivoMAT:
    def __init__(self, nombre, ruta, fs=250):
        self.__nombre = nombre
        self.__ruta = ruta
        self.__fs = fs                              # frecuencia de muestreo: 250 muestras por segundo
        # whosmat da una lista con (nombre, forma, tipo) de cada variable, sin cargar los datos
        self.__variables = sio.whosmat(ruta)
        # loadmat devuelve un DICCIONARIO {nombre_variable: matriz}
        dicc = sio.loadmat(ruta)
        llave = self.__variables[0][0]              # nombre de la variable, ej. 'Visual'
        self.__matriz = dicc[llave]                 # matriz 3D (canales, puntos, épocas)

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
            # variable = ('Visual', (64, 625, 189), 'single')
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
        # (canales, puntos, épocas) -> (canales, puntos * épocas)
        # order="F" pone las épocas una detrás de otra (como una señal continua).
        canales, puntos, epocas = self.__matriz.shape
        return np.reshape(self.__matriz, (canales, puntos * epocas), order="F")

    def operar(self, funcion, canales, pmin, pmax):
        # funcion: sumar, restar o multiplicar (se recibe la FUNCIÓN, sin paréntesis)
        # canales: lista con los 4 canales elegidos, ej. [0, 10, 20, 30]
        # pmin, pmax: rango de puntos de la matriz 2D (pmax no se incluye)
        matriz = self.matriz2D()
        tiempo = np.arange(pmin, pmax) / self.__fs      # eje X en segundos

        # resultado = c1 (op) c2 (op) c3 (op) c4
        resultado = matriz[canales[0], pmin:pmax]
        for c in canales[1:]:
            resultado = funcion(resultado, matriz[c, pmin:pmax])

        # Al multiplicar 4 voltajes las unidades quedan en µV^4
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
        # Se usa la matriz 3D ORIGINAL (sin el reshape).
        # Los dos ejes que se ponen en axis desaparecen; queda solo el tercero.
        promedio = np.mean(self.__matriz, axis=(eje1, eje2))
        desviacion = np.std(self.__matriz, axis=(eje1, eje2))
        print("Forma original de la matriz:", self.__matriz.shape)
        print("Forma final del promedio:", promedio.shape)
        print("Forma final de la desviación:", desviacion.shape)

        # Dos boxplots en el MISMO eje
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


# ==========================================================
# CLASE SISTEMA (puntos extra): guarda cada objeto creado y permite buscarlo
# ==========================================================
class Sistema:
    def __init__(self):
        # Dos diccionarios {nombre: objeto}, uno para cada tipo de archivo
        self.__csv = {}
        self.__mat = {}

    def ingresarCSV(self, archivo):
        self.__csv[archivo.verNombre()] = archivo

    def ingresarMAT(self, archivo):
        self.__mat[archivo.verNombre()] = archivo

    def verCSV(self, nombre):
        # .get devuelve False si el nombre no está guardado
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
        # Devuelve los nombres que contienen el texto (sin importar mayúsculas)
        encontrados = []
        for nombre in self.__csv:
            if texto.lower() in nombre.lower():
                encontrados.append("CSV: " + nombre)
        for nombre in self.__mat:
            if texto.lower() in nombre.lower():
                encontrados.append("MAT: " + nombre)
        return encontrados
