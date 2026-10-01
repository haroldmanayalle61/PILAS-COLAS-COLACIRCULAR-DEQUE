import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from deque_tad import Deque


class PruebasDeque(unittest.TestCase):

    def setUp(self) -> None:
        self.deque: Deque[int] = Deque()

    def test_deque_inicialmente_vacio(self) -> None:
        self.assertTrue(self.deque.esta_vacio())
        self.assertEqual(self.deque.tamanio(), 0)

    def test_insertar_un_elemento_frente(self) -> None:
        self.deque.insertar_frente(10)

        self.assertFalse(self.deque.esta_vacio())
        self.assertEqual(self.deque.tamanio(), 1)
        self.assertEqual(self.deque.consultar_frente(), 10)
        self.assertEqual(self.deque.consultar_final(), 10)

    def test_insertar_un_elemento_final(self) -> None:
        self.deque.insertar_final(20)

        self.assertFalse(self.deque.esta_vacio())
        self.assertEqual(self.deque.tamanio(), 1)
        self.assertEqual(self.deque.consultar_frente(), 20)
        self.assertEqual(self.deque.consultar_final(), 20)

    def test_insertar_por_ambos_extremos(self) -> None:
        self.deque.insertar_final(20)
        self.deque.insertar_final(30)
        self.deque.insertar_frente(10)

        self.assertEqual(self.deque.tamanio(), 3)
        self.assertEqual(self.deque.consultar_frente(), 10)
        self.assertEqual(self.deque.consultar_final(), 30)

    def test_consultar_ambos_extremos(self) -> None:
        self.deque.insertar_final(10)
        self.deque.insertar_final(20)
        self.deque.insertar_final(30)

        self.assertEqual(self.deque.consultar_frente(), 10)
        self.assertEqual(self.deque.consultar_final(), 30)

    def test_eliminar_frente(self) -> None:
        self.deque.insertar_final(10)
        self.deque.insertar_final(20)
        self.deque.insertar_final(30)

        self.assertEqual(self.deque.eliminar_frente(), 10)
        self.assertEqual(self.deque.tamanio(), 2)
        self.assertEqual(self.deque.consultar_frente(), 20)
        self.assertEqual(self.deque.consultar_final(), 30)

    def test_eliminar_final(self) -> None:
        self.deque.insertar_final(10)
        self.deque.insertar_final(20)
        self.deque.insertar_final(30)

        self.assertEqual(self.deque.eliminar_final(), 30)
        self.assertEqual(self.deque.tamanio(), 2)
        self.assertEqual(self.deque.consultar_frente(), 10)
        self.assertEqual(self.deque.consultar_final(), 20)

    def test_uno_a_cero_eliminando_frente(self) -> None:
        self.deque.insertar_frente(10)

        self.assertEqual(self.deque.eliminar_frente(), 10)
        self.assertTrue(self.deque.esta_vacio())
        self.assertEqual(self.deque.tamanio(), 0)

    def test_uno_a_cero_eliminando_final(self) -> None:
        self.deque.insertar_final(10)

        self.assertEqual(self.deque.eliminar_final(), 10)
        self.assertTrue(self.deque.esta_vacio())
        self.assertEqual(self.deque.tamanio(), 0)

    def test_varios_a_uno(self) -> None:
        self.deque.insertar_final(10)
        self.deque.insertar_final(20)
        self.deque.insertar_final(30)
        self.deque.insertar_frente(5)

        self.assertEqual(self.deque.tamanio(), 4)

        self.assertEqual(self.deque.eliminar_frente(), 5)
        self.assertEqual(self.deque.eliminar_final(), 30)
        self.assertEqual(self.deque.eliminar_final(), 20)

        self.assertEqual(self.deque.tamanio(), 1)
        self.assertEqual(self.deque.consultar_frente(), 10)
        self.assertEqual(self.deque.consultar_final(), 10)

    def test_vaciado_completo(self) -> None:
        self.deque.insertar_final(10)
        self.deque.insertar_final(20)
        self.deque.insertar_final(30)

        self.assertEqual(self.deque.eliminar_frente(), 10)
        self.assertEqual(self.deque.eliminar_final(), 30)
        self.assertEqual(self.deque.eliminar_frente(), 20)

        self.assertTrue(self.deque.esta_vacio())
        self.assertEqual(self.deque.tamanio(), 0)

    # ---- Pruebas nuevas: verifican los enlaces anterior/siguiente ----

    def test_insertar_frente_y_eliminar_final(self) -> None:
        # Si insertar_frente no enlaza bien "anterior", eliminar_final falla.
        for valor in (1, 2, 3):
            self.deque.insertar_frente(valor)

        self.assertEqual(self.deque.eliminar_final(), 1)
        self.assertEqual(self.deque.eliminar_final(), 2)
        self.assertEqual(self.deque.eliminar_final(), 3)
        self.assertTrue(self.deque.esta_vacio())

    def test_insertar_final_y_eliminar_frente(self) -> None:
        # Si insertar_final no enlaza bien "siguiente", eliminar_frente falla.
        for valor in (1, 2, 3):
            self.deque.insertar_final(valor)

        self.assertEqual(self.deque.eliminar_frente(), 1)
        self.assertEqual(self.deque.eliminar_frente(), 2)
        self.assertEqual(self.deque.eliminar_frente(), 3)
        self.assertTrue(self.deque.esta_vacio())

    def test_reutilizacion_tras_vaciar(self) -> None:
        # Tras quedar vacio, frente y final deben reiniciarse correctamente.
        self.deque.insertar_final(1)
        self.deque.eliminar_final()
        self.deque.insertar_frente(2)

        self.assertEqual(self.deque.tamanio(), 1)
        self.assertEqual(self.deque.consultar_frente(), 2)
        self.assertEqual(self.deque.consultar_final(), 2)

    def test_mostrar_orden(self) -> None:
        for valor in (10, 20, 30):
            self.deque.insertar_final(valor)

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            self.deque.mostrar()

        self.assertEqual(
            buffer.getvalue().splitlines(),
            ["1. 10", "2. 20", "3. 30"],
        )

    # ---- Underflow ----

    def test_eliminar_frente_deque_vacio(self) -> None:
        with self.assertRaises(IndexError):
            self.deque.eliminar_frente()

    def test_eliminar_final_deque_vacio(self) -> None:
        with self.assertRaises(IndexError):
            self.deque.eliminar_final()

    def test_consultar_frente_deque_vacio(self) -> None:
        with self.assertRaises(IndexError):
            self.deque.consultar_frente()

    def test_consultar_final_deque_vacio(self) -> None:
        with self.assertRaises(IndexError):
            self.deque.consultar_final()

    def test_mostrar_no_modifica_el_deque(self) -> None:
        self.deque.insertar_final(10)
        self.deque.insertar_final(20)
        self.deque.insertar_final(30)

        tamanio_antes = self.deque.tamanio()
        frente_antes = self.deque.consultar_frente()
        final_antes = self.deque.consultar_final()

        with redirect_stdout(io.StringIO()):
            self.deque.mostrar()

        self.assertEqual(self.deque.tamanio(), tamanio_antes)
        self.assertEqual(self.deque.consultar_frente(), frente_antes)
        self.assertEqual(self.deque.consultar_final(), final_antes)


if __name__ == "__main__":
    unittest.main(verbosity=2)