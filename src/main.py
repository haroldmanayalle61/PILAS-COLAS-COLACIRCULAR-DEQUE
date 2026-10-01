import ui_pila
import ui_expresiones
import ui_cola
import ui_deque
import ui_circular
import pruebas

def mostrar_menu_principal() -> None:
    print("\n" + "=" * 45)
    print("      CENTRO DE SERVICIOS DIGITALES")
    print("=" * 45)
    print("1. Demostrar Pila")
    print("2. Procesar expresiones")
    print("3. Demostrar Cola")
    print("4. Demostrar Cola Circular")
    print("5. Demostrar Deque")
    print("6. Ejecutar pruebas")
    print("7. Salir")
    print("=" * 45)

def main() -> None:
    while True:
        try:
            mostrar_menu_principal()
            opcion = input("\nSeleccione una opción general: ").strip()
            if opcion == "1":
                ui_pila.ejecutar()
                
            elif opcion == "2":
                ui_expresiones.ejecutar()
                
            elif opcion == "3":
                ui_cola.ejecutar()
                
            elif opcion == "4":
                ui_circular.ejecutar()
                
            elif opcion == "5":
                ui_deque.ejecutar()
                
            elif opcion == "6":
                pruebas.ejecutar_pruebas()
                
            elif opcion == "7":
                print("\nCerrando el sistema integrador.")
                break
                
            else:
                print("\nError: Opción inválida. Ingrese un número del 1 al 7.")
                
        except (EOFError, KeyboardInterrupt):
            print("\nCerrando el sistema integrador.")
            break
        except Exception as e:
            # Capturamos cualquier error no previsto para que el menú no colapse
            print(f"\n[ERROR CRÍTICO] El submenú falló con el error: {e}")

if __name__ == "__main__":
    main()
