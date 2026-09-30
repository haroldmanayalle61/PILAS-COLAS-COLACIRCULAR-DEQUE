from typing import List

OPERADORES = {'+', '-', '*', '/', '^'}
PARENTESIS = {'(', ')'}
SEPARADORES = {' ', '\t'}


def es_operador(token: str) -> bool:
    if token in OPERADORES:
        return True
    else:
        return False

def es_parentesis(token: str) -> bool:
    if token in PARENTESIS:
        return True
    else:
        return False

def es_letra_o_digito(caracter: str) -> bool:
    #Devuelve True si el caracter es una letra (A-Z, a-z) o un digito (0-9).
    if ('a' <= caracter <= 'z') or ('A' <= caracter <= 'Z') or ('0' <= caracter <= '9'):
        return True
    else:
        return False

def obtener_jerarquia(operador: str) -> int:
    #jerarquia de operadores
    if operador == '^':
        return 3
    elif operador in ('*', '/'):
        return 2
    elif operador in ('+', '-'):
        return 1
    else:
        return 0


def es_asociativo_derecha(operador: str) -> bool:
    #Devuelve True solo si el operador asocia por la derecha (^).
    if operador == '^':
        return True
    else:
        return False


def es_operando_valido(token: str) -> bool:
    #Valida que el token sea un identificador o un número bien formado.
    cuerpo = token[1:] if token[0] == '-' else token
    if cuerpo == "":
        return False
    if ('0' <= cuerpo[0] <= '9') or cuerpo[0] == '.':
        try:
            float(cuerpo)
            return True
        except ValueError:
            return False
    for caracter in cuerpo:
        if not es_letra_o_digito(caracter):
            return False
    return True


def dividir_tokens(expresion: str) -> List[str]:
    #Descompone la cadena en una lista de tokens.
    tokens: List[str] = []
    actual = ""

    for caracter in expresion:
        # El espacio separa tokens; no se elimina, para que "A B" no se una
        if caracter in SEPARADORES:
            if actual:
                tokens.append(actual)
                actual = ""
            continue

        # Un '-' es signo de número negativo si no hay operando antes
        es_negativo = (caracter == '-') and (not actual) and (
            not tokens or tokens[-1] in OPERADORES or tokens[-1] == '('
        )

        if es_letra_o_digito(caracter) or caracter == '.' or es_negativo:
            actual += caracter
        elif es_operador(caracter) or es_parentesis(caracter):
            if actual:
                tokens.append(actual)
                actual = ""
            tokens.append(caracter)
        else:
            raise ValueError(f"Error de sintaxis: Carácter no reconocido '{caracter}'")

    if actual:
        tokens.append(actual)

    if not tokens:
        raise ValueError("Error de sintaxis: La expresión está vacía.")

    return tokens


def validar_sintaxis(tokens: List[str]) -> None:
    #Lanza ValueError si la secuencia de tokens no es una expresión válida.
    espera_operando = True
    nivel = 0  # paréntesis abiertos pendientes de cerrar

    for token in tokens:
        if token == '(':
            if not espera_operando:
                raise ValueError("Error de sintaxis: Falta operador antes de '('")
            nivel += 1
        elif token == ')':
            if espera_operando:
                raise ValueError("Error de sintaxis: Paréntesis ')' inesperado")
            nivel -= 1
            if nivel < 0:
                raise ValueError("Error de sintaxis: Paréntesis desbalanceados")
        elif es_operador(token):
            if espera_operando:
                raise ValueError(f"Error de sintaxis: Operador inesperado '{token}'")
            espera_operando = True
        else:  # operando (variable o número)
            if not es_operando_valido(token):
                raise ValueError(f"Error de sintaxis: Operando inválido '{token}'")
            if not espera_operando:
                raise ValueError(f"Error de sintaxis: Falta operador antes de '{token}'")
            espera_operando = False

    if nivel != 0:
        raise ValueError("Error de sintaxis: Paréntesis desbalanceados")
    if espera_operando:
        raise ValueError("Error de sintaxis: La expresión no puede terminar con un operador")