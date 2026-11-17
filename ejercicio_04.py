from ejercicio_02 import RecetaNoEncontrada


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self._tamanio = 0

    def esta_vacia(self):
        return self.primero is None

    def tamanio(self):
        return self._tamanio

    def insertar_al_final(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self._tamanio += 1

    def insertar_al_inicio(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.ultimo = nuevo
        nuevo.siguiente = self.primero
        self.primero = nuevo
        self._tamanio += 1

    def quitar_primero(self):
        if self.esta_vacia():
            return None
        dato = self.primero.dato
        self.primero = self.primero.siguiente
        self._tamanio -= 1
        if self.primero is None:
            self.ultimo = None
        return dato

    def eliminar_donde(self, condicion):
        anterior = None
        actual = self.primero

        while actual is not None:
            if condicion(actual.dato):
                if anterior is None:
                    self.primero = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                if actual is self.ultimo:
                    self.ultimo = anterior

                self._tamanio -= 1
                return True

            anterior = actual
            actual = actual.siguiente

        return False

    def __iter__(self):
        actual = self.primero
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente


class MenuSemanal:
    DIAS = ("lunes", "martes", "miercoles", "jueves",
            "viernes", "sabado", "domingo")

    def __init__(self):
        self.platos = ListaEnlazada()

    def agregar(self, dia, receta):
        if dia not in self.DIAS:
            raise ValueError("Día inválido")

        actual = self.platos.primero
        while actual is not None:
            if actual.dato[0] == dia:
                actual.dato = (dia, receta)
                return
            actual = actual.siguiente
        self.platos.insertar_al_final((dia, receta))

    def quitar(self, dia):
        if dia not in self.DIAS:
            raise ValueError("Día inválido")
        if not self.platos.eliminar_donde(lambda par: par[0] == dia):
            raise RecetaNoEncontrada(f"No hay receta para {dia}")

    def receta_de(self, dia):
        if dia not in self.DIAS:
            raise ValueError("Día inválido")
        for dia_guardado, receta in self.platos:
            if dia_guardado == dia:
                return receta
        raise RecetaNoEncontrada(f"No hay receta para {dia}")

    def __iter__(self):
        return iter(self.platos)


# TEORIA
# La referencia al penúltimo no está guardada directamente en cada nodo.
# Se obtiene recorriendo desde el primero y conservando una referencia al nodo anterior.
