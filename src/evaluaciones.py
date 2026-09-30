from pila import Pila
import tokens


def es_numero(token: str) -> bool:
    """
    Verifica si un token representa un número válido.
    """

    try:
        float(token)
        return True

    except ValueError:
        return False


def convertir_numero(token: str) -> int | float:
    """
    Convierte un token a entero o decimal.
    """

    numero = float(token)

    return int(numero) if numero.is_integer() else numero


def operar(
    a: int | float,
    b: int | float,
    operador: str
) -> int | float:
    """
    Realiza la operación indicada entre dos operandos.

    El orden siempre es:
    a operador b
    """

    match operador:

        case "+":
            return a + b

        case "-":
            return a - b

        case "*":
            return a * b

        case "/":
            if b == 0:
                raise ZeroDivisionError(
                    "No se puede dividir entre cero"
                )

            return a / b

        case "^":
            return a ** b

        case _:
            raise ValueError(
                f"Operador inválido: {operador}"
            )


def evaluar_postfija(expresion: str) -> int | float:
    """
    Evalúa una expresión en notación postfija.

    Ejemplo:
    8 2 / 3 -

    Resultado:
    1
    """

    pila = Pila[int | float]()
    lista_tokens = expresion.split()

    if not lista_tokens:
        raise ValueError(
            "La expresión está vacía"
        )

    for token in lista_tokens:

        if es_numero(token):

            pila.apilar(
                convertir_numero(token)
            )

        elif tokens.es_operador(token):

            if pila.tamanio() < 2:
                raise ValueError(
                    "Operandos insuficientes"
                )

            b = pila.desapilar()
            a = pila.desapilar()

            resultado = operar(
                a,
                b,
                token
            )

            pila.apilar(resultado)

        else:

            raise ValueError(
                f"Token inválido: {token}"
            )

    if pila.tamanio() != 1:

        raise ValueError(
            "La expresión tiene operandos sobrantes"
        )

    return pila.desapilar()


def evaluar_prefija(expresion: str) -> int | float:
    """
    Evalúa una expresión en notación prefija.

    Ejemplo:
    - / 8 2 3

    Resultado:
    1
    """

    pila = Pila[int | float]()
    lista_tokens = expresion.split()

    if not lista_tokens:
        raise ValueError(
            "La expresión está vacía"
        )

    for token in reversed(lista_tokens):

        if es_numero(token):

            pila.apilar(
                convertir_numero(token)
            )

        elif tokens.es_operador(token):

            if pila.tamanio() < 2:
                raise ValueError(
                    "Operandos insuficientes"
                )

            a = pila.desapilar()
            b = pila.desapilar()

            resultado = operar(
                a,
                b,
                token
            )

            pila.apilar(resultado)

        else:

            raise ValueError(
                f"Token inválido: {token}"
            )

    if pila.tamanio() != 1:

        raise ValueError(
            "La expresión tiene operandos sobrantes"
        )

    return pila.desapilar()