from typing import Generic, Optional, TypeVar
T = TypeVar("T")


class NodoDeque(Generic[T]):
  def __init__(self, dato: T) -> None:   
    self.dato: T = dato
    self.anterior: Optional["NodoDeque[T]"] = None
    self.siguiente: Optional["NodoDeque[T]"] = None


class Deque(Generic[T]):
  
  def __init__(self) -> None:
    self.__frente: Optional[NodoDeque[T]] = None
    self.__final: Optional[NodoDeque[T]] = None
    self.__tamanio: int = 0
  
  def esta_vacio(self) -> bool:
    return self.__tamanio == 0
  
  def tamanio(self) -> int:
    return self.__tamanio      
  
  def insertar_frente(self, dato: T) -> None:
    nuevo = NodoDeque(dato)

    if self.esta_vacio():
      self.__frente = nuevo 
      self.__final = nuevo
    else:  
      self.__frente.anterior = nuevo
      nuevo.siguiente = self.__frente
      self.__frente = nuevo

    self.__tamanio +=  1
    
  def insertar_final(self, dato: T) -> None:
    nuevo = NodoDeque(dato)

    if self.esta_vacio():
      self.__frente = nuevo
      self.__final = nuevo
    else:
      self.__final.siguiente = nuevo
      nuevo.anterior = self.__final
      self.__final = nuevo

    self.__tamanio += 1      

  def eliminar_frente(self) -> T:
    if self.esta_vacio():
      raise IndexError("El deque esta vacio (Underflow)")

    valor = self.__frente

    if self.__tamanio == 1:
      self.__frente = None
      self.__final = None
    else:
      self.__frente = valor.siguiente
      self.__frente.anterior = None

    self.__tamanio -= 1  

    return valor.dato 


  def eliminar_final(self) -> T:
    if self.esta_vacio():
      raise IndexError("El deque esta vacio (Underflow)")

    valor = self.__final

    if self.__tamanio == 1:
      self.__frente = None
      self.__final = None
    else:
      self.__final = valor.anterior
      self.__final.siguiente = None

    self.__tamanio -= 1

    return valor.dato    

    
  def consultar_frente(self) -> T:
    if self.esta_vacio():
      raise IndexError("El deque esta vacio (Underflow)")

    return self.__frente.dato

  def consultar_final(self) -> T:
    if self.esta_vacio():
      raise IndexError("El deque esta vacio (Underflow)")

    return self.__final.dato
  
  def mostrar(self) -> None:
    if self.esta_vacio():
      print("Deque vacio")
      return
 
    actual = self.__frente
    elementos = []
    while actual is not None:
      elementos.append(str(actual.dato))
      actual = actual.siguiente
 
    print(elementos)
