from typing import Generic,TypeVar, Optional
T = TypeVar("T")


class NodoPila (Generic[T]):
    def __init__ (self,dato:T)->None :
        self.dato : T = dato
        self.siguiente : Optional["NodoPila[T]"]=None

class Pila(Generic[T]):
    def __init__(self)-> None :
        self.__cima : Optional[NodoPila[T]]=None
        self.__cantidad : int = 0

    def apilar (self,dato:T)->None:
        nuevo : NodoPila[T] = NodoPila(dato)
        nuevo.siguiente = self.__cima
        self.__cima = nuevo
        self.__cantidad +=1

    def tamanio (self)->int:
        return self.__cantidad

    def desapilar (self)-> T:
        if self.esta_vacia():
            raise IndexError("Pila Vacia : Underflow generado")
        valor : T = self.__cima.dato
        self.__cima = self.__cima.siguiente
        self.__cantidad -=1
        return valor

    def cima (self)->T:
        if self.__cima is None:
            raise IndexError ("Pila vacia : No se puede consultar la cima")
        return self.__cima.dato

    def esta_vacia(self)->bool:
        return self.tamanio()==0

    def mostrar(self) -> None: #Recorrido lineal, complejidad O(n)
        if self.__cima is None :
            raise IndexError ("Pila vacia")
        actual : Optional[NodoPila[T]] = self.__cima
        print("Cima")

        while actual is not None :
            print(f'{actual.dato}')
            actual = actual.siguiente

        print("Base")
