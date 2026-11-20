class NodoCola:

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:

    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, dato):

        nuevo = NodoCola(dato)

        if self.esta_vacia():
            self.frente = nuevo
            self.final = nuevo

        else:
            self.final.siguiente = nuevo
            self.final = nuevo

    def desencolar(self):

        if self.esta_vacia():
            return None

        dato = self.frente.dato

        self.frente = self.frente.siguiente

        if self.frente is None:
            self.final = None

        return dato

    def esta_vacia(self):
        return self.frente is None

class NodoCircular:

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

# en realidad no es una ColaCircular, es una lista doblemente enlazada circular
class ColaCircular:

    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, dato):

        nuevo = NodoCircular(dato)

        if self.frente is None:
            self.frente = nuevo
            self.final = nuevo

            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo

        else:
            nuevo.anterior = self.final
            nuevo.siguiente = self.frente

            self.final.siguiente = nuevo
            self.frente.anterior = nuevo

            self.final = nuevo

    def siguiente(self):

        if self.frente is not None:
            self.frente = self.frente.siguiente

    def anterior(self):

        if self.frente is not None:
            self.frente = self.frente.anterior

    def obtener_actual(self):

        if self.frente is None:
            return None

        return self.frente.dato

    def esta_vacia(self):
        return self.frente is None