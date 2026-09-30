from evaluaciones import evaluar_postfija, evaluar_prefija


def mostrar_menu() -> None:
    print("\n==============================")
    print("   EVALUACIÓN DE EXPRESIONES")
    print("==============================")
    print("1. Evaluar expresión postfija")
    print("2. Evaluar expresión prefija")
    print("3. Salir")


def evaluar_postfija_ui() -> None:
    print("\n--- Evaluación postfija ---")
    print("Ejemplo: 8 2 / 3 -")

    expresion = input("Ingrese la expresión postfija: ")

    try:
        resultado = evaluar_postfija(expresion)
        print(f"Resultado: {resultado}")

    except (ZeroDivisionError, ValueError) as error:
        print(f"Error: {error}")


def evaluar_prefija_ui() -> None:
    print("\n--- Evaluación prefija ---")
    print("Ejemplo: - / 8 2 3")

    expresion = input("Ingrese la expresión prefija: ")

    try:
        resultado = evaluar_prefija(expresion)
        print(f"Resultado: {resultado}")

    except (ZeroDivisionError, ValueError) as error:
        print(f"Error: {error}")


def ejecutar() -> None:
    while True:

        mostrar_menu()

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            evaluar_postfija_ui()

        elif opcion == "2":
            evaluar_prefija_ui()

        elif opcion == "3":
            print("\nSaliendo del módulo de expresiones...")
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")


if __name__ == "__main__":
    ejecutar()
