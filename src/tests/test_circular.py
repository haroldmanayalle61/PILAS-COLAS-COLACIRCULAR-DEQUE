import sys
from pathlib import Path

# Permite ejecutar el archivo directamente desde la carpeta tests.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cola_circular import ColaCircular

def verificar(nombre: str, esperado: object, obtenido: object) -> None:
    print(f"\nPrueba: {nombre}")
    print(f"Esperado: {esperado} | Obtenido: {obtenido}")
    if esperado != obtenido:
        raise AssertionError(f"Resultado: FALLO; {nombre}")
    print("Resultado: APROBADO")


def ejecutar_pruebas_circular() -> None:
    cola: ColaCircular[int] = ColaCircular(10)

    print("\nPRUEBAS DE COLA CIRCULAR (CAPACIDAD 10)")

    # 1. Cola vacia, un elemento y varios elementos.
    verificar("Cola inicialmente vacia", True, cola.esta_vacia())
    verificar("Tamanio inicial", 0, cola.tamanio())
    cola.encolar(10)
    verificar("Frente despues de encolar 10", 10, cola.frente())
    verificar("Tipo del dato en la cola de enteros", int, type(cola.frente()))
    verificar("Tamanio con un elemento", 1, cola.tamanio())
    cola.encolar(20)
    cola.encolar(30)
    verificar("Frente con varios elementos", 10, cola.frente())
    verificar("Tamanio con tres elementos", 3, cola.tamanio())

    # 2. Ocupacion parcial y dos retiros.
    for dato in range(40, 100, 10):
        cola.encolar(dato)
    print("\nOcupacion parcial:")
    cola.mostrar()
    verificar("Primero debe salir 10", 10, cola.desencolar())
    verificar("Despues debe salir 20", 20, cola.desencolar())
    print("\nEstado despues de dos retiros:")
    cola.mostrar()

    # 3. Retorno del final a cero y reutilizacion hasta llenar la cola.
    cola.encolar(100)
    print("\nRetorno del indice final a cero:")
    cola.mostrar()
    cola.encolar(110)
    cola.encolar(120)
    verificar("Cola llena", True, cola.esta_llena())#
    verificar("Tamanio de la cola llena", 10, cola.tamanio())
    cola.mostrar()

    # 4. Overflow.
    print("\nPrueba: encolar en cola llena | Esperado: OverflowError")
    try:
        cola.encolar(130)
    except OverflowError as error:
        print(f"Obtenido: OverflowError ({error}) | Resultado: APROBADO")
    else:
        raise AssertionError("Resultado: FALLO; no se produjo OverflowError")

    # 5. Vaciado en orden FIFO.
    for esperado in range(30, 130, 10):
        verificar(f"Debe salir {esperado} en orden FIFO", esperado, cola.desencolar())
    verificar("Cola vacia despues de retirar todo", True, cola.esta_vacia())
    verificar("Tamanio despues de retirar todo", 0, cola.tamanio())

    # 6. Underflow.
    print("\nPrueba: desencolar cola vacia | Esperado: IndexError")
    try:
        cola.desencolar()
    except IndexError as error:
        print(f"Obtenido: IndexError ({error}) | Resultado: APROBADO")
    else:
        raise AssertionError("Resultado: FALLO; no se produjo IndexError")

    # 7. Consultar el frente vacio.
    print("\nPrueba: consultar frente vacio | Esperado: IndexError")
    try:
        cola.frente()
    except IndexError as error:
        print(f"Obtenido: IndexError ({error}) | Resultado: APROBADO")
    else:
        raise AssertionError("Resultado: FALLO; no se produjo IndexError")

    # 8. La misma clase generica tambien trabaja con cadenas.
    cola_texto: ColaCircular[str] = ColaCircular(10)
    cola_texto.encolar("007")
    cola_texto.encolar("Captura")
    verificar("Frente de la cola de cadenas", "007", cola_texto.frente())
    verificar("Tipo del dato en la cola de cadenas", str, type(cola_texto.frente()))
    verificar("Primera cadena en salir", "007", cola_texto.desencolar())
    verificar("Segunda cadena en salir", "Captura", cola_texto.desencolar())
    verificar("Cola de cadenas vacia", True, cola_texto.esta_vacia())

if __name__ == "__main__":
    ejecutar_pruebas_circular()