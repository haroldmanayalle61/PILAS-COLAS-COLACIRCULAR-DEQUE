import sys
import unittest
from pathlib import Path

# Permite ejecutar el archivo directamente desde la carpeta tests.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cola_circular import ColaCircular

class PruebasColaCircular(unittest.TestCase):
    def setUp(self) -> None:
        self.cola: ColaCircular[int] = ColaCircular(10)

    def test_cola_inicialmente_vacia(self) -> None:
        self.assertTrue(self.cola.esta_vacia())
        self.assertEqual(self.cola.tamanio(), 0)
        self.assertFalse(self.cola.esta_llena())

    def test_un_elemento(self) -> None:
        self.cola.encolar(10)
        self.assertEqual(self.cola.frente(), 10)
        self.assertIs(type(self.cola.frente()), int)
        self.assertEqual(self.cola.tamanio(), 1)
        self.assertFalse(self.cola.esta_vacia())

    def test_varios_elementos_fifo(self) -> None:
        for dato in (10, 20, 30):
            self.cola.encolar(dato)
        self.assertEqual(self.cola.frente(), 10)
        self.assertEqual(self.cola.tamanio(), 3)
        for esperado in (10, 20, 30):
            self.assertEqual(self.cola.desencolar(), esperado)
        self.assertTrue(self.cola.esta_vacia())
        self.assertEqual(self.cola.tamanio(), 0)

    def test_reutilizacion_y_vaciado(self) -> None:
        for dato in range(10, 100, 10):
            self.cola.encolar(dato)
        self.assertFalse(self.cola.esta_llena())
        self.assertEqual(self.cola.desencolar(), 10)
        self.assertEqual(self.cola.desencolar(), 20)
        self.cola.encolar(100)  # El indice final vuelve a cero.
        self.cola.encolar(110)
        self.cola.encolar(120)
        self.assertEqual(self.cola.frente(), 30)
        self.assertEqual(self.cola.tamanio(), 10)
        self.assertTrue(self.cola.esta_llena())
        for esperado in range(30, 130, 10):
            self.assertEqual(self.cola.desencolar(), esperado)
        self.assertTrue(self.cola.esta_vacia())
        self.assertEqual(self.cola.tamanio(), 0)

    def test_overflow(self) -> None:
        for dato in range(10, 110, 10):
            self.cola.encolar(dato)
        with self.assertRaises(OverflowError):
            self.cola.encolar(110)
        self.assertEqual(self.cola.tamanio(), 10)
        self.assertEqual(self.cola.frente(), 10)

    def test_underflow(self) -> None:
        with self.assertRaises(IndexError):
            self.cola.desencolar()

    def test_frente_vacio(self) -> None:
        with self.assertRaises(IndexError):
            self.cola.frente()

    def test_cadenas(self) -> None:
        cola_texto: ColaCircular[str] = ColaCircular(10)
        cola_texto.encolar("007")
        cola_texto.encolar("Captura")
        self.assertEqual(cola_texto.frente(), "007")
        self.assertIs(type(cola_texto.frente()), str)
        self.assertEqual(cola_texto.desencolar(), "007")
        self.assertEqual(cola_texto.desencolar(), "Captura")
        self.assertTrue(cola_texto.esta_vacia())

    def test_capacidad_no_positiva(self) -> None:
        for capacidad in (0, -1):
            with self.assertRaises(ValueError):
                ColaCircular[int](capacidad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
