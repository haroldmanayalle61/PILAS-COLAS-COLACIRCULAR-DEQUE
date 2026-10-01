from expresiones import (
    infija_a_postfija,
    infija_a_prefija,
    evaluar_postfija,
    evaluar_prefija,
)


def mostrar_menu() -> None:
    print("\n===================================")
    print("      PROCESAMIENTO DE EXPRESIONES")
    print("===================================")
    print("1. Convertir infija a postfija")
    print("2. Convertir infija a prefija")
    print("3. Evaluar expresión postfija")
    print("4. Evaluar expresión prefija")
    print("5. Salir")


def convertir_postfija_ui() -> None:
    print("\n--- INFIJA A POSTFIJA ---")

    expresion = input(
        "Ingrese la expresión infija: "
    ).strip()

    try:
        resultado = infija_a_postfija(expresion)

        print(
            f"Expresión postfija: {resultado}"
        )

    except ValueError as error:
        print(f"Error: {error}")


def convertir_prefija_ui() -> None:
    print("\n--- INFIJA A PREFIJA ---")

    expresion = input(
        "Ingrese la expresión infija: "
    ).strip()

    try:
        resultado = infija_a_prefija(expresion)

        print(
            f"Expresión prefija: {resultado}"
        )

    except ValueError as error:
        print(f"Error: {error}")


def evaluar_postfija_ui() -> None:
    print("\n--- EVALUAR POSTFIJA ---")
    print("Ejemplo: 8 2 / 3 -")

    expresion = input(
        "Ingrese la expresión postfija: "
    ).strip()

    try:
        resultado = evaluar_postfija(expresion)

        print(f"Resultado: {resultado}")

    except (ZeroDivisionError, ValueError) as error:
        print(f"Error: {error}")


def evaluar_prefija_ui() -> None:
    print("\n--- EVALUAR PREFIJA ---")
    print("Ejemplo: - / 8 2 3")

    expresion = input(
        "Ingrese la expresión prefija: "
    ).strip()

    try:
        resultado = evaluar_prefija(expresion)

        print(f"Resultado: {resultado}")

    except (ZeroDivisionError, ValueError) as error:
        print(f"Error: {error}")


def ejecutar() -> None:

    while True:

        mostrar_menu()

        opcion = input(
            "\nSeleccione una opción: "
        ).strip()

        if opcion == "1":
            convertir_postfija_ui()

        elif opcion == "2":
            convertir_prefija_ui()

        elif opcion == "3":
            evaluar_postfija_ui()

        elif opcion == "4":
            evaluar_prefija_ui()

        elif opcion == "5":
            print(
                "\nSaliendo del módulo de expresiones..."
            )
            break

        else:
            print(
                "\nOpción inválida. Intente nuevamente."
            )


if __name__ == "__main__":
    ejecutar()