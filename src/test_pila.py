from pila import Pila


def verificar(nombre: str,esperado: object,obtenido: object) -> None:
    print(f"\nPrueba: {nombre}")
    print(f"Esperado: {esperado}")
    print(f"Obtenido: {obtenido}")

    if obtenido == esperado:
        print("Resultado: APROBADO")
    else:
        print("Resultado: FALLO")


def ejecutar_pruebas_pila() -> None:
    pila: Pila[int] = Pila()

    print("\nPRUEBAS DE PILA")

    # 1. Pila recien creada.
    verificar("Pila inicialmente vacia", True, pila.esta_vacia())
    verificar("Tamanioo inicial", 0, pila.tamanio())

    # 2. Un elemento.
    pila.apilar(10)
    verificar("Cima despues de apilar 10", 10, pila.cima())
    verificar("Tamanio con un elemento", 1, pila.tamanio())

    # 3. Varios elementos.
    pila.apilar(20)
    pila.apilar(30)
    verificar("Cima con varios elementos", 30, pila.cima())
    verificar("Tamanio con tres elementos", 3, pila.tamanio())

    # 4. vaciado de pila
    verificar("Primero debe salir 30", 30, pila.desapilar())
    verificar("Despues debe salir 20", 20, pila.desapilar())
    verificar("Finalmente debe salir 10", 10, pila.desapilar())
    verificar("Pila vacia despues de retirar todo", True, pila.esta_vacia())
    verificar("Tamanio despues de retirar todo", 0, pila.tamanio())

    # 5. Desapilar una pila vacia.
    print("\nPrueba: desapilar una pila vacia")
    print("Esperado: IndexError")

    try:
        pila.desapilar()
        print('Prueba fallida: Permitio desapilar una pila vacia')
    except IndexError as error:
        print(f"Obtenido: IndexError ({error})")
        print("Resultado: APROBADO")

    # 6. Consultar la cima de una pila vacia.
    print("\nPrueba: consultar la cima vacia")
    print("Esperado: IndexError")

    try:
        pila.cima()
        print("Resultado: FALLO; no se produjo IndexError")
    except IndexError as error:
        print(f"Obtenido: IndexError ({error})")
        print("Resultado: APROBADO")


if __name__ == "__main__":
    ejecutar_pruebas_pila()