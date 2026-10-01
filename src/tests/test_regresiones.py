import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cola_circular import ColaCircular
from conversiones import infija_a_postfija, infija_a_prefija
from evaluaciones import evaluar_postfija, evaluar_prefija
from pila import Pila
from tokens import es_operando_valido


class TestRegresiones(unittest.TestCase):
    def test_mostrar_estructuras_vacias_no_genera_underflow(self) -> None:
        for tad in (Pila[str](), ColaCircular[int](5)):
            with self.subTest(tad=type(tad).__name__), redirect_stdout(io.StringIO()) as salida:
                tad.mostrar()
                self.assertIn('vacia', salida.getvalue())
                self.assertEqual(tad.tamanio(), 0)

    def test_iteracion_pila_conserva_datos_y_cima(self) -> None:
        pila = Pila[int]()
        for valor in (10, 20, 30):
            pila.apilar(valor)
        self.assertEqual(tuple(pila), (30, 20, 10))
        self.assertEqual(pila.tamanio(), 3)
        self.assertEqual(pila.cima(), 30)
        self.assertEqual(tuple(pila.desapilar() for _ in range(3)), (30, 20, 10))
        self.assertEqual(tuple(pila), ())

    def test_consultar_frente_conserva_elemento_y_alias(self) -> None:
        cola = ColaCircular[str](5)
        with self.assertRaises(IndexError):
            cola.consultar_frente()
        cola.encolar('007')
        self.assertEqual(cola.consultar_frente(), '007')
        self.assertEqual(cola.frente(), '007')
        self.assertEqual(cola.tamanio(), 1)
        self.assertEqual(cola.desencolar(), '007')

    def test_capacidad_rechaza_bool_y_tipos_no_enteros(self) -> None:
        for capacidad in (True, False, '5', 5.0, None):
            with self.subTest(capacidad=capacidad), self.assertRaises(ValueError):
                ColaCircular(capacidad)

    def test_evaluaciones_devuelven_float(self) -> None:
        for evaluar, expresion in (
            (evaluar_postfija, '5'), (evaluar_prefija, '5'),
            (evaluar_postfija, '5 3 +'), (evaluar_prefija, '+ 5 3'),
        ):
            with self.subTest(expresion=expresion):
                self.assertIs(type(evaluar(expresion)), float)

    def test_evaluaciones_rechazan_no_finitos(self) -> None:
        for evaluar in (evaluar_postfija, evaluar_prefija):
            for token in ('nan', 'NaN', 'inf', '-inf', '1e309'):
                with self.subTest(evaluar=evaluar.__name__, token=token), self.assertRaises(ValueError):
                    evaluar(token)

    def test_resultados_fuera_del_dominio_real_controlados(self) -> None:
        for evaluar, expresion in (
            (evaluar_postfija, '-2 0.5 ^'), (evaluar_prefija, '^ -2 0.5'),
            (evaluar_postfija, '10 1000 ^'), (evaluar_prefija, '^ 10 1000'),
            (evaluar_postfija, '1e308 1e308 *'), (evaluar_prefija, '* 1e308 1e308'),
        ):
            with self.subTest(expresion=expresion), self.assertRaises(ValueError):
                evaluar(expresion)

    def test_cero_con_potencia_negativa_controlado(self) -> None:
        for evaluar, expresion in ((evaluar_postfija, '0 -1 ^'), (evaluar_prefija, '^ 0 -1')):
            with self.subTest(expresion=expresion), self.assertRaises(ZeroDivisionError):
                evaluar(expresion)

    def test_conversiones_asociatividad_y_parentesis(self) -> None:
        for infija, postfija, prefija, resultado in (
            ('10 - 3 - 2', '10 3 - 2 -', '- - 10 3 2', 5.0),
            ('20 / 5 / 2', '20 5 / 2 /', '/ / 20 5 2', 2.0),
            ('2 ^ 3 ^ 2', '2 3 2 ^ ^', '^ 2 ^ 3 2', 512.0),
            ('(2 ^ 3) ^ 2', '2 3 ^ 2 ^', '^ ^ 2 3 2', 64.0),
            ('((2.5 + 1.5) * 3) - 8 / 2', '2.5 1.5 + 3 * 8 2 / -', '- * + 2.5 1.5 3 / 8 2', 8.0),
            ('-2 * (3 - -4)', '-2 3 -4 - *', '* -2 - 3 -4', -14.0),
        ):
            with self.subTest(infija=infija):
                self.assertEqual(infija_a_postfija(infija), postfija)
                self.assertEqual(infija_a_prefija(infija), prefija)
                self.assertEqual(evaluar_postfija(postfija), resultado)
                self.assertEqual(evaluar_prefija(prefija), resultado)

    def test_conversion_y_evaluacion_aceptan_espacios_y_saltos(self) -> None:
        infija = '\n8\t / 2\n - 3\r\n'
        self.assertEqual(evaluar_postfija(infija_a_postfija(infija)), 1.0)
        self.assertEqual(evaluar_prefija(infija_a_prefija(infija)), 1.0)

    def test_conversiones_rechazan_sintaxis_invalida(self) -> None:
        for convertir in (infija_a_postfija, infija_a_prefija):
            for expresion in ('', ' ', 'A B', '()', '(A+B', 'A+B)', 'A+@', 'A+', '-A', '2..3+1', '2(3+1)'):
                with self.subTest(expresion=expresion), self.assertRaises(ValueError):
                    convertir(expresion)
        self.assertFalse(es_operando_valido(''))

    def test_conversiones_coinciden_con_calculo_independiente(self) -> None:
        for a, b, c, d in ((9, 8, 2, 3), (-4, 7, 2, 0.5), (5.25, -3.5, 7, -2)):
            infija = f'{a} - {b} / {c} * {d}'
            esperado = a - b / c * d
            with self.subTest(infija=infija):
                self.assertAlmostEqual(evaluar_postfija(infija_a_postfija(infija)), esperado)
                self.assertAlmostEqual(evaluar_prefija(infija_a_prefija(infija)), esperado)


if __name__ == '__main__':
    unittest.main(verbosity=2)
