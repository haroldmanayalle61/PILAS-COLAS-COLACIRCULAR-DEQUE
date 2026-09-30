from pila import Pila

#Operadores permitidos
OPERADORES = ['+', '-', '*', '/', '^']


def es_numero(token: str) -> bool:
    """Verifica si un token representa un numero entero o decimal."""

    try:
        float(token)
        return True
    except ValueError:
        return False


def es_operador(token: str) -> bool:
    """Verifica si el token es un operador valido."""    
    return token in OPERADORES


def operar(a: int|float, b: int|float, operador: str) -> int|float:
    """Realiza la operacion matematica entre dos numeros segun el operador."""
    match operador:
        case '+':
            return a + b
        case '-':
            return a - b
        case '*':
            return a * b
        case '/':
            if b == 0:
                raise ZeroDivisionError("Division por cero")
            return a / b
        case '^':
            return a ** b
        case _:
            raise ValueError(f"Operador no valido: {operador}")

def convertir_numero(token: str) -> int|float:
    # sourcery skip: assign-if-exp, reintroduce-else
    """Convierte un token a numero entero o decimal."""

    numero = float(token)

    #Si es entero devuelve int
    if numero.is_integer():
        return int(numero)

    return numero


def evaluar_postfija(expresion: str) -> int|float:
    """Evalua una expresion en notacion postfija y devuelve el resultado."""

    pila = Pila()

    tokens = expresion.split()

    for token in tokens:

        #Si es numero
        if es_numero(token):
            pila.apilar(convertir_numero(token))

        #Si es operador
        elif es_operador(token):

            try:
                b = pila.desapilar()
                a = pila.desapilar()

            except IndexError:

                raise ValueError("Expresion invalida: no hay suficientes operandos para el operador")

            resultado = operar(a, b, token)
            pila.apilar(resultado)

        else:
            raise ValueError(f"Token no valido: {token}")

    #Debe quedar solo un resultado
    if pila.tamanio() != 1:
        raise ValueError("Expresion invalida: quedan operandos sin operar")    

    return pila.desapilar()  


def evaluar_prefija(expresion: str) -> int|float:
    """Evalua una expresion en notacion prefija y devuelve el resultado."""

    pila = Pila()

    tokens = expresion.split()

    #Prefija se lee de derecha a izquierda

    for token in reversed(tokens):

        #Si es numero
        if es_numero(token):
            pila.apilar(convertir_numero(token))

        #Si es operador
        elif es_operador(token):

            try:
                a = pila.desapilar()
                b = pila.desapilar()

            except IndexError:

                raise ValueError("Expresion invalida: no hay suficientes operandos para el operador")

            resultado = operar(a, b, token)
            pila.apilar(resultado)

        else:
            raise ValueError(f"Token no valido: {token}")

    if pila.tamanio() != 1:
        raise ValueError("Expresion invalida: quedan operandos sin operar")

    return pila.desapilar()