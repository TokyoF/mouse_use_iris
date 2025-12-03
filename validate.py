"""
Script de validación del sistema
Verifica que todos los módulos se puedan importar correctamente
"""
import sys
import io
from pathlib import Path

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Prueba que todos los módulos se importen correctamente"""
    print("=" * 60)
    print("VALIDACIÓN DE MÓDULOS")
    print("=" * 60)

    tests = []

    # Test database
    try:
        from src.database.db_manager import DatabaseManager
        print("✓ DatabaseManager")
        tests.append(("DatabaseManager", True, None))
    except Exception as e:
        print(f"✗ DatabaseManager: {e}")
        tests.append(("DatabaseManager", False, str(e)))

    # Test auth
    try:
        from src.auth.face_auth import FaceAuthenticator
        print("✓ FaceAuthenticator")
        tests.append(("FaceAuthenticator", True, None))
    except Exception as e:
        print(f"✗ FaceAuthenticator: {e}")
        tests.append(("FaceAuthenticator", False, str(e)))

    try:
        from src.auth.user_manager import UserManager
        print("✓ UserManager")
        tests.append(("UserManager", True, None))
    except Exception as e:
        print(f"✗ UserManager: {e}")
        tests.append(("UserManager", False, str(e)))

    # Test core
    try:
        from src.core.filters import OneEuro, EMA, DeadzoneFilter
        print("✓ Filters (OneEuro, EMA, DeadzoneFilter)")
        tests.append(("Filters", True, None))
    except Exception as e:
        print(f"✗ Filters: {e}")
        tests.append(("Filters", False, str(e)))

    try:
        from src.core.face_detector import FaceDetector
        print("✓ FaceDetector")
        tests.append(("FaceDetector", True, None))
    except Exception as e:
        print(f"✗ FaceDetector: {e}")
        tests.append(("FaceDetector", False, str(e)))

    try:
        from src.core.gaze_tracker import GazeTracker
        print("✓ GazeTracker")
        tests.append(("GazeTracker", True, None))
    except Exception as e:
        print(f"✗ GazeTracker: {e}")
        tests.append(("GazeTracker", False, str(e)))

    try:
        from src.core.mouse_controller import MouseController
        print("✓ MouseController")
        tests.append(("MouseController", True, None))
    except Exception as e:
        print(f"✗ MouseController: {e}")
        tests.append(("MouseController", False, str(e)))

    try:
        from src.core.calibration import Calibration
        print("✓ Calibration")
        tests.append(("Calibration", True, None))
    except Exception as e:
        print(f"✗ Calibration: {e}")
        tests.append(("Calibration", False, str(e)))

    # Test UI
    try:
        from src.ui.main_window import MainWindow
        print("✓ MainWindow")
        tests.append(("MainWindow", True, None))
    except Exception as e:
        print(f"✗ MainWindow: {e}")
        tests.append(("MainWindow", False, str(e)))

    # Test utils
    try:
        from src.utils.logger import setup_logger
        print("✓ Logger")
        tests.append(("Logger", True, None))
    except Exception as e:
        print(f"✗ Logger: {e}")
        tests.append(("Logger", False, str(e)))

    try:
        from src.utils.config import Config
        print("✓ Config")
        tests.append(("Config", True, None))
    except Exception as e:
        print(f"✗ Config: {e}")
        tests.append(("Config", False, str(e)))

    try:
        from src.utils.error_handler import ErrorHandler
        print("✓ ErrorHandler")
        tests.append(("ErrorHandler", True, None))
    except Exception as e:
        print(f"✗ ErrorHandler: {e}")
        tests.append(("ErrorHandler", False, str(e)))

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)

    passed = sum(1 for _, success, _ in tests if success)
    total = len(tests)

    print(f"Módulos validados: {passed}/{total}")

    if passed == total:
        print("\n✓ TODOS LOS MÓDULOS SE IMPORTAN CORRECTAMENTE")
        return 0
    else:
        print(f"\n✗ {total - passed} MÓDULOS FALLARON")
        print("\nErrores:")
        for name, success, error in tests:
            if not success:
                print(f"  - {name}: {error}")
        return 1


def test_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n" + "=" * 60)
    print("VALIDACIÓN DE DEPENDENCIAS")
    print("=" * 60)

    dependencies = [
        ("numpy", "numpy"),
        ("OpenCV", "cv2"),
        ("MediaPipe", "mediapipe"),
        ("PyAutoGUI", "pyautogui"),
    ]

    all_ok = True

    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError as e:
            print(f"✗ {name}: {e}")
            all_ok = False

    return 0 if all_ok else 1


def main():
    """Función principal"""
    print("VALIDACIÓN DEL SISTEMA - Gaze Control v2.0\n")

    # Test dependencias
    deps_result = test_dependencies()

    # Test imports
    imports_result = test_imports()

    # Resultado final
    print("\n" + "=" * 60)
    if deps_result == 0 and imports_result == 0:
        print("✓ SISTEMA VALIDADO CORRECTAMENTE")
        print("  Puedes ejecutar: python main.py")
    else:
        print("✗ ERRORES ENCONTRADOS")
        print("  Ejecuta: python setup.py")
    print("=" * 60)

    return max(deps_result, imports_result)


if __name__ == "__main__":
    sys.exit(main())
