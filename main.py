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
    print(archivo)          # llama a __str__ (info y describe)


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
    print(archivo)          # llama a __str__ (whosmat)


def main():
    sis = Sistema()
    while True:
        menu = validar_entero("""
        >>>>> MENU PRINCIPAL <<<<<
        1- Cargar archivo CSV
        2- Cargar archivo MAT
        3- Trabajar con un archivo CSV
        4- Trabajar con un archivo MAT
        5- Buscar archivo
        6- Ver archivos cargados
        7- Salir
        --> """, 1, 7)

        if menu == 1:
            cargar_csv(sis)
        elif menu == 2:
            cargar_mat(sis)
        elif menu == 3 or menu == 4:
            print("Opción en construcción")
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
