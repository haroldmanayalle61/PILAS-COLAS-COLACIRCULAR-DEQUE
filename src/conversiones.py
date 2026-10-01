import tokens
from pila import Pila


def infija_a_postfija(expresion: str) -> str:
    """Convierte infija a postfija usando exclusivamente pilas propias."""
    tokens.validar_sintaxis(tokens.dividir_tokens(expresion))
    operadores = Pila[str]()
    salida = Pila[str]()

    for token in tokens.dividir_tokens(expresion):
        if not tokens.es_operador(token) and not tokens.es_parentesis(token):
            salida.apilar(token)
        elif token == '(':
            operadores.apilar(token)
        elif token == ')':
            while not operadores.esta_vacia() and operadores.cima() != '(':
                salida.apilar(operadores.desapilar())
            operadores.desapilar()  # La validación previa garantiza la apertura.
        else:
            prioridad = tokens.obtener_jerarquia(token)
            while not operadores.esta_vacia() and operadores.cima() != '(':
                prioridad_cima = tokens.obtener_jerarquia(operadores.cima())
                if prioridad_cima > prioridad or (
                    prioridad_cima == prioridad
                    and not tokens.es_asociativo_derecha(token)
                ):
                    salida.apilar(operadores.desapilar())
                else:
                    break
            operadores.apilar(token)

    while not operadores.esta_vacia():
        salida.apilar(operadores.desapilar())

    # Dos pilas conservan el orden de emisión sin una lista auxiliar.
    salida_ordenada = Pila[str]()
    while not salida.esta_vacia():
        salida_ordenada.apilar(salida.desapilar())
    return ' '.join(salida_ordenada)


def infija_a_prefija(expresion: str) -> str:
    """Invierte el recorrido mediante Pila y respeta la asociatividad."""
    tokens.validar_sintaxis(tokens.dividir_tokens(expresion))
    entrada_invertida = Pila[str]()
    for token in tokens.dividir_tokens(expresion):
        if token == '(':
            entrada_invertida.apilar(')')
        elif token == ')':
            entrada_invertida.apilar('(')
        else:
            entrada_invertida.apilar(token)

    operadores = Pila[str]()
    salida = Pila[str]()
    while not entrada_invertida.esta_vacia():
        token = entrada_invertida.desapilar()
        if not tokens.es_operador(token) and not tokens.es_parentesis(token):
            salida.apilar(token)
        elif token == '(':
            operadores.apilar(token)
        elif token == ')':
            while not operadores.esta_vacia() and operadores.cima() != '(':
                salida.apilar(operadores.desapilar())
            operadores.desapilar()
        else:
            prioridad = tokens.obtener_jerarquia(token)
            while not operadores.esta_vacia() and operadores.cima() != '(':
                prioridad_cima = tokens.obtener_jerarquia(operadores.cima())
                # Al recorrer al revés se invierte la regla de desempate.
                if prioridad_cima > prioridad or (
                    prioridad_cima == prioridad
                    and tokens.es_asociativo_derecha(token)
                ):
                    salida.apilar(operadores.desapilar())
                else:
                    break
            operadores.apilar(token)

    while not operadores.esta_vacia():
        salida.apilar(operadores.desapilar())
    # El recorrido de cima a base invierte la salida auxiliar.
    return ' '.join(salida)
