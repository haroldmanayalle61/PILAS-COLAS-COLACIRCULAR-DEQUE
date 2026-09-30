from typing import List

import tokens
from pila import Pila


def infija_a_postfija(expresion: str) -> str:
    """Convierte una expresión en notación infija a notación postfija."""
    lista_tokens = tokens.dividir_tokens(expresion)
    tokens.validar_sintaxis(lista_tokens)

    pila = Pila[str]()
    salida: List[str] = []

    for token in lista_tokens:
        if not tokens.es_operador(token) and not tokens.es_parentesis(token):
            salida.append(token)
        elif token == '(':
            pila.apilar(token)
        elif token == ')':
            while not pila.esta_vacia() and pila.cima() != '(':
                salida.append(pila.desapilar())
            if pila.esta_vacia():
                raise ValueError("Error de sintaxis: Paréntesis desbalanceados")
            pila.desapilar()  # descarta el '('
        else:  # operador
            prec_actual = tokens.obtener_jerarquia(token)
            while not pila.esta_vacia() and pila.cima() != '(':
                prec_cima = tokens.obtener_jerarquia(pila.cima())
                if (prec_cima > prec_actual) or (
                    prec_cima == prec_actual and not tokens.es_asociativo_derecha(token)
                ):
                    salida.append(pila.desapilar())
                else:
                    break
            pila.apilar(token)

    while not pila.esta_vacia():
        top = pila.desapilar()
        if tokens.es_parentesis(top):
            raise ValueError("Error de sintaxis: Paréntesis desbalanceados")
        salida.append(top)

    return " ".join(salida)


def infija_a_prefija(expresion: str) -> str:
    """Convierte una expresión en notación infija a notación prefija."""
    lista_tokens = tokens.dividir_tokens(expresion)
    tokens.validar_sintaxis(lista_tokens)

    # Se invierte la expresión intercambiando '(' y ')'
    tokens_invertidos: List[str] = []
    for token in reversed(lista_tokens):
        if token == '(':
            tokens_invertidos.append(')')
        elif token == ')':
            tokens_invertidos.append('(')
        else:
            tokens_invertidos.append(token)

    pila = Pila[str]()
    salida: List[str] = []

    for token in tokens_invertidos:
        if not tokens.es_operador(token) and not tokens.es_parentesis(token):
            salida.append(token)
        elif token == '(':
            pila.apilar(token)
        elif token == ')':
            while not pila.esta_vacia() and pila.cima() != '(':
                salida.append(pila.desapilar())
            if pila.esta_vacia():
                raise ValueError("Error de sintaxis: Paréntesis desbalanceados")
            pila.desapilar()  # descarta el '('
        else:  # operador
            prec_actual = tokens.obtener_jerarquia(token)
            while not pila.esta_vacia() and pila.cima() != '(':
                prec_cima = tokens.obtener_jerarquia(pila.cima())
                # Al ir invertido, la asociatividad se comporta al revés
                if (prec_cima > prec_actual) or (
                    prec_cima == prec_actual and tokens.es_asociativo_derecha(token)
                ):
                    salida.append(pila.desapilar())
                else:
                    break
            pila.apilar(token)

    while not pila.esta_vacia():
        top = pila.desapilar()
        if tokens.es_parentesis(top):
            raise ValueError("Error de sintaxis: Paréntesis desbalanceados")
        salida.append(top)

    salida.reverse()
    return " ".join(salida)