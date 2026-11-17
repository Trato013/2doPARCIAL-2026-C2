import struct
from ejercicio_02 import LibroRecetas
from ejercicio_01 import Receta
from ejercicio_09 import ArchivoInvalidoError


FORMATO_ENCABEZADO = "<4scI"
FORMATO_REGISTRO = "<I32sH8s16s"
TAMANIO_ENCABEZADO = struct.calcsize(FORMATO_ENCABEZADO)  # 9 bytes
TAMANIO_REGISTRO = struct.calcsize(FORMATO_REGISTRO)      # 62 bytes


def _codificar_cadena(texto, ancho):
    datos = str(texto).encode("utf-8")
    datos = datos[:ancho]

    # Evita dejar una secuencia UTF-8 incompleta al recortar por bytes.
    while datos:
        try:
            datos.decode("utf-8")
            break
        except UnicodeDecodeError:
            datos = datos[:-1]

    return datos.ljust(ancho, b"\\0")


def _decodificar_cadena(datos):
    return datos.split(b"\\0", 1)[0].decode("utf-8")


def _empaquetar_receta(receta):
    return struct.pack(
        FORMATO_REGISTRO,
        receta.id,
        _codificar_cadena(receta.nombre, 32),
        receta.tiempo_min,
        _codificar_cadena(receta.dificultad, 8),
        _codificar_cadena(receta.categoria, 16)
    )


def _leer_encabezado(archivo):
    archivo.seek(0)
    datos = archivo.read(TAMANIO_ENCABEZADO)
    if len(datos) < TAMANIO_ENCABEZADO:
        raise ArchivoInvalidoError("Archivo más corto que el encabezado")

    magia, tema, cantidad = struct.unpack(FORMATO_ENCABEZADO, datos)
    if magia != b"AYED":
        raise ArchivoInvalidoError("Magia inválida")

    return cantidad


def guardar_binario(ruta, libro):
    recetas = libro.listar()
    try:
        with open(ruta, "wb") as archivo:
            encabezado = struct.pack(
                FORMATO_ENCABEZADO, b"AYED", b"R", len(recetas)
            )
            archivo.write(encabezado)

            for receta in recetas:
                archivo.write(_empaquetar_receta(receta))
    except (OSError, struct.error, UnicodeError) as error:
        raise ArchivoInvalidoError("No se pudo guardar el archivo") from error


def cargar_binario(ruta):
    libro = LibroRecetas()
    try:
        with open(ruta, "rb") as archivo:
            cantidad = _leer_encabezado(archivo)
            for _ in range(cantidad):
                datos = archivo.read(TAMANIO_REGISTRO)
                if len(datos) != TAMANIO_REGISTRO:
                    raise ArchivoInvalidoError("Registro incompleto")

                id_receta, nombre, tiempo, dificultad, categoria = struct.unpack(
                    FORMATO_REGISTRO, datos
                )
                try:
                    receta = Receta(
                        id_receta,
                        _decodificar_cadena(nombre),
                        tiempo,
                        _decodificar_cadena(dificultad),
                        _decodificar_cadena(categoria)
                    )
                except (UnicodeDecodeError, ValueError) as error:
                    raise ArchivoInvalidoError("Registro inválido") from error
                libro.agregar(receta)

    except ArchivoInvalidoError:
        raise
    except (OSError, struct.error, UnicodeError) as error:
        raise ArchivoInvalidoError("No se pudo leer el archivo") from error

    return libro


def actualizar_registro(ruta, posicion, receta):
    try:
        with open(ruta, "r+b") as archivo:
            cantidad = _leer_encabezado(archivo)

            if posicion < 0 or posicion >= cantidad:
                raise ArchivoInvalidoError("Posición fuera de rango")

            archivo.seek(0, 2)
            tamanio_archivo = archivo.tell()
            tamanio_esperado = TAMANIO_ENCABEZADO + cantidad * TAMANIO_REGISTRO
            if tamanio_archivo < tamanio_esperado:
                raise ArchivoInvalidoError("Archivo con registros incompletos")

            desplazamiento = TAMANIO_ENCABEZADO + posicion * TAMANIO_REGISTRO
            archivo.seek(desplazamiento)
            archivo.write(_empaquetar_receta(receta))

    except ArchivoInvalidoError:
        raise
    except (OSError, struct.error, UnicodeError) as error:
        raise ArchivoInvalidoError("No se pudo actualizar el archivo") from error


# TEORIA
# El tamaño fijo del registro (62 bytes) y el encabezado de 9 bytes permiten calcular
# el inicio: 9 + posicion * 62.
