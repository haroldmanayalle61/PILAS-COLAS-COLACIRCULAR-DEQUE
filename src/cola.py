from typing import Generic, TypeVar, Optional, Iterator


T = TypeVar("T")


class NodoCola(Generic[T]):

    def __init__(self, dato: T) -> None:
        self.dato: T = dato
        self.siguiente: Optional["NodoCola[T]"] = None


class Cola(Generic[T]):

    def __init__(self) -> None:
        self.__frente: Optional[NodoCola[T]] = None
        self.__final: Optional[NodoCola[T]] = None
        self.__cantidad: int = 0


    def encolar(self, dato: T) -> None:
        nuevo: NodoCola[T] = NodoCola(dato)

        if self.esta_vacia():
            self.__frente = nuevo

        else:
            assert self.__final is not None
            self.__final.siguiente = nuevo

        self.__final = nuevo
        self.__cantidad += 1


    def desencolar(self) -> T:

        if self.esta_vacia():
            raise IndexError(
                "Cola vacía: Underflow generado"
            )

        assert self.__frente is not None

        valor: T = self.__frente.dato

        self.__frente = self.__frente.siguiente
        self.__cantidad -= 1

        # Si se retiró el último elemento
        if self.__frente is None:
            self.__final = None

        return valor


    def frente(self) -> T:

        if self.esta_vacia():
            raise IndexError(
                "Cola vacía: No se puede consultar el frente"
            )

        assert self.__frente is not None

        return self.__frente.dato


    def esta_vacia(self) -> bool:
        return self.__cantidad == 0


    def tamanio(self) -> int:
        return self.__cantidad


    def __iter__(self) -> Iterator[T]:
        """
        Permite recorrer la cola sin modificarla.
        """

        actual = self.__frente

        while actual is not None:
            yield actual.dato
            actual = actual.siguiente


    def mostrar(self) -> None:

        if self.esta_vacia():
            print("Cola vacía")
            return

        print("Frente")

        for dato in self:
            print(dato)

        print("Final")