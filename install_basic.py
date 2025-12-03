#!/usr/bin/env python3
"""
Instalador básico de dependencias para Gaze Control
Instala solo las dependencias esenciales para el modo básico
"""
import subprocess
import sys


def install_basic_deps():
    """Instala las dependencias básicas necesarias"""
    print("🚀 INSTALADOR BÁSICO - GAZE CONTROL")
    print("=" * 50)
    
    # Dependencias básicas
    deps = [
        "numpy",
        "opencv-python", 
        "pyautogui"
    ]
    
    print(f"Instalando {len(deps)} dependencias básicas...")
    
    for i, dep in enumerate(deps, 1):
        print(f"[{i}/{len(deps)}] Instalando {dep}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", dep],
                check=True, capture_output=True
            )
            print(f"   ✅ {dep} instalado")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error instalando {dep}: {e}")
            return False
            
    print("\n✅ Dependencias básicas instaladas")
    return True


def verify_installation():
    """Verifica que las dependencias funcionen"""
    print("\n🔍 Verificando instalación...")
    
    try:
        import numpy
        import cv2
        import pyautogui
        print("✅ Todas las dependencias funcionan correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error verificando: {e}")
        return False


def main():
    """Función principal"""
    print("Este instalador configura las dependencias básicas para")
    print("el modo básico de Gaze Control (sin MediaPipe).")
    print()
    
    # Instalar dependencias
    if not install_basic_deps():
        print("\n❌ Falló la instalación")
        return 1
        
    # Verificar
    if not verify_installation():
        print("\n❌ Falló la verificación")
        return 1
        
    print("\n" + "=" * 50)
    print("🎉 ¡INSTALACIÓN BÁSICA COMPLETADA!")
    print("=" * 50)
    print("\nAhora puedes ejecutar:")
    print("   python test_basic.py")
    print("\nPara el sistema completo con todas las características:")
    print("   python install.py")
    print("=" * 50)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())