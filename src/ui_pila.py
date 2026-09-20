from pila import Pila

pila_acciones : Pila[str] = Pila()

def leer_entero(mensaje : str)->int:
    cadena: str = input(mensaje).strip()
    try:
        return int(cadena)
    except ValueError:
        raise ValueError("Ingrese un número entero") from None

def mostrar_estado() -> None:
    pila_acciones.mostrar()
    print(f"Tamanioo: {pila_acciones.tamanio()}")

    if pila_acciones.esta_vacia():
        print("Cima: ninguna")
    else:
        print(f"Cima: {pila_acciones.cima()}")

def submenu_pila () -> None:
    while True:
        try :
            print(f'{'='*10}SUBMENU - OPERACIONES CON PILA{'='*10}')
            print('1. Apilar una accion')
            print('2. Deshacer la última accion')
            print('3. Consultar la cima')
            print('4. Mostrar la pila')
            print('5. Consultar el tamanio')
            print('6. Comprobar si esta vacia')
            print('0. Cerrar submenu')
            opcion = leer_entero('Ingrese una opcion')

            match opcion:
                case 1:
                    accion = input('Ingrese una accion : ').strip()
                    if accion == "":
                        raise ValueError('La accion no puede estar vacia')
                    pila_acciones.apilar(accion)
                    mostrar_estado()
                case 2:
                    valor = pila_acciones.desapilar()
                    print(f'Accion deshecha: {valor}')
                    mostrar_estado()
                case 3:
                    print (f'Cima : {pila_acciones.cima()}')
                case 4:
                    pila_acciones.mostrar()
                case 5:
                    print (f'Tamanio de la pila : {pila_acciones.tamanio()}')
                case 6:
                    if pila_acciones.esta_vacia():
                        print('Pila vacia')
                    else :
                        print('Pila no vacia')
                        mostrar_estado()
                case 0 :
                    print('Menu cerrado exitosamente')
                    break
                case _ :
                    print('Opcion fuera de ramgp')

        except Exception as e:
            print(f"Error ({type(e).__name__}): {e}")

def ejecutar() -> None:
    submenu_pila()


if __name__ == "__main__":
    ejecutar()