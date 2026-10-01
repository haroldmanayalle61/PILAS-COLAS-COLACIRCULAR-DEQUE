from typing import Callable, Optional, TypeVar
from cola_circular import ColaCircular

T = TypeVar("T")
cola_enteros: Optional[ColaCircular[int]] = None
cola_cadenas: Optional[ColaCircular[str]] = None


def leer_entero(mensaje: str) -> int:
    cadena: str = input(mensaje).strip()
    try:
        return int(cadena)
    except ValueError:
        raise ValueError("Ingrese un numero entero") from None

def leer_cadena(mensaje: str) -> str:
    cadena: str = input(mensaje).strip()
    if cadena == "":
        raise ValueError("La captura no puede estar vacia")
    return cadena

def mostrar_estado(cola_capturas: ColaCircular[T]) -> None:
    cola_capturas.mostrar()
    print(f"Tamanio: {cola_capturas.tamanio()}")
    if cola_capturas.esta_vacia():
        print("Frente: ninguno")
    else:
        print(f"Frente: {cola_capturas.consultar_frente()}")
    if cola_capturas.esta_llena():
        print("Cola circular llena")
    else:
        print("Cola circular no llena")

#Callable indica que el parametro recibe una funcion que acepta un str y devuelve un tipo T
def submenu_circular(cola_capturas: ColaCircular[T], leer_dato: Callable[[str], T]) -> None:
    #Recibe una cola circular y una funcion para leer el tipo de dato correspondiente
    while True:
        try:
            print("=" * 10 + " SUBMENU - COLA CIRCULAR " + "=" * 10)
            print("1. Encolar una captura")
            print("2. Retirar la captura mas antigua")
            print("3. Consultar el frente")
            print("4. Mostrar el estado del buffer")
            print("5. Consultar el tamanio")
            print("6. Comprobar si esta vacia")
            print("7. Comprobar si esta llena")
            print("0. Cerrar submenu")
            opcion: int = leer_entero("Ingrese una opcion: ")

            match opcion:
                case 1:
                    captura: T = leer_dato("Ingrese una captura: ")
                    cola_capturas.encolar(captura)
                    mostrar_estado(cola_capturas)
                case 2:
                    valor: T = cola_capturas.desencolar()
                    print(f"Captura retirada: {valor}")
                    mostrar_estado(cola_capturas)
                case 3:
                    print(f"Frente: {cola_capturas.consultar_frente()}")
                case 4:
                    mostrar_estado(cola_capturas)
                case 5:
                    print(f"Tamanio de la cola circular: {cola_capturas.tamanio()}")
                case 6:
                    if cola_capturas.esta_vacia():
                        print("Cola circular vacia")
                    else:
                        print("Cola circular no vacia")
                        mostrar_estado(cola_capturas)
                case 7:
                    if cola_capturas.esta_llena():
                        print("Cola circular llena")
                    else:
                        print("Cola circular no llena")
                        mostrar_estado(cola_capturas)
                case 0:
                    print("Menu cerrado exitosamente")
                    break
                case _:
                    print("Opcion fuera de rango")

        except (ValueError, IndexError, OverflowError) as error:
            print(f"Error ({type(error).__name__}): {error}")

def ejecutar() -> None:
    global cola_enteros, cola_cadenas
     #Si fuera dentro cada vez que llame a la funcion, se crearia una nueva cola 

    while True:
        try:
            print("TIPO DE DATOS")
            print("1. Enteros")
            print("2. Cadenas")
            print("0. Volver al menu principal")
            tipo: int = leer_entero("Ingrese el tipo de datos: ")
            if tipo == 0:
                return
            if tipo not in (1, 2):
                raise ValueError("Seleccione 1 para enteros o 2 para cadenas")
            if tipo == 1:
                if cola_enteros is None:
                    capacidad = leer_entero("Ingrese la capacidad de la cola circular: ")
                    cola_enteros = ColaCircular[int](capacidad)
                submenu_circular(cola_enteros, leer_entero)
            else:
                if cola_cadenas is None:
                    capacidad = leer_entero("Ingrese la capacidad de la cola circular: ")
                    cola_cadenas = ColaCircular[str](capacidad)
                submenu_circular(cola_cadenas, leer_cadena)
            return
        except ValueError as error:
            print(f"Error ({type(error).__name__}): {error}")

if __name__ == "__main__":
    ejecutar()
