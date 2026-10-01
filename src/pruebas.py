import unittest
from pathlib import Path

def ejecutar_pruebas() -> None:
    print("\n" + "=" * 45)
    print("      EJECUCIÓN GLOBAL DE PRUEBAS")
    print("=" * 45)
    cargador = unittest.TestLoader()
    carpeta_src = Path(__file__).resolve().parent
    suite = cargador.discover(
        start_dir=str(carpeta_src / 'tests'),
        pattern='test_*.py',
        top_level_dir=str(carpeta_src),
    )
    # 2. Ejecuta la suite completa (verbosity=2 muestra el detalle de cada prueba en consola)
    corredor = unittest.TextTestRunner(verbosity=2)
    resultado = corredor.run(suite)
    
    print("=" * 45)
    if resultado.wasSuccessful():
        print("ESTADO FINAL: Todas las pruebas integradas pasaron con éxito.")
    else:
        print(f"ESTADO FINAL: Se encontraron {len(resultado.failures)} fallos y {len(resultado.errors)} errores.")
        print("Revisa los módulos de tus compañeros.")

if __name__ == "__main__":
    ejecutar_pruebas()
