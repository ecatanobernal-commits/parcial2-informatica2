from clases import *


def cargar_csv(sis):
    nombre = input("Nombre para identificar el archivo (ej. paciente1): ")
    if sis.existe(nombre):
        print("Ya existe un archivo con ese nombre")
        return
    ruta = input("Ruta del archivo .csv (ej. ../Arch_CSV/ERP_01.csv): ")
    try:
        archivo = ArchivoCSV(nombre, ruta)
    except FileNotFoundError:
        print("No se encontró el archivo, revise la ruta")
        return
    sis.ingresarCSV(archivo)
    print(archivo)


def cargar_mat(sis):
    nombre = input("Nombre para identificar el archivo (ej. visual1): ")
    if sis.existe(nombre):
        print("Ya existe un archivo con ese nombre")
        return
    ruta = input("Ruta del archivo .mat (ej. ../Archs_MAT/Visual_Cue.mat): ")
    try:
        archivo = ArchivoMAT(nombre, ruta)
    except FileNotFoundError:
        print("No se encontró el archivo, revise la ruta")
        return
    sis.ingresarMAT(archivo)
    print(archivo)


def menu_csv(archivo):
    while True:
        print(f"\n----- CSV: {archivo.verNombre()} -----")
        print("1- Ver información (info y describe)")
        print("2- Gráficas por condición (stem, histograma y scatter)")
        print("3- Diferencia interhemisférica")
        print("4- Volver al menú principal")
        opcion = validar_entero("--> ", 1, 4)

        if opcion == 1:
            print(archivo)

        elif opcion == 2:
            condicion = validar_entero("Condición (1, 2 o 3): ", 1, 3)
            columnas = archivo.verColumnas()
            print("Columnas disponibles:", columnas)
            canal = validar_opcion("Canal para el stem y el histograma: ", columnas)
            canal_x = validar_opcion("Columna para el eje X del scatter: ", columnas)
            canal_y = validar_opcion("Columna para el eje Y del scatter: ", columnas)
            imagen = archivo.graficar(condicion, canal, canal_x, canal_y)
            print("Gráfica guardada como:", imagen)

        elif opcion == 3:
            print("Pares sugeridos (izquierdo = impar, derecho = par): FC3-FC4, C3-C4, CP3-CP4")
            columnas = archivo.verColumnas()
            print("Columnas disponibles:", columnas)
            izq = validar_opcion("Canal del hemisferio IZQUIERDO: ", columnas)
            der = validar_opcion("Canal del hemisferio DERECHO: ", columnas)
            nueva = archivo.diferencia_interhemisferica(izq, der)
            tabla = archivo.verTabla()
            print(f"\nNueva columna '{nueva}' (µV). Primeros 10 registros:")
            print(tabla[["condition", izq, der, nueva]].head(10))
            print(f"\nPromedio de '{nueva}' en cada condición (µV):")
            print(archivo.promedio_por_condicion(nueva))

        elif opcion == 4:
            break


def menu_mat(archivo):
    while True:
        print(f"\n----- MAT: {archivo.verNombre()} -----")
        print("1- Ver variables del archivo (whosmat)")
        print("2- Operación entre 4 canales (matriz 2D)")
        print("3- Promedio y desviación estándar en dos ejes (matriz 3D)")
        print("4- Volver al menú principal")
        opcion = validar_entero("--> ", 1, 4)

        if opcion == 1:
            print(archivo)

        elif opcion == 2:
            print("1- Suma\n2- Resta\n3- Multiplicación")
            op = validar_entero("Operación: ", 1, 3)
            if op == 1:
                funcion = sumar
            elif op == 2:
                funcion = restar
            else:
                funcion = multiplicar

            canales, puntos, epocas = archivo.verForma()
            total = puntos * epocas
            lista_canales = []
            for i in range(4):
                c = validar_entero(f"Canal {i + 1} (0 a {canales - 1}): ", 0, canales - 1)
                lista_canales.append(c)

            print(f"La matriz 2D tiene {total} puntos ({archivo.verFs()} puntos = 1 segundo)")
            pmin = validar_entero(f"Punto mínimo (0 a {total - 2}): ", 0, total - 2)
            pmax = validar_entero(f"Punto máximo ({pmin + 1} a {total}): ", pmin + 1, total)
            imagen = archivo.operar(funcion, lista_canales, pmin, pmax)
            print("Gráfica guardada como:", imagen)

        elif opcion == 3:
            print("Ejes: 0 = canales, 1 = puntos (tiempo), 2 = épocas")
            eje1 = validar_entero("Primer eje: ", 0, 2)
            eje2 = validar_entero("Segundo eje: ", 0, 2)
            while eje2 == eje1:
                print("Los ejes deben ser diferentes")
                eje2 = validar_entero("Segundo eje: ", 0, 2)
            forma = archivo.promedio_desviacion(eje1, eje2)
            print("Forma final del vector resultante:", forma)

        elif opcion == 4:
            break


def main():
    sis = Sistema()
    while True:
        print("\n>>>>> MENU PRINCIPAL <<<<<")
        print("1- Cargar archivo CSV")
        print("2- Cargar archivo MAT")
        print("3- Trabajar con un archivo CSV")
        print("4- Trabajar con un archivo MAT")
        print("5- Buscar archivo")
        print("6- Ver archivos cargados")
        print("7- Salir")
        menu = validar_entero("--> ", 1, 7)

        if menu == 1:
            cargar_csv(sis)

        elif menu == 2:
            cargar_mat(sis)

        elif menu == 3:
            print("Archivos CSV cargados:", sis.verNombresCSV())
            archivo = sis.verCSV(input("Nombre del archivo: "))
            if archivo == False:
                print("Ese archivo CSV no está cargado")
            else:
                menu_csv(archivo)

        elif menu == 4:
            print("Archivos MAT cargados:", sis.verNombresMAT())
            archivo = sis.verMAT(input("Nombre del archivo: "))
            if archivo == False:
                print("Ese archivo MAT no está cargado")
            else:
                menu_mat(archivo)

        elif menu == 5:
            texto = input("Texto a buscar: ")
            print("Encontrados:", sis.buscar(texto))

        elif menu == 6:
            print("Archivos CSV:", sis.verNombresCSV())
            print("Archivos MAT:", sis.verNombresMAT())

        elif menu == 7:
            print("Hasta luego")
            break


if __name__ == "__main__":
    main()
