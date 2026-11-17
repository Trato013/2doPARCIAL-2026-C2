def _clave(receta, campo):
    if campo == "tiempo":
        return receta.tiempo_min
    if campo == "dificultad":
        orden = {"baja": 0, "media": 1, "alta": 2}
        if receta.dificultad not in orden:
            raise ValueError("Dificultad inválida")
        return orden[receta.dificultad]
    raise ValueError("Campo de ordenamiento inválido")


def ordenar_seleccion(recetas, campo, descendente=False):
    n = len(recetas)

    for i in range(n - 1):
        indice_extremo = i

        for j in range(i + 1, n):
            clave_j = _clave(recetas[j], campo)
            clave_extremo = _clave(recetas[indice_extremo], campo)

            if descendente:
                if clave_j > clave_extremo:
                    indice_extremo = j
            else:
                if clave_j < clave_extremo:
                    indice_extremo = j

        if indice_extremo != i:
            recetas[i], recetas[indice_extremo] = recetas[indice_extremo], recetas[i]

    return recetas


def ordenar_insercion(recetas, campo, descendente=False):
    for i in range(1, len(recetas)):
        actual = recetas[i]
        clave_actual = _clave(actual, campo)
        j = i - 1

        while j >= 0:
            clave_anterior = _clave(recetas[j], campo)
            if descendente:
                debe_mover = clave_anterior < clave_actual
            else:
                debe_mover = clave_anterior > clave_actual

            if not debe_mover:
                break

            recetas[j + 1] = recetas[j]
            j -= 1

        recetas[j + 1] = actual

    return recetas


# TEORIA
# Inserción es estable. Un algoritmo estable conserva el orden relativo de los elementos
# que tienen la misma clave de ordenamiento.
