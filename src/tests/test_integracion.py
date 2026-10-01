import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main
import pruebas
import ui_circular
import ui_cola
import ui_pila
from cola import Cola
from cola_circular import ColaCircular
from modelos import Solicitud
from pila import Pila


class TestIntegracion(unittest.TestCase):
    def setUp(self) -> None:
        for modulo, atributo, valor in (
            (ui_pila, 'pila_acciones', Pila[str]()),
            (ui_circular, 'cola_enteros', None),
            (ui_circular, 'cola_cadenas', None),
            (ui_cola, 'cola_solicitudes', Cola[Solicitud]()),
        ):
            cambio = patch.object(modulo, atributo, valor)
            cambio.start()
            self.addCleanup(cambio.stop)

    def ejecutar_menu(self, entradas: tuple[str, ...]) -> str:
        salida = io.StringIO()
        respuestas = iter(entradas)

        def responder(mensaje: str = '') -> str:
            try:
                return next(respuestas)
            except StopIteration:
                raise EOFError from None

        with patch('builtins.input', side_effect=responder) as lectura:
            with redirect_stdout(salida), redirect_stderr(salida):
                main.main()
        self.assertEqual(lectura.call_count, len(entradas), 'El menú pidió una entrada inesperada')
        self.assertNotIn('ERROR CRÍTICO', salida.getvalue())
        return salida.getvalue()

    def test_main_abre_circular_y_muestra_vacio_al_retirar(self) -> None:
        salida = self.ejecutar_menu(('4', '1', '5', '1', '28', '2', '4', '0', '7'))
        self.assertIn('SUBMENU - COLA CIRCULAR', salida)
        self.assertIn('Captura retirada: 28', salida)
        self.assertIn('Frente: ninguno', salida)
        self.assertIn('Tamanio: 0', salida)
        self.assertNotIn('Error', salida)
        self.assertTrue(ui_circular.cola_enteros.esta_vacia())

    def test_circular_puede_cancelar_sin_crear_cola(self) -> None:
        self.ejecutar_menu(('4', '0', '7'))
        self.assertIsNone(ui_circular.cola_enteros)
        self.assertIsNone(ui_circular.cola_cadenas)

    def test_circular_cambia_tipo_y_conserva_cada_buffer(self) -> None:
        salida = self.ejecutar_menu((
            '4', '1', '5', '1', '8', '0',
            '4', '2', '5', '1', '007', '0',
            '4', '1', '3', '2', '0', '7',
        ))
        self.assertIn('Captura retirada: 8', salida)
        self.assertTrue(ui_circular.cola_enteros.esta_vacia())
        self.assertEqual(ui_circular.cola_cadenas.consultar_frente(), '007')
        self.assertNotIn('Error', salida)

    def test_circular_recupera_datos_invalidos_y_underflow(self) -> None:
        salida = self.ejecutar_menu((
            '4', '9', 'x', '1', '0', '1', '-1', '1', 'texto',
            '1', '5', '1', 'x', '1', '7', '3', '4', '5', '6', '7',
            '2', '2', '0', '7',
        ))
        self.assertIn('Error (ValueError)', salida)
        self.assertIn('Error (IndexError)', salida)
        self.assertIn('Captura retirada: 7', salida)
        self.assertTrue(ui_circular.cola_enteros.esta_vacia())

    def test_circular_wrap_around_overflow_y_vaciado_desde_main(self) -> None:
        salida = self.ejecutar_menu((
            '4', '1', '5', '1', '10', '1', '20', '1', '30', '2', '2',
            '1', '40', '1', '50', '1', '60', '1', '70', '1', '80',
            '2', '2', '2', '2', '2', '0', '7',
        ))
        self.assertEqual(salida.count('Error (OverflowError)'), 1)
        self.assertNotIn('Error (IndexError)', salida)
        retirados = [line for line in salida.splitlines() if line.startswith('Captura retirada:')]
        self.assertEqual(retirados, [f'Captura retirada: {n}' for n in (10, 20, 30, 40, 50, 60, 70)])
        self.assertTrue(ui_circular.cola_enteros.esta_vacia())

    def test_circular_cadena_vacia_no_se_registra(self) -> None:
        salida = self.ejecutar_menu(('4', '2', '5', '1', ' ', '1', 'texto', '2', '0', '7'))
        self.assertIn('La captura no puede estar vacia', salida)
        self.assertIn('Captura retirada: texto', salida)
        self.assertTrue(ui_circular.cola_cadenas.esta_vacia())

    def test_pila_operaciones_y_visualizacion_al_vaciar(self) -> None:
        salida = self.ejecutar_menu(('1', '4', '1', 'A', '3', '5', '6', '2', '4', '6', '0', '7'))
        self.assertIn('Accion deshecha: A', salida)
        self.assertIn('Cima: ninguna', salida)
        self.assertIn('Tamanio: 0', salida)
        self.assertNotIn('Error', salida)
        self.assertTrue(ui_pila.pila_acciones.esta_vacia())

    def test_pila_datos_invalidos_underflow_y_reutilizacion(self) -> None:
        salida = self.ejecutar_menu(('x', '1', 'x', '9', '1', ' ', '2', '3', '1', 'B', '2', '0', '7'))
        self.assertIn('Opción inválida', salida)
        self.assertIn('Error (ValueError)', salida)
        self.assertIn('Error (IndexError)', salida)
        self.assertIn('Accion deshecha: B', salida)

    def test_cola_registra_duplica_consulta_y_atiende(self) -> None:
        salida = self.ejecutar_menu((
            '3', '1', 's01', 'Ana', 'Consulta',
            '1', 'S01', 'Luis', 'Duplicada', '2', '4', '5',
            '3', '4', '5', '6', '7',
        ))
        self.assertIn('pendiente con ese código', salida)
        self.assertIn('Solicitud atendida correctamente', salida)
        self.assertIn('No existen solicitudes pendientes', salida)
        self.assertIn('Solicitudes pendientes: 0', salida)
        self.assertTrue(ui_cola.cola_solicitudes.esta_vacia())

    def test_cola_rechaza_campos_vacios_y_controla_underflow(self) -> None:
        salida = self.ejecutar_menu(('3', '1', '', 'Ana', 'Consulta', '2', '3', '6', '7'))
        self.assertIn('Todos los campos son obligatorios', salida)
        self.assertEqual(salida.count('Cola vacía'), 2)
        self.assertTrue(ui_cola.cola_solicitudes.esta_vacia())

    def test_deque_todas_las_operaciones_y_demostraciones(self) -> None:
        salida = self.ejecutar_menu((
            '5', '7', '1', 'Urgente', '2', 'Normal', '5', '6', '7', '8', '9',
            '3', '4', '9', '10', '11', '12', '0', '7',
        ))
        self.assertIn('Tarea atendida: Urgente', salida)
        self.assertIn('Tarea cancelada: Normal', salida)
        self.assertIn('Uso combinado', salida)
        self.assertNotIn('Error', salida)

    def test_deque_datos_invalidos_y_underflow_controlados(self) -> None:
        salida = self.ejecutar_menu(('5', 'x', '99', '1', ' ', '3', '4', '5', '6', '0', '7'))
        self.assertIn('Error (ValueError)', salida)
        self.assertEqual(salida.count('Error (IndexError)'), 4)

    def test_expresiones_cuatro_funciones_y_recuperacion_de_errores(self) -> None:
        salida = self.ejecutar_menu((
            '2', 'x', '1', '(A+B', '1', 'A + B * (C - D)',
            '2', '(A+B)*(C-D)', '3', '8 0 /', '3', '8 2 / 3 -',
            '4', '^ -2 0.5', '4', '- / 8 2 3', '5', '7',
        ))
        self.assertIn('A B C D - * +', salida)
        self.assertIn('* + A B - C D', salida)
        self.assertIn('No se puede dividir entre cero', salida)
        self.assertIn('número real finito', salida)
        self.assertEqual(salida.count('Resultado: 1.0'), 2)

    def test_menu_pruebas_dispatch_y_etiqueta(self) -> None:
        with patch.object(pruebas, 'ejecutar_pruebas') as ejecutar:
            salida = self.ejecutar_menu(('6', '7'))
        ejecutar.assert_called_once_with()
        self.assertNotIn('PENDIENTE', salida)

    def test_ejecutor_usa_rutas_absolutas(self) -> None:
        with patch.object(pruebas.unittest, 'TestLoader') as loader:
            with patch.object(pruebas.unittest, 'TextTestRunner') as runner:
                runner.return_value.run.return_value.wasSuccessful.return_value = True
                with redirect_stdout(io.StringIO()):
                    pruebas.ejecutar_pruebas()
        carpeta = Path(pruebas.__file__).resolve().parent
        loader.return_value.discover.assert_called_once_with(
            start_dir=str(carpeta / 'tests'), pattern='test_*.py', top_level_dir=str(carpeta),
        )

    def test_fin_de_entrada_cierra_main(self) -> None:
        salida = io.StringIO()
        with patch('builtins.input', side_effect=EOFError), redirect_stdout(salida):
            main.main()
        self.assertIn('Cerrando el sistema integrador', salida.getvalue())

    def test_interrupcion_en_submenu_cierra_main(self) -> None:
        salida = io.StringIO()
        with patch('builtins.input', side_effect=('1', KeyboardInterrupt)), redirect_stdout(salida):
            main.main()
        self.assertIn('Cerrando el sistema integrador', salida.getvalue())
        self.assertNotIn('ERROR CRÍTICO', salida.getvalue())


if __name__ == '__main__':
    unittest.main(verbosity=2)
