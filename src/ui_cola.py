from cola import Cola
from modelos import Solicitud


cola_solicitudes = Cola[Solicitud]()


def codigo_duplicado(codigo: str) -> bool:
    """
    Comprueba si existe una solicitud pendiente
    con el mismo código.
    """

    return any(solicitud.codigo == codigo for solicitud in cola_solicitudes)


def registrar_solicitud() -> None:

    print("\n--- REGISTRAR SOLICITUD ---")

    codigo = input("Código: ").strip().upper()
    solicitante = input("Solicitante: ").strip()
    descripcion = input("Descripción: ").strip()


    # Validar datos vacíos

    if codigo == "" or solicitante == "" or descripcion == "":
        print("\nError: Todos los campos son obligatorios.")
        return


    # Validar código duplicado

    if codigo_duplicado(codigo):
        print(
            "\nError: Ya existe una solicitud "
            "pendiente con ese código."
        )
        return


    solicitud = Solicitud(
        codigo,
        solicitante,
        descripcion
    )


    cola_solicitudes.encolar(solicitud)


    print("\nSolicitud registrada correctamente.")
    print(solicitud)


def consultar_proxima() -> None:

    print("\n--- PRÓXIMA SOLICITUD ---")

    try:

        solicitud = cola_solicitudes.frente()

        print(solicitud)

    except IndexError as error:

        print(f"Error: {error}")


def atender_solicitud() -> None:

    print("\n--- ATENDER SOLICITUD ---")

    try:

        solicitud = cola_solicitudes.desencolar()

        print("Solicitud atendida correctamente:")
        print(solicitud)

    except IndexError as error:

        print(f"Error: {error}")


def mostrar_solicitudes() -> None:

    print("\n--- SOLICITUDES PENDIENTES ---")


    if cola_solicitudes.esta_vacia():

        print("No existen solicitudes pendientes.")
        return


    for posicion, solicitud in enumerate(cola_solicitudes, start=1):

        print(f"\nSolicitud {posicion}")
        print(solicitud)


def mostrar_cantidad() -> None:

    print(
        f"\nSolicitudes pendientes: "
        f"{cola_solicitudes.tamanio()}"
    )


def mostrar_menu() -> None:

    print("\n==============================")
    print("       MESA DE AYUDA")
    print("==============================")

    print("1. Registrar solicitud")
    print("2. Consultar próxima solicitud")
    print("3. Atender solicitud")
    print("4. Mostrar solicitudes pendientes")
    print("5. Mostrar cantidad de solicitudes")
    print("6. Salir")


def ejecutar() -> None:

    while True:

        mostrar_menu()

        opcion = input(
            "\nSeleccione una opción: "
        ).strip()


        if opcion == "1":

            registrar_solicitud()


        elif opcion == "2":

            consultar_proxima()


        elif opcion == "3":

            atender_solicitud()


        elif opcion == "4":

            mostrar_solicitudes()


        elif opcion == "5":

            mostrar_cantidad()


        elif opcion == "6":

            print(
                "\nSaliendo de la mesa de ayuda..."
            )

            break


        else:

            print(
                "\nOpción inválida. Intente nuevamente."
            )


if __name__ == "__main__":
    ejecutar()