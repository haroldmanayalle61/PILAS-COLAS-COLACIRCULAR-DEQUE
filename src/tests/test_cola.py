import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cola import Cola
from modelos import Solicitud
from ui_cola import codigo_duplicado, cola_solicitudes

class TestCola(unittest.TestCase):

    def test_cola_inicialmente_vacia(self) -> None:
        cola = Cola[int]()

        self.assertTrue(cola.esta_vacia())
        self.assertEqual(cola.tamanio(), 0)


    def test_encolar_un_elemento(self) -> None:
        cola = Cola[int]()

        cola.encolar(10)

        self.assertFalse(cola.esta_vacia())
        self.assertEqual(cola.tamanio(), 1)
        self.assertEqual(cola.frente(), 10)


    def test_encolar_varios_elementos(self) -> None:
        cola = Cola[int]()

        cola.encolar(10)
        cola.encolar(20)
        cola.encolar(30)

        self.assertEqual(cola.tamanio(), 3)
        self.assertEqual(cola.frente(), 10)


    def test_fifo(self) -> None:
        """
        FIFO:
        First In, First Out.
        El primero en entrar debe ser el primero en salir.
        """

        cola = Cola[str]()

        cola.encolar("A")
        cola.encolar("B")
        cola.encolar("C")

        self.assertEqual(cola.desencolar(), "A")
        self.assertEqual(cola.desencolar(), "B")
        self.assertEqual(cola.desencolar(), "C")


    def test_frente_no_elimina(self) -> None:
        cola = Cola[int]()

        cola.encolar(10)
        cola.encolar(20)

        valor = cola.frente()

        self.assertEqual(valor, 10)
        self.assertEqual(cola.tamanio(), 2)


    def test_desencolar_actualiza_frente(self) -> None:
        cola = Cola[int]()

        cola.encolar(10)
        cola.encolar(20)
        cola.encolar(30)

        eliminado = cola.desencolar()

        self.assertEqual(eliminado, 10)
        self.assertEqual(cola.frente(), 20)
        self.assertEqual(cola.tamanio(), 2)


    def test_vaciado_completo(self) -> None:
        cola = Cola[int]()

        cola.encolar(10)
        cola.encolar(20)

        cola.desencolar()
        cola.desencolar()

        self.assertTrue(cola.esta_vacia())
        self.assertEqual(cola.tamanio(), 0)


    def test_reutilizar_despues_de_vaciar(self) -> None:
        """
        Comprueba indirectamente que frente y final
        se reiniciaron correctamente al vaciar la cola.
        """

        cola = Cola[int]()

        cola.encolar(10)
        cola.desencolar()

        self.assertTrue(cola.esta_vacia())

        cola.encolar(99)

        self.assertEqual(cola.frente(), 99)
        self.assertEqual(cola.tamanio(), 1)


    def test_underflow_desencolar(self) -> None:
        cola = Cola[int]()

        with self.assertRaises(IndexError):
            cola.desencolar()


    def test_underflow_consultar_frente(self) -> None:
        cola = Cola[int]()

        with self.assertRaises(IndexError):
            cola.frente()


    def test_fifo_despues_de_encolar_y_desencolar(self) -> None:
        """
        Secuencia parecida a la requerida:
        S01, S02, S03, retirar y luego agregar S04.
        """

        cola = Cola[str]()

        cola.encolar("S01")
        cola.encolar("S02")
        cola.encolar("S03")

        self.assertEqual(cola.frente(), "S01")

        self.assertEqual(cola.desencolar(), "S01")

        cola.encolar("S04")

        self.assertEqual(cola.desencolar(), "S02")
        self.assertEqual(cola.desencolar(), "S03")
        self.assertEqual(cola.desencolar(), "S04")

        self.assertTrue(cola.esta_vacia())


    def test_solicitud_guarda_datos(self) -> None:
        solicitud = Solicitud(
            "S01",
            "Juan",
            "Problema de acceso",
            "08:30"
        )

        self.assertEqual(solicitud.codigo, "S01")
        self.assertEqual(solicitud.solicitante, "Juan")
        self.assertEqual(solicitud.descripcion, "Problema de acceso")
        self.assertEqual(solicitud.hora_llegada, "08:30")


    def test_codigo_duplicado(self) -> None:
        # Limpiar la cola global por si quedó algo de otra prueba
        while not cola_solicitudes.esta_vacia():
            cola_solicitudes.desencolar()

        solicitud = Solicitud(
            "S01",
            "Ana",
            "Problema con contraseña",
            "09:00"
        )

        cola_solicitudes.encolar(solicitud)

        self.assertTrue(codigo_duplicado("S01"))
        self.assertFalse(codigo_duplicado("S02"))


    def test_codigo_disponible_despues_de_atender(self) -> None:
        # Limpiar la cola global
        while not cola_solicitudes.esta_vacia():
            cola_solicitudes.desencolar()

        solicitud = Solicitud(
            "S01",
            "Pedro",
            "Problema de conexión",
            "10:00"
        )

        cola_solicitudes.encolar(solicitud)

        self.assertTrue(codigo_duplicado("S01"))

        cola_solicitudes.desencolar()

        self.assertFalse(codigo_duplicado("S01"))   


if __name__ == "__main__":
    unittest.main(verbosity=2)
