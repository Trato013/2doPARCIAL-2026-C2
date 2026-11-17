import csv
from ejercicio_02 import LibroRecetas
from ejercicio_01 import Receta


class ArchivoInvalidoError(Exception):
    pass


ENCABEZADO_RECETAS = ["id", "nombre", "tiempo_min", "dificultad", "categoria"]
ENCABEZADO_INGREDIENTES = ["receta_id", "nombre", "cantidad", "unidad"]


def guardar_recetas_csv(ruta, libro):
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo, delimiter=",")
            escritor.writerow(ENCABEZADO_RECETAS)
            for receta in libro.listar():
                escritor.writerow([
                    receta.id, receta.nombre, receta.tiempo_min,
                    receta.dificultad, receta.categoria
                ])
    except (OSError, csv.Error, UnicodeError) as error:
        raise ArchivoInvalidoError("No se pudo guardar el archivo") from error


def cargar_recetas_csv(ruta):
    libro = LibroRecetas()
    try:
        with open(ruta, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo, delimiter=",")
            encabezado = next(lector, None)
            if encabezado != ENCABEZADO_RECETAS:
                raise ArchivoInvalidoError("Encabezado de recetas inválido")

            for fila in lector:
                if len(fila) != 5:
                    raise ArchivoInvalidoError("Cantidad de columnas inválida")
                try:
                    receta = Receta(
                        int(fila[0]), fila[1], int(fila[2]), fila[3], fila[4]
                    )
                except ValueError as error:
                    raise ArchivoInvalidoError("Número inválido") from error
                libro.agregar(receta)

    except ArchivoInvalidoError:
        raise
    except (OSError, csv.Error, UnicodeError, StopIteration) as error:
        raise ArchivoInvalidoError("No se pudo leer el archivo") from error

    return libro


def guardar_ingredientes_csv(ruta, ingredientes):
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo, delimiter=",")
            escritor.writerow(ENCABEZADO_INGREDIENTES)
            for ingrediente in ingredientes:
                escritor.writerow(ingrediente)
    except (OSError, csv.Error, UnicodeError) as error:
        raise ArchivoInvalidoError("No se pudo guardar el archivo") from error


def cargar_ingredientes_csv(ruta):
    ingredientes = []
    try:
        with open(ruta, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo, delimiter=",")
            encabezado = next(lector, None)
            if encabezado != ENCABEZADO_INGREDIENTES:
                raise ArchivoInvalidoError("Encabezado de ingredientes inválido")

            for fila in lector:
                if len(fila) != 4:
                    raise ArchivoInvalidoError("Cantidad de columnas inválida")
                try:
                    receta_id = int(fila[0])
                    cantidad = int(fila[2])
                except ValueError as error:
                    raise ArchivoInvalidoError("Número inválido") from error
                ingredientes.append((receta_id, fila[1], cantidad, fila[3]))

    except ArchivoInvalidoError:
        raise
    except (OSError, csv.Error, UnicodeError, StopIteration) as error:
        raise ArchivoInvalidoError("No se pudo leer el archivo") from error

    return ingredientes


# TEORIA
# No, hace falta leer los registros anteriores: el acceso al archivo de texto es secuencial.
