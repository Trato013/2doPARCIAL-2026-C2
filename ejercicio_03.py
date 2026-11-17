from ejercicio_02 import RecetaNoEncontrada


class SubrecetaFaltanteError(Exception):
    pass


class IngredienteFaltanteError(Exception):
    pass


def ingredientes_totales(receta_id, libro, subrecetas, ingredientes):
    # Verifica que la receta inicial exista.
    libro.obtener(receta_id)

    resultado = []

    # Primero se agregan los ingredientes propios, respetando el orden recibido.
    for fila in ingredientes:
        id_receta, nombre, cantidad, unidad = fila
        if id_receta == receta_id:
            if nombre is None or str(nombre).strip() == "":
                raise IngredienteFaltanteError("Ingrediente sin nombre")
            resultado.append((nombre, cantidad, unidad))

    # Después se expanden las sub-recetas, una por una, en profundidad.
    for id_padre, id_subreceta in subrecetas:
        if id_padre == receta_id:
            try:
                libro.obtener(id_subreceta)
            except RecetaNoEncontrada:
                raise SubrecetaFaltanteError(f"No existe la sub-receta {id_subreceta}")
            resultado.extend(
                ingredientes_totales(id_subreceta, libro, subrecetas, ingredientes)
            )

    return resultado


# TEORIA
# Traza para ingredientes_totales(9):
# 9 -> 1 (caso base) -> 2 (caso base).
