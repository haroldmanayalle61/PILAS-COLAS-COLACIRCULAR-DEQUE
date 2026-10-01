from deque_tad import Deque
 
def leer_entero(mensaje: str) -> int:
    cadena: str = input(mensaje).strip()
    try:
        return int(cadena)
    except ValueError:
        raise ValueError("Ingrese un número entero") from None
 
 
def mostrar_estado(deque_actual: Deque[str]) -> None:
    deque_actual.mostrar()
    print(f"Tamaño: {deque_actual.tamanio()}")
 
    if deque_actual.esta_vacio():
        print("Frente: ninguno")
        print("Final: ninguno")
    else:
        print(f"Frente: {deque_actual.consultar_frente()}")
        print(f"Final: {deque_actual.consultar_final()}")
 
 
def demo_como_pila() -> None:
    print("--- Demostracion: Deque usado como Pila (LIFO) ---")
    print("Se usan insertar_final y eliminar_final, igual que apilar/desapilar.")

    deque_demo = Deque()

    for tarea in ("Tarea A", "Tarea B", "Tarea C"):
        deque_demo.insertar_final(tarea)
        print(f"Insertada al final: {tarea}")
        mostrar_estado(deque_demo)
 
    while not deque_demo.esta_vacio():
        valor = deque_demo.eliminar_final()
        print(f"Eliminada del final (LIFO): {valor}")
        mostrar_estado(deque_demo)
 
 
def demo_como_cola() -> None:
    print("--- Demostracion: Deque usado como Cola (FIFO) ---")
    print("Se usan insertar_final y eliminar_frente, igual que encolar/desencolar.")

    deque_demo = Deque()

    for tarea in ("Tarea A", "Tarea B", "Tarea C"):
        deque_demo.insertar_final(tarea)
        print(f"Insertada al final: {tarea}")
        mostrar_estado(deque_demo)
 
    while not deque_demo.esta_vacio():
        valor = deque_demo.eliminar_frente()
        print(f"Eliminada del frente (FIFO): {valor}")
        mostrar_estado(deque_demo)
 
 
def demo_combinado() -> None:
    print("--- Demostracion: Uso combinado del Deque ---")

    deque_demo = Deque()

    deque_demo.insertar_final("Tarea normal 1")
    mostrar_estado(deque_demo)
    deque_demo.insertar_frente("Tarea urgente 1")
    mostrar_estado(deque_demo)
    deque_demo.insertar_final("Tarea normal 2")
    mostrar_estado(deque_demo)
 
    valor = deque_demo.eliminar_frente()
    print(f"Se atiende primero la mas urgente: {valor}")
    mostrar_estado(deque_demo)
 
    valor = deque_demo.eliminar_final()
    print(f"Se cancela la ultima tarea agregada: {valor}")
    mostrar_estado(deque_demo)
 
 
def submenu_deque() -> None:

    deque_planificador: Deque[str] = Deque()

    while True:
        try:
            print(f'{"="*10}SUBMENU - PLANIFICADOR FLEXIBLE (DEQUE){"="*10}')
            print('1. Insertar tarea urgente (frente)')
            print('2. Insertar tarea normal (final)')
            print('3. Atender siguiente tarea (eliminar frente)')
            print('4. Cancelar ultima tarea agregada (eliminar final)')
            print('5. Consultar la tarea mas urgente (frente)')
            print('6. Consultar la ultima tarea agregada (final)')
            print('7. Mostrar el deque completo')
            print('8. Consultar el tamanio')
            print('9. Comprobar si esta vacio')
            print('10. Demostracion: uso como pila (LIFO)')
            print('11. Demostracion: uso como cola (FIFO)')
            print('12. Demostracion: uso combinado')
            print('0. Cerrar submenu')
            opcion = leer_entero('Ingrese una opcion: ')
 
            match opcion:
                case 1:
                    tarea = input('Ingrese la tarea urgente: ').strip()
                    if tarea == "":
                        raise ValueError('La tarea no puede estar vacia')
                    deque_planificador.insertar_frente(tarea)
                    mostrar_estado(deque_planificador)
                case 2:
                    tarea = input('Ingrese la tarea normal: ').strip()
                    if tarea == "":
                        raise ValueError('La tarea no puede estar vacia')
                    deque_planificador.insertar_final(tarea)
                    mostrar_estado(deque_planificador)
                case 3:
                    valor = deque_planificador.eliminar_frente()
                    print(f'Tarea atendida: {valor}')
                    mostrar_estado(deque_planificador)
                case 4:
                    valor = deque_planificador.eliminar_final()
                    print(f'Tarea cancelada: {valor}')
                    mostrar_estado(deque_planificador)
                case 5:
                    print(f'Tarea mas urgente: {deque_planificador.consultar_frente()}')
                case 6:
                    print(f'Ultima tarea agregada: {deque_planificador.consultar_final()}')
                case 7:
                    deque_planificador.mostrar()
                case 8:
                    print(f'Tamanio del deque: {deque_planificador.tamanio()}')
                case 9:
                    if deque_planificador.esta_vacio():
                        print('Deque vacio')
                    else:
                        print('Deque no vacio')
                        mostrar_estado(deque_planificador)
                case 10:
                    demo_como_pila()
                case 11:
                    demo_como_cola()
                case 12:
                    demo_combinado()
                case 0:
                    print('Menu cerrado exitosamente')
                    break
                case _:
                    print('Opcion fuera de rango')
 
        except (ValueError, IndexError, OverflowError) as e:
            print(f"Error ({type(e).__name__}): {e}")
 
 
def ejecutar() -> None:
    submenu_deque()
 
 
if __name__ == "__main__":
    ejecutar()
