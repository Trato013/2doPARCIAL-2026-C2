def busqueda_lineal(recetas, ingredientes, campo, valor):
    encontrados = []

    for receta in recetas:
        coincide = False

        if campo == "nombre":
            coincide = receta.nombre == valor
        elif campo == "categoria":
            coincide = receta.categoria == valor
        elif campo == "ingrediente":
            for id_receta, nombre, cantidad, unidad in ingredientes:
                if id_receta == receta.id and nombre == valor:
                    coincide = True
                    break
        else:
            raise ValueError("Campo de búsqueda inválido")

        if coincide:
            encontrados.append(receta)

    return encontrados


def busqueda_binaria(recetas, campo, valor):
    if campo != "nombre":
        raise ValueError("La búsqueda binaria solo admite el campo nombre")

    izquierda = 0
    derecha = len(recetas) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        nombre_medio = recetas[medio].nombre

        if nombre_medio == valor:
            return recetas[medio]
        elif nombre_medio < valor:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None


# TEORIA
# No, porque la búsqueda binaria necesita que los elementos estén ordenados por el mismo
# campo que se está buscando para poder descartar correctamente una mitad.
