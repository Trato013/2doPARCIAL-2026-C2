from ejercicio_01 import Receta


class RecetaNoEncontrada(Exception):
    pass


class LibroRecetas:
    def __init__(self):
        self.recetas = []

    def agregar(self, receta):
        for i in range(len(self.recetas)):
            if self.recetas[i].id == receta.id:
                self.recetas[i] = receta
                return
        self.recetas.append(receta)

    def obtener(self, id):
        for receta in self.recetas:
            if receta.id == id:
                return receta
        raise RecetaNoEncontrada(f"No existe la receta {id}")

    def listar(self):
        return self.recetas[:]

    def cantidad(self):
        return len(self.recetas)


# TEORIA
# Quien llama puede distinguir claramente el caso de error y manejarlo sin confundirlo
# con un resultado válido.
