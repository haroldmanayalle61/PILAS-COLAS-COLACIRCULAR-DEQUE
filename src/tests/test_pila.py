import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pila import Pila


class PruebasPila(unittest.TestCase):
    def setUp(self) -> None:
        self.pila: Pila[int] = Pila()

    def test_pila_inicialmente_vacia(self) -> None:
        self.assertTrue(self.pila.esta_vacia())
        self.assertEqual(self.pila.tamanio(), 0)

    def test_un_elemento(self) -> None:
        self.pila.apilar(10)
        self.assertEqual(self.pila.cima(), 10)
        self.assertEqual(self.pila.tamanio(), 1)

    def test_varios_elementos(self) -> None:
        for dato in (10, 20, 30):
            self.pila.apilar(dato)

        self.assertEqual(self.pila.cima(), 30)
        self.assertEqual(self.pila.tamanio(), 3)

    def test_vaciado_en_orden_lifo(self) -> None:
        for dato in (10, 20, 30):
            self.pila.apilar(dato)

        self.assertEqual(self.pila.desapilar(), 30)
        self.assertEqual(self.pila.desapilar(), 20)
        self.assertEqual(self.pila.desapilar(), 10)
        self.assertTrue(self.pila.esta_vacia())
        self.assertEqual(self.pila.tamanio(), 0)

    def test_desapilar_pila_vacia(self) -> None:
        with self.assertRaises(IndexError):
            self.pila.desapilar()

    def test_consultar_cima_vacia(self) -> None:
        with self.assertRaises(IndexError):
            self.pila.cima()


if __name__ == "__main__":
    unittest.main(verbosity=2)