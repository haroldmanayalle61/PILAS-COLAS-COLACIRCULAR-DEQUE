import unittest
from conversiones import infija_a_postfija, infija_a_prefija

class TestConversiones(unittest.TestCase):

    def test_todas_las_conversiones(self):
        print("\n" + "="*50)
        print("    INICIANDO PRUEBAS DE CONVERSIONES ")
        print("="*50)

        # 1. Traza 1 (Postfija)
        exp1 = "A + B * (C - D)"
        res1 = infija_a_postfija(exp1)
        print(f"\n[1] Probando Postfija: '{exp1}'")
        print(f"    -> Resultado: '{res1}'")
        assert res1 == "A B C D - * +"
        print("    OK!")

        # 2. Traza 2 (Prefija)
        exp2 = "(A + B) * (C - D)"
        res2 = infija_a_prefija(exp2)
        print(f"\n[2] Probando Prefija : '{exp2}'")
        print(f"    -> Resultado: '{res2}'")
        assert res2 == "* + A B - C D"
        print("    OK!")

        # 3. Paréntesis anidados
        exp3 = "((A + B) * C)"
        res3 = infija_a_postfija(exp3)
        print(f"\n[3] Probando Anidados: '{exp3}'")
        print(f"    -> Resultado: '{res3}'")
        assert res3 == "A B + C *"
        print("    OK!")

        # 4. Potencia encadenada (Asociatividad derecha)
        exp4 = "2 ^ 3 ^ 2"
        res4_post = infija_a_postfija(exp4)
        res4_pre = infija_a_prefija(exp4)
        print(f"\n[4] Probando Potencia: '{exp4}'")
        print(f"    -> Postfija: '{res4_post}'")
        print(f"    -> Prefija : '{res4_pre}'")
        assert res4_post == "2 3 2 ^ ^"
        assert res4_pre == "^ 2 ^ 3 2"
        print("    OK!")

        # 5. Detección de error de sintaxis
        exp5 = "(A + B * C"
        print(f"\n[5] Probando Error Sintaxis: '{exp5}'")
        try:
            infija_a_postfija(exp5)
            assert False, "Debió fallar"
        except ValueError as e:
            print(f"    -> Captura de error correcta: '{e}'")
            assert True
            print("    OK!")

        print("\n" + "="*50)
        print(" ¡TODAS LAS PRUEBAS PASARON SATISFACTORIAMENTE!")
        print("="*50 + "\n")

if __name__ == '__main__':
    unittest.main()