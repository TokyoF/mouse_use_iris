#!/usr/bin/env python3
"""
Script de prueba para Gaze Control sin MediaPipe
Usa detección facial básica de OpenCV
"""
import sys
import cv2 as cv
import pyautogui
import numpy as np
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.core.alternative_detector import AlternativeGazeTracker
    ALTERNATIVE_MODE = True
    print("✅ Usando detector facial alternativo (OpenCV)")
except ImportError as e:
    print(f"❌ Error importando detector alternativo: {e}")
    ALTERNATIVE_MODE = False


class SimpleGazeControl:
    """Control de mouse por mirada simplificado"""
    
    def __init__(self):
        # Configuración de pyautogui
        pyautogui.FAILSAFE = True
        screen_w, screen_h = pyautogui.size()
        
        print(f"📺 Resolución de pantalla: {screen_w}x{screen_h}")
        
        # Inicializar tracker
        if ALTERNATIVE_MODE:
            self.gaze_tracker = AlternativeGazeTracker(
                screen_w, screen_h,
                gain=1.2,
                deadzone=0.02
            )
        else:
            print("❌ No se pudo inicializar el tracker")
            sys.exit(1)
            
        # Cámara
        self.camera = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.camera.isOpened():
            print("❌ No se pudo abrir la cámara")
            sys.exit(1)
            
        print("✅ Cámara inicializada")
        
        # Estado
        self.running = True
        self.debug_mode = True
        
    def process_frame(self, frame):
        """Procesa un frame individual"""
        frame = cv.flip(frame, 1)
        
        # Procesar seguimiento de mirada
        screen_pos = self.gaze_tracker.process_frame(frame)
        
        if screen_pos:
            screen_x, screen_y = screen_pos
            
            # Mover mouse
            pyautogui.moveTo(screen_x, screen_y, _pause=False)
            
            # Dibujar posición en frame
            cv.circle(frame, (screen_x // 4, screen_y // 4), 10, (0, 255, 0), -1)
            
        # Detectar gestos
        gestures = self.gaze_tracker.detect_gestures(frame)
        
        # Procesar gestos
        if gestures.get('left_wink'):
            pyautogui.click()
            print("🖱️ Click izquierdo")
            
        if gestures.get('right_wink'):
            pyautogui.rightClick()
            print("🖱️ Click derecho")
            
        # Debug info
        if self.debug_mode:
            frame = self.gaze_tracker.draw_debug_info(frame)
            
            # Texto informativo
            cv.putText(frame, "Q para salir", (10, 30), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if screen_pos:
                cv.putText(frame, f"Pos: {screen_pos}", (10, 60),
                          cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                          
        return frame
        
    def run(self):
        """Loop principal"""
        print("\n🎯 INICIANDO CONTROL POR MIRADA")
        print("=" * 50)
        print("Controles:")
        print("  - Mira a la cámara para mover el cursor")
        print("  - Guiño ojo izquierdo → Click izquierdo")
        print("  - Guiño ojo derecho → Click derecho")
        print("  - Q para salir")
        print("=" * 50)
        
        try:
            while self.running:
                ret, frame = self.camera.read()
                if not ret:
                    print("⚠️ No se pudo leer frame")
                    continue
                    
                # Procesar frame
                processed_frame = self.process_frame(frame)
                
                # Mostrar
                cv.imshow("Gaze Control - Modo Básico", processed_frame)
                
                # Teclas
                key = cv.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.running = False
                elif key == ord('d'):
                    self.debug_mode = not self.debug_mode
                    
        except KeyboardInterrupt:
            print("\n👋 Interrupción por usuario")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Limpia recursos"""
        print("🧹 Limpiando recursos...")
        self.camera.release()
        cv.destroyAllWindows()
        print("✅ Listo")


def main():
    """Función principal"""
    print("=" * 60)
    print("🎯 GAZE CONTROL - MODO BÁSICO (SIN MEDIAPIPE)")
    print("=" * 60)
    print("Este modo usa detección facial básica de OpenCV")
    print("Funcionalidad reducida pero compatible con más sistemas")
    print("=" * 60)
    
    # Verificar dependencias básicas
    try:
        import cv2
        import pyautogui
        import numpy as np
        print("✅ Dependencias básicas verificadas")
    except ImportError as e:
        print(f"❌ Faltan dependencias: {e}")
        print("Ejecuta: pip install opencv-python pyautogui numpy")
        return 1
        
    # Iniciar control
    app = SimpleGazeControl()
    app.run()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())