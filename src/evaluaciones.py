from math import isfinite
from typing import Iterable

from pila import Pila
import tokens


def es_numero(token: str) -> bool:
    """Acepta valores reales finitos; rechaza nan e infinitos."""
    try:
        return isfinite(float(token))
    except ValueError:
        return False


def convertir_numero(token: str) -> float:
    numero = float(token)
    if not isfinite(numero):
        raise ValueError('El operando debe ser un número real finito')
    return numero


def operar(a: float, b: float, operador: str) -> float:
    """Calcula a operador b y controla resultados fuera del dominio real."""
    try:
        match operador:
            case '+':
                resultado = a + b
            case '-':
                resultado = a - b
            case '*':
                resultado = a * b
            case '/':
                if b == 0:
                    raise ZeroDivisionError('No se puede dividir entre cero')
                resultado = a / b
            case '^':
                if a == 0 and b < 0:
                    raise ZeroDivisionError('Cero no puede elevarse a una potencia negativa')
                resultado = a ** b
            case _:
                raise ValueError(f'Operador inválido: {operador}')
    except OverflowError as error:
        raise ValueError('El resultado excede el rango numérico admitido') from error

    if isinstance(resultado, complex) or not isfinite(resultado):
        raise ValueError('El resultado debe ser un número real finito')
    return float(resultado)


def _evaluar(secuencia: Iterable[str], prefija: bool) -> float:
    pila = Pila[float]()
    leyo_token = False
    for token in secuencia:
        leyo_token = True
        if es_numero(token):
            pila.apilar(convertir_numero(token))
        elif tokens.es_operador(token):
            if pila.tamanio() < 2:
                raise ValueError('Operandos insuficientes')
            primero = pila.desapilar()
            segundo = pila.desapilar()
            a, b = (primero, segundo) if prefija else (segundo, primero)
            pila.apilar(operar(a, b, token))
        else:
            raise ValueError(f'Token inválido: {token}')

    if not leyo_token:
        raise ValueError('La expresión está vacía')
    if pila.tamanio() != 1:
        raise ValueError('La expresión tiene operandos sobrantes')
    return pila.desapilar()


def evaluar_postfija(expresion: str) -> float:
    """Lee de izquierda a derecha; extrae derecho antes que izquierdo."""
    return _evaluar(tokens.iterar_tokens_separados(expresion), prefija=False)


def evaluar_prefija(expresion: str) -> float:
    """Lee de derecha a izquierda usando la pila propia para invertir tokens."""
    entrada = Pila[str]()
    for token in tokens.iterar_tokens_separados(expresion):
        entrada.apilar(token)
    return _evaluar(entrada, prefija=True)
