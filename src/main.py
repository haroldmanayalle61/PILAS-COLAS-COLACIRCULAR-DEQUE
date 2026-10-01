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
    print("4. Demostrar Cola Circular [PENDIENTE]")
    print("5. Demostrar Deque")
    print("6. Ejecutar pruebas [PENDIENTE]")
    print("7. Salir")
    print("=" * 45)

def main() -> None:
    while True:
        mostrar_menu_principal()
        opcion = input("\nSeleccione una opción general: ").strip()

        try:
            if opcion == "1":
                ui_pila.ejecutar()
                
            elif opcion == "2":
                ui_expresiones.ejecutar()
                
            elif opcion == "3":
                ui_cola.ejecutar()
                
            elif opcion == "4":
                print("\n[AVISO] El módulo de Cola Circular está en desarrollo por Harold.")
                
            elif opcion == "5":
                ui_deque.ejecutar()
                
            elif opcion == "6":
                import pruebas
                pruebas.ejecutar_pruebas()
                
            elif opcion == "7":
                print("\nCerrando el sistema integrador.")
                break
                
            else:
                print("\nError: Opción inválida. Ingrese un número del 1 al 7.")
                
        except Exception as e:
            # Capturamos cualquier error no previsto para que el menú no colapse
            print(f"\n[ERROR CRÍTICO] El submenú falló con el error: {e}")

if __name__ == "__main__":
    main()
