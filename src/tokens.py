import re
from typing import Iterable, Iterator

OPERADORES = {'+', '-', '*', '/', '^'}
PARENTESIS = {'(', ')'}


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
    return operador == '^'


def es_operando_valido(token: str) -> bool:
    #Valida que el token sea un identificador o un número bien formado.
    if not token:
        return False
    cuerpo = token[1:] if token[0] == '-' else token
    if cuerpo == "":
        return False
    if ('0' <= cuerpo[0] <= '9') or cuerpo[0] == '.':
        try:
            float(cuerpo)
            return True
        except ValueError:
            return False
    if token.startswith('-'):
        return False  # El signo se admite en números, no en identificadores.
    for caracter in cuerpo:
        if not es_letra_o_digito(caracter):
            return False
    return True


def dividir_tokens(expresion: str) -> Iterator[str]:
    # Emite tokens sin almacenarlos en una lista de Python.
    actual = ""
    anterior = ""
    emitio_token = False

    for caracter in expresion:
        # El espacio separa tokens; no se elimina, para que "A B" no se una
        if caracter.isspace():
            if actual:
                yield actual
                anterior = actual
                emitio_token = True
                actual = ""
            continue

        # Un '-' es signo de número negativo si no hay operando antes
        es_negativo = (caracter == '-') and (not actual) and (
            not anterior or anterior in OPERADORES or anterior == '('
        )

        if es_letra_o_digito(caracter) or caracter == '.' or es_negativo:
            actual += caracter
        elif es_operador(caracter) or es_parentesis(caracter):
            if actual:
                yield actual
                anterior = actual
                emitio_token = True
                actual = ""
            yield caracter
            anterior = caracter
            emitio_token = True
        else:
            raise ValueError(f"Error de sintaxis: Carácter no reconocido '{caracter}'")

    if actual:
        yield actual
        emitio_token = True

    if not emitio_token:
        raise ValueError("Error de sintaxis: La expresión está vacía.")


def iterar_tokens_separados(expresion: str) -> Iterator[str]:
    """Lee operandos y operadores separados por espacios sin usar split()."""
    for coincidencia in re.finditer(r'\S+', expresion):
        yield coincidencia.group()


def validar_sintaxis(tokens: Iterable[str]) -> None:
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
