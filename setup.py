"""
Script de configuración rápida para Gaze Control v2.0
"""
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro} detectado")

    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        return False

    if version.minor < 10:
        print("⚠️  Advertencia: Se recomienda Python 3.10+ para mejor compatibilidad")

    return True


def install_dependencies():
    """Instala las dependencias"""
    print("\n" + "=" * 60)
    print("Instalando dependencias...")
    print("=" * 60)

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\n✓ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error instalando dependencias: {e}")
        return False


def create_directories():
    """Crea los directorios necesarios"""
    print("\n" + "=" * 60)
    print("Creando directorios...")
    print("=" * 60)

    directories = [
        "data",
        "data/logs"
    ]

    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"✓ Creado: {directory}/")
        else:
            print(f"  Existe: {directory}/")

    return True


def check_camera():
    """Verifica si la cámara está disponible"""
    print("\n" + "=" * 60)
    print("Verificando cámara...")
    print("=" * 60)

    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Cámara detectada correctamente")
            cap.release()
            return True
        else:
            print("❌ No se pudo abrir la cámara")
            print("   Asegúrate de que no esté siendo usada por otra aplicación")
            return False
    except Exception as e:
        print(f"❌ Error verificando cámara: {e}")
        return False


def main():
    """Función principal de setup"""
    print("=" * 60)
    print("GAZE CONTROL v2.0 - SETUP")
    print("=" * 60)

    # Verificar Python
    if not check_python_version():
        return 1

    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Fallo en instalación de dependencias")
        return 1

    # Crear directorios
    if not create_directories():
        print("\n❌ Fallo creando directorios")
        return 1

    # Verificar cámara
    camera_ok = check_camera()

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE INSTALACIÓN")
    print("=" * 60)
    print("✓ Python verificado")
    print("✓ Dependencias instaladas")
    print("✓ Directorios creados")
    if camera_ok:
        print("✓ Cámara verificada")
    else:
        print("⚠️  Cámara no verificada (puede funcionar de todas formas)")

    print("\n" + "=" * 60)
    print("LISTO PARA USAR")
    print("=" * 60)
    print("\nPara iniciar la aplicación, ejecuta:")
    print("  python main.py")
    print("\nPara gestionar usuarios:")
    print("  python manage_user.py")
    print("\nConsulta GUIDE.md para más información")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
