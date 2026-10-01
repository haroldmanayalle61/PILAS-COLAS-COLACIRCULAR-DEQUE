import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluaciones import evaluar_postfija, evaluar_prefija
from evaluaciones import evaluar_postfija, evaluar_prefija
from conversiones import infija_a_postfija, infija_a_prefija

class TestEvaluaciones(unittest.TestCase):

    # =========================================================
    # PRUEBAS DE EVALUACIÓN POSTFIJA
    # =========================================================

    def test_postfija_obligatoria(self) -> None:
        """
        Expresión obligatoria de la guía:
        8 2 / 3 - = 1
        """
        resultado = evaluar_postfija("8 2 / 3 -")
        self.assertEqual(resultado, 1.0)


    def test_postfija_suma(self) -> None:
        resultado = evaluar_postfija("5 3 +")
        self.assertEqual(resultado, 8)


    def test_postfija_resta(self) -> None:
        resultado = evaluar_postfija("10 3 -")
        self.assertEqual(resultado, 7)


    def test_postfija_division(self) -> None:
        resultado = evaluar_postfija("20 5 /")
        self.assertEqual(resultado, 4.0)


    def test_postfija_potencia(self) -> None:
        resultado = evaluar_postfija("2 3 ^")
        self.assertEqual(resultado, 8)


    def test_postfija_decimal(self) -> None:
        resultado = evaluar_postfija("2.5 1.5 +")
        self.assertAlmostEqual(resultado, 4.0)


    # =========================================================
    # PRUEBAS DE EVALUACIÓN PREFIJA
    # =========================================================

    def test_prefija_obligatoria(self) -> None:
        """
        Expresión obligatoria de la guía:
        - / 8 2 3 = 1
        """
        resultado = evaluar_prefija("- / 8 2 3")
        self.assertEqual(resultado, 1.0)


    def test_prefija_suma(self) -> None:
        resultado = evaluar_prefija("+ 5 3")
        self.assertEqual(resultado, 8)


    def test_prefija_resta(self) -> None:
        resultado = evaluar_prefija("- 10 3")
        self.assertEqual(resultado, 7)


    def test_prefija_division(self) -> None:
        resultado = evaluar_prefija("/ 20 5")
        self.assertEqual(resultado, 4.0)


    def test_prefija_potencia(self) -> None:
        resultado = evaluar_prefija("^ 2 3")
        self.assertEqual(resultado, 8)


    def test_prefija_decimal(self) -> None:
        resultado = evaluar_prefija("+ 2.5 1.5")
        self.assertAlmostEqual(resultado, 4.0)


    # =========================================================
    # PRUEBAS DE ERRORES
    # =========================================================

    def test_division_entre_cero_postfija(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            evaluar_postfija("5 0 /")


    def test_division_entre_cero_prefija(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            evaluar_prefija("/ 5 0")


    def test_token_invalido_postfija(self) -> None:
        with self.assertRaises(ValueError):
            evaluar_postfija("5 hola +")


    def test_token_invalido_prefija(self) -> None:
        with self.assertRaises(ValueError):
            evaluar_prefija("+ 5 hola")


    def test_operandos_insuficientes_postfija(self) -> None:
        with self.assertRaises(ValueError):
            evaluar_postfija("5 +")


    def test_operandos_insuficientes_prefija(self) -> None:
        with self.assertRaises(ValueError):
            evaluar_prefija("+ 5")


    def test_operandos_sobrantes_postfija(self) -> None:
        with self.assertRaises(ValueError):
            evaluar_postfija("8 2 3 +")


    def test_operandos_sobrantes_prefija(self) -> None:
        with self.assertRaises(ValueError):
            evaluar_prefija("+ 8 2 3")


    def test_integracion_postfija(self) -> None:
        expresion_infija = "8 / 2 - 3"

        postfija = infija_a_postfija(expresion_infija)
        resultado = evaluar_postfija(postfija)

        self.assertEqual(postfija, "8 2 / 3 -")
        self.assertEqual(resultado, 1.0)


    def test_integracion_prefija(self) -> None:
        expresion_infija = "8 / 2 - 3"

        prefija = infija_a_prefija(expresion_infija)
        resultado = evaluar_prefija(prefija)

        self.assertEqual(prefija, "- / 8 2 3")
        self.assertEqual(resultado, 1.0)


    def test_integracion_potencia(self) -> None:
        expresion_infija = "2 ^ 3 ^ 2"

        postfija = infija_a_postfija(expresion_infija)
        resultado = evaluar_postfija(postfija)

        self.assertEqual(postfija, "2 3 2 ^ ^")
        self.assertEqual(resultado, 512)


if __name__ == "__main__":
    unittest.main(verbosity=2)