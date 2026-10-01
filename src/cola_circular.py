from typing import Generic, TypeVar, Optional, cast
T = TypeVar("T")


class ColaCircular(Generic[T]):
    def __init__(self, capacidad: int) -> None:
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
        #bool hereda de int , por lo que True se acepta como entero, por eso se valida que no sea bool
            raise ValueError("La capacidad debe ser un entero positivo")
        self.__capacidad: int = capacidad
        self.__datos: list[Optional[T]] = [None] * capacidad #Crea posiciones vacias en la lista
        self.__frente: int = 0
        self.__final: int = 0
        self.__cantidad: int = 0

    def encolar(self, dato: T) -> None:
        if self.esta_llena():
            raise OverflowError("Cola circular llena: Overflow generado")
        self.__datos[self.__final] = dato
        self.__final = (self.__final + 1) % self.__capacidad
        self.__cantidad += 1

    def tamanio(self) -> int:
        return self.__cantidad

    def desencolar(self) -> T:
        if self.esta_vacia():
            raise IndexError("Cola circular vacia: Underflow generado")
        valor: T = cast(T, self.__datos[self.__frente]) #cast: dato esperado es del tipo T al verificador
        self.__datos[self.__frente] = None
        self.__frente = (self.__frente + 1) % self.__capacidad
        self.__cantidad -= 1
        return valor

    def consultar_frente(self) -> T:
        if self.esta_vacia():
            raise IndexError("Cola circular vacia: No se puede consultar el frente")
        return cast(T, self.__datos[self.__frente]) #cast: dato esperado es del tipo T al verificador

    def frente(self) -> T:
        """Alias que conserva la compatibilidad con las llamadas anteriores."""
        return self.consultar_frente()

    def esta_vacia(self) -> bool:
        return self.tamanio() == 0

    def esta_llena(self) -> bool:
        return self.tamanio() == self.__capacidad

    def mostrar(self) -> None:
        # Recorrido en orden FIFO, complejidad O(n).
        if self.esta_vacia():
            print("Cola circular vacia")
            return
        print("Frente")
        for posicion in range(self.__cantidad):
            indice: int = (self.__frente + posicion) % self.__capacidad
            print(f"{self.__datos[indice]}")
        print("Final")

