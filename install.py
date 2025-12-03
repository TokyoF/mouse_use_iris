#!/usr/bin/env python3
"""
Instalador Unificado - Gaze Control v2.0
Instala todas las dependencias y configura el sistema automáticamente
"""
import subprocess
import sys
import os
from pathlib import Path


class GazeControlInstaller:
    """Instalador completo para Gaze Control"""
    
    def __init__(self):
        self.python_version = sys.version_info
        self.project_root = Path(__file__).parent
        self.dependencies = [
            "numpy>=1.21.0",
            "opencv-python>=4.5.0", 
            "mediapipe>=0.10.0",
            "pyautogui>=0.9.53",
            "opencv-contrib-python>=4.5.0"
        ]
        
    def print_header(self):
        """Muestra el encabezado del instalador"""
        print("=" * 70)
        print("🎯 GAZE CONTROL v2.0 - INSTALADOR UNIFICADO")
        print("=" * 70)
        print("Este instalador configurará todo lo necesario para el sistema")
        print("de control de mouse por mirada con autenticación facial.")
        print("=" * 70)
        
    def check_python_version(self):
        """Verifica la versión de Python"""
        print(f"\n📋 Verificando Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        
        if self.python_version.major < 3 or (self.python_version.major == 3 and self.python_version.minor < 7):
            print("❌ Error: Se requiere Python 3.7 o superior")
            print("   Por favor, instala una versión más reciente de Python")
            return False
            
        if self.python_version.minor < 10:
            print("⚠️  Advertencia: Se recomienda Python 3.10+ para mejor compatibilidad")
            
        print("✅ Versión de Python compatible")
        return True
        
    def check_pip(self):
        """Verifica que pip esté disponible"""
        print("\n📋 Verificando pip...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            print("✅ pip disponible")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error: pip no está disponible")
            print("   Por favor, instala pip: python -m ensurepip --upgrade")
            return False
            
    def upgrade_pip(self):
        """Actualiza pip a la última versión"""
        print("\n🔄 Actualizando pip...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                         check=True, capture_output=True)
            print("✅ pip actualizado")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  No se pudo actualizar pip (continuando con versión actual)")
            return True
            
    def install_dependencies(self):
        """Instala todas las dependencias necesarias"""
        print(f"\n📦 Instalando {len(self.dependencies)} dependencias...")
        print("-" * 50)
        
        failed_deps = []
        
        for i, dep in enumerate(self.dependencies, 1):
            print(f"[{i}/{len(self.dependencies)}] Instalando {dep}...")
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep],
                    check=True, capture_output=True, text=True
                )
                print(f"   ✅ {dep} instalado")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Error instalando {dep}: {e}")
                
                # Manejar MediaPipe específicamente
                if "mediapipe" in dep.lower():
                    print(f"   🔄 Intentando versión alternativa de MediaPipe...")
                    try:
                        # Intentar con versión más baja
                        alt_dep = "mediapipe>=0.9.0"
                        result = subprocess.run(
                            [sys.executable, "-m", "pip", "install", alt_dep],
                            check=True, capture_output=True, text=True
                        )
                        print(f"   ✅ {alt_dep} instalado (versión alternativa)")
                    except subprocess.CalledProcessError:
                        print(f"   ⚠️  MediaPipe no disponible para tu sistema")
                        print(f"      El sistema funcionará con detección básica")
                        failed_deps.append(dep)
                else:
                    failed_deps.append(dep)
                
        if failed_deps:
            print(f"\n⚠️  {len(failed_deps)} dependencias no pudieron instalarse:")
            for dep in failed_deps:
                print(f"   - {dep}")
            print("\nEl sistema intentará funcionar con funcionalidad reducida")
            return False
        else:
            print("\n✅ Todas las dependencias instaladas correctamente")
            return True
        
    def verify_installation(self):
        """Verifica que las dependencias se instalaron correctamente"""
        print("\n🔍 Verificando instalación...")
        
        modules_to_test = [
            ("numpy", "np"),
            ("cv2", "cv"),
            ("mediapipe", "mp"),
            ("pyautogui", "pyautogui")
        ]
        
        failed_modules = []
        optional_modules = ["mediapipe"]  # Módulos opcionales
        
        for module_name, alias in modules_to_test:
            try:
                __import__(module_name)
                print(f"   ✅ {module_name}")
            except ImportError as e:
                if module_name in optional_modules:
                    print(f"   ⚠️  {module_name}: {e}")
                    print(f"      (Opcional - sistema funcionará con detección básica)")
                else:
                    print(f"   ❌ {module_name}: {e}")
                    failed_modules.append(module_name)
                
        if failed_modules:
            print(f"\n❌ {len(failed_modules)} módulos requeridos fallaron:")
            for module in failed_modules:
                print(f"   - {module}")
            return False
        else:
            print("\n✅ Módulos requeridos importados correctamente")
            return True
            
    def create_directories(self):
        """Crea los directorios necesarios para el sistema"""
        print("\n📁 Creando estructura de directorios...")
        
        directories = [
            "data",
            "data/logs",
            "data/config",
            "data/calibrations"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   ✅ Creado: {directory}/")
            else:
                print(f"   📂 Existe: {directory}/")
                
        print("✅ Estructura de directorios lista")
        return True
        
    def check_camera(self):
        """Verifica si hay una cámara disponible"""
        print("\n📷 Verificando disponibilidad de cámara...")
        
        try:
            import cv2
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            
            if cap.isOpened():
                # Intentar leer un frame para asegurarse de que funciona
                ret, _ = cap.read()
                cap.release()
                
                if ret:
                    print("✅ Cámara detectada y funcional")
                    return True
                else:
                    print("⚠️  Cámara detectada pero no se pueden leer frames")
                    print("   Puede que esté siendo usada por otra aplicación")
                    return False
            else:
                print("❌ No se pudo acceder a la cámara")
                print("   Verifica que:")
                print("   - La cámara esté conectada")
                print("   - No esté siendo usada por otra aplicación")
                print("   - Los drivers estén instalados correctamente")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando cámara: {e}")
            return False
            
    def create_desktop_shortcut(self):
        """Crea un acceso directo en el escritorio (Windows)"""
        if sys.platform != "win32":
            return True
            
        print("\n🖥️  Creando acceso directo en el escritorio...")
        
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Gaze Control.lnk")
            target = str(self.project_root / "main.py")
            wDir = str(self.project_root)
            icon = target
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
            
            print("✅ Acceso directo creado en el escritorio")
            return True
            
        except ImportError:
            print("⚠️  No se pudo crear acceso directo (falta winshell/pywin32)")
            return True
        except Exception as e:
            print(f"⚠️  Error creando acceso directo: {e}")
            return True
            
    def test_basic_functionality(self):
        """Prueba básica del sistema"""
        print("\n🧪 Realizando prueba básica del sistema...")
        
        try:
            # Importar los módulos principales
            sys.path.insert(0, str(self.project_root / "src"))
            
            print("   📦 Importando módulos del sistema...")
            from src.utils.config import Config
            from src.utils.logger import setup_logger
            print("   ✅ Módulos de utils importados")
            
            # Test de configuración
            config = Config()
            print("   ✅ Sistema de configuración funcional")
            
            # Test de logger
            logger = setup_logger()
            logger.info("Test de instalación exitoso")
            print("   ✅ Sistema de logging funcional")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error en prueba básica: {e}")
            return False
            
    def print_summary(self, installation_ok, camera_ok, test_ok):
        """Muestra el resumen final de la instalación"""
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE INSTALACIÓN")
        print("=" * 70)
        
        print(f"Python:                 {'✅' if self.python_version >= (3, 7) else '❌'}")
        print(f"Dependencias:           {'✅' if installation_ok else '❌'}")
        print(f"Directorios:            ✅")
        print(f"Cámara:                 {'✅' if camera_ok else '❌'}")
        print(f"Prueba básica:          {'✅' if test_ok else '❌'}")
        
        if installation_ok and test_ok:
            print("\n🎉 ¡INSTALACIÓN COMPLETADA CON ÉXITO!")
            print("\n" + "=" * 70)
            print("🚀 PRÓXIMOS PASOS")
            print("=" * 70)
            print("\nPara iniciar la aplicación:")
            print("   python main.py")
            print("\nPara gestionar usuarios:")
            print("   python manage_user.py")
            print("\nDocumentación disponible:")
            print("   - GUIDE.md: Guía de uso")
            print("   - FLUJO_SISTEMA.md: Documentación técnica")
            print("   - QUICKSTART.md: Inicio rápido")
            
            if not camera_ok:
                print("\n⚠️  ADVERTENCIA:")
                print("   La cámara no fue detectada. Verifica que esté conectada")
                print("   y no esté siendo usada por otra aplicación antes de")
                print("   iniciar el programa.")
                
        else:
            print("\n❌ LA INSTALACIÓN PRESENTÓ PROBLEMAS")
            print("\nSoluciones sugeridas:")
            if not installation_ok:
                print("   - Revisa tu conexión a internet")
                print("   - Ejecuta como administrador")
                print("   - Intenta: pip install --upgrade pip")
            if not test_ok:
                print("   - Revisa que todos los paquetes se instalaron correctamente")
                print("   - Reinicia tu terminal y vuelve a intentar")
                
        print("\n" + "=" * 70)
        
    def run(self):
        """Ejecuta el proceso completo de instalación"""
        self.print_header()
        
        # Verificaciones previas
        if not self.check_python_version():
            return 1
            
        if not self.check_pip():
            return 1
            
        # Actualizar pip
        self.upgrade_pip()
        
        # Instalación de dependencias
        installation_ok = self.install_dependencies()
        if not installation_ok:
            return 1
            
        # Verificación
        verification_ok = self.verify_installation()
        if not verification_ok:
            return 1
            
        # Crear estructura
        self.create_directories()
        
        # Verificar cámara
        camera_ok = self.check_camera()
        
        # Acceso directo
        self.create_desktop_shortcut()
        
        # Prueba básica
        test_ok = self.test_basic_functionality()
        
        # Resumen final
        self.print_summary(installation_ok, camera_ok, test_ok)
        
        return 0 if installation_ok and test_ok else 1


def main():
    """Punto de entrada del instalador"""
    installer = GazeControlInstaller()
    return installer.run()


if __name__ == "__main__":
    sys.exit(main())