"""
Gaze Control - Sistema de control del cursor por mirada con autenticación
Versión 2.0 - Mejorado con arquitectura modular y seguridad
"""
import sys
import cv2 as cv
import pyautogui
import time
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.database.db_manager import DatabaseManager
from src.auth.user_manager import UserManager
from src.core.gaze_tracker import GazeTracker
from src.core.mouse_controller import MouseController
from src.ui.main_window import MainWindow
from src.utils.logger import setup_logger
from src.utils.config import Config
from src.utils.error_handler import ErrorHandler


class GazeControlApp:
    """Aplicación principal de control por mirada"""

    def __init__(self):
        # Setup logging
        self.logger = setup_logger()
        self.logger.info("=" * 60)
        self.logger.info("Iniciando Gaze Control v2.0")
        self.logger.info("=" * 60)

        # Configuración
        self.config = Config()
        self.error_handler = ErrorHandler(self.logger)

        # Base de datos y autenticación
        self.db = DatabaseManager()
        self.user_manager = UserManager(self.db)

        # Componentes principales
        screen_w, screen_h = pyautogui.size()
        self.logger.info(f"Resolución de pantalla: {screen_w}x{screen_h}")

        self.gaze_tracker = GazeTracker(
            screen_w, screen_h,
            gain=self.config.get('gain'),
            deadzone=self.config.get('deadzone'),
            filter_min_cutoff=self.config.get('filter_min_cutoff'),
            filter_beta=self.config.get('filter_beta'),
            logger=self.logger
        )

        self.mouse_controller = MouseController(
            wink_threshold=self.config.get('wink_threshold'),
            wink_min_frames=self.config.get('wink_min_frames'),
            double_wink_window=self.config.get('double_wink_window'),
            dwell_time=self.config.get('dwell_time'),
            scroll_band=self.config.get('scroll_band'),
            scroll_step=self.config.get('scroll_step'),
            logger=self.logger
        )

        self.window = MainWindow(
            window_name=self.config.get('window_name'),
            logger=self.logger
        )

        # Estado
        self.camera = None
        self.running = False
        self.debug_mode = self.config.get('debug_mode')
        self.authenticated = False
        self.last_auth_check = 0
        self.auth_check_interval = self.config.get('auth_check_interval')

    def initialize_camera(self) -> bool:
        """Inicializa la cámara"""
        try:
            camera_index = self.config.get('camera_index')
            self.logger.info(f"Inicializando cámara {camera_index}...")

            self.camera = cv.VideoCapture(camera_index, cv.CAP_DSHOW)

            if not self.camera.isOpened():
                self.logger.error("No se pudo abrir la cámara")
                return False

            # Configurar cámara
            self.camera.set(cv.CAP_PROP_FRAME_WIDTH, self.config.get('camera_width'))
            self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, self.config.get('camera_height'))
            self.camera.set(cv.CAP_PROP_FPS, self.config.get('camera_fps'))

            self.logger.info("Cámara inicializada correctamente")
            return True

        except Exception as e:
            self.logger.error(f"Error inicializando cámara: {e}")
            return False

    def register_user_if_needed(self) -> bool:
        """Verifica si hay usuarios o permite registrar uno nuevo"""
        if self.user_manager.has_registered_user():
            self.logger.info("Ya hay usuarios registrados")
            return True

        self.logger.info("No hay usuarios registrados. Iniciando proceso de registro...")
        print("\n" + "=" * 60)
        print("PRIMER REGISTRO DE USUARIO")
        print("=" * 60)
        print("No hay usuarios en el sistema. Registra al primer usuario.")

        username = input("Ingresa tu nombre de usuario: ").strip()
        if not username:
            username = "Usuario1"

        print(f"\nRegistrando usuario: {username}")
        print("Se capturarán 10 muestras de tu rostro.")
        print("Por favor, mira a la cámara y mueve ligeramente la cabeza.")
        print("Presiona ENTER para continuar...")
        input()

        success = self.user_manager.register_new_user(username, self.camera, num_samples=10)

        if success:
            print(f"\n✓ Usuario '{username}' registrado exitosamente!")
            self.logger.info(f"Usuario '{username}' registrado")
            return True
        else:
            print("\n✗ Error en el registro del usuario")
            self.logger.error("Fallo en registro de usuario")
            return False

    def authenticate_user(self) -> bool:
        """Autentica al usuario con la cámara - ahora con selección de usuario"""
        self.logger.info("Iniciando autenticación...")
        
        # Verificar si hay usuarios registrados
        users = self.user_manager.get_all_users()
        if not users:
            print("\n✗ No hay usuarios registrados")
            return False
        
        # Si hay múltiples usuarios, mostrar menú de selección
        if len(users) > 1:
            print("\n" + "=" * 60)
            print("SELECCIÓN DE USUARIO")
            print("=" * 60)
            for i, user in enumerate(users, 1):
                print(f"{i}. {user['username']}")
            print("=" * 60)
            
            try:
                choice = input("\nSelecciona tu usuario (número): ").strip()
                idx = int(choice) - 1
                
                if idx < 0 or idx >= len(users):
                    print("\n✗ Opción inválida")
                    return False
                
                selected_user_id = users[idx]['id']
                selected_username = users[idx]['username']
            except (ValueError, IndexError):
                print("\n✗ Entrada inválida")
                return False
        else:
            # Un solo usuario
            selected_user_id = users[0]['id']
            selected_username = users[0]['username']
        
        # Autenticar con reconocimiento facial
        print("\n" + "=" * 60)
        print("AUTENTICACIÓN FACIAL")
        print("=" * 60)
        print(f"Verificando identidad de: {selected_username}")
        print("Por favor, mira a la cámara...")

        max_attempts = 30  # 30 frames = ~1-2 segundos
        attempts = 0

        while attempts < max_attempts:
            ret, frame = self.camera.read()
            if not ret:
                continue

            frame = cv.flip(frame, 1)

            # Mostrar feedback
            cv.putText(
                frame, f"Autenticando {selected_username}...",
                (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2
            )
            cv.imshow("Autenticacion", frame)
            cv.waitKey(1)

            # Intentar login con el usuario seleccionado
            if self.user_manager.login(frame, user_id=selected_user_id):
                cv.destroyWindow("Autenticacion")
                user = self.user_manager.get_current_user()
                print(f"\n✓ Autenticación exitosa! Bienvenido {user['username']}")
                self.logger.info(f"Usuario autenticado: {user['username']}")
                self.authenticated = True
                return True

            attempts += 1

        cv.destroyWindow("Autenticacion")
        print("\n✗ Autenticación fallida - Rostro no reconocido")
        self.logger.warning("Autenticación fallida")
        return False

    def load_user_settings(self):
        """Carga las configuraciones guardadas del usuario"""
        if not self.user_manager.current_user:
            return

        user_id = self.user_manager.current_user['id']
        self.logger.info("Cargando configuraciones del usuario...")

        # Cargar configuraciones
        configs = self.user_manager.get_all_user_configs()
        for key, value in configs.items():
            self.config.set(key, value)

        # Aplicar configuraciones al gaze tracker
        self.gaze_tracker.set_gain(self.config.get('gain'))
        self.gaze_tracker.set_deadzone(self.config.get('deadzone'))

        # Cargar calibración
        calib_data = self.db.get_active_calibration(user_id)
        if calib_data:
            self.gaze_tracker.calibration.load_calibration_data(calib_data)
            self.logger.info("Calibración cargada desde base de datos")

    def save_user_settings(self):
        """Guarda las configuraciones del usuario"""
        if not self.user_manager.current_user:
            return

        self.logger.info("Guardando configuraciones...")

        # Guardar configuraciones principales
        settings_to_save = ['gain', 'deadzone', 'dwell_enabled', 'debug_mode']
        for key in settings_to_save:
            value = self.config.get(key)
            self.user_manager.save_user_config(key, value)

        self.config.save()
        self.logger.info("Configuraciones guardadas")

    def run_calibration(self):
        """Ejecuta el proceso de calibración"""
        self.logger.info("Iniciando calibración...")

        # Obtener puntos de calibración
        grid_points = self.gaze_tracker.calibration.get_grid_points(3, 3)
        self.window.start_calibration(grid_points)

        # Limpiar calibración anterior
        self.gaze_tracker.calibration.clear_samples()

        while self.window.is_calibrating():
            ret, frame = self.camera.read()
            if not ret:
                continue

            frame = cv.flip(frame, 1)

            # Obtener posición de mirada sin filtrar
            gaze_pos = self.gaze_tracker.get_raw_gaze_position(frame)
            has_face = gaze_pos is not None

            # Procesar frame de calibración
            completed_target = self.window.process_calibration_frame(frame, has_face)

            if completed_target and gaze_pos:
                target_x, target_y = completed_target
                gaze_x, gaze_y = gaze_pos
                self.gaze_tracker.calibration.add_sample(gaze_x, gaze_y, target_x, target_y)

            self.window.show_frame(frame)
            if self.window.wait_key(1) == ord('q'):
                break

        # Calcular calibración
        if self.gaze_tracker.calibration.compute_calibration():
            self.logger.info("Calibración completada exitosamente")

            # Guardar en base de datos
            if self.user_manager.current_user:
                calib_data = self.gaze_tracker.calibration.get_calibration_data()
                self.db.save_calibration(
                    self.user_manager.current_user['id'],
                    calib_data['matrix'],
                    calib_data['samples_src'],
                    calib_data['samples_dst']
                )
                self.logger.info("Calibración guardada en base de datos")
        else:
            self.logger.warning("Calibración incompleta")

    def main_loop(self):
        """Loop principal de la aplicación"""
        self.logger.info("Iniciando loop principal...")
        self.window.create_window()
        self.running = True

        try:
            while self.running:
                ret, frame = self.camera.read()
                if not ret:
                    self.logger.warning("No se pudo leer frame de cámara")
                    time.sleep(0.1)
                    continue

                frame = cv.flip(frame, 1)

                # Verificar autenticación periódicamente
                current_time = time.time()
                if current_time - self.last_auth_check > self.auth_check_interval:
                    is_match, similarity, num_faces = self.user_manager.authenticate_user(frame)
                    self.window.update_auth_status(is_match, similarity)

                    if not is_match:
                        # Usuario no reconocido - BLOQUEAR TODO CONTROL
                        warning_msg = "USUARIO NO RECONOCIDO - CONTROL BLOQUEADO"
                        if num_faces > 1:
                            warning_msg = f"MULTIPLES ROSTROS DETECTADOS ({num_faces}) - CONTROL BLOQUEADO"
                        elif num_faces == 0:
                            warning_msg = "NO SE DETECTA ROSTRO"
                        
                        self.window.draw_warning(frame, warning_msg)
                        self.window.show_frame(frame)
                        self.window.wait_key(1)
                        continue

                    self.last_auth_check = current_time

                # Procesar seguimiento de mirada SOLO si el usuario está autenticado
                screen_pos = self.gaze_tracker.process_frame(frame)

                if screen_pos:
                    screen_x, screen_y = screen_pos

                    # Mover mouse SOLO si usuario autenticado
                    self.mouse_controller.move_to(screen_x, screen_y)

                    # Detectar gestos
                    gestures = self.gaze_tracker.detect_gestures(frame)

                    # Obtener posición x de la mirada para gestos avanzados
                    gaze_x = None
                    if self.gaze_tracker.last_gaze_position:
                        gaze_x = self.gaze_tracker.last_gaze_position[0]

                    self.mouse_controller.process_gestures(gestures, screen_x, screen_y, gaze_x)

                    # Dwell click
                    if self.gaze_tracker.last_gaze_position:
                        gx, gy = self.gaze_tracker.last_gaze_position
                        self.mouse_controller.process_dwell_click(gx, gy, screen_x, screen_y)

                        # Auto scroll
                        self.mouse_controller.process_auto_scroll(gy)

                # Actualizar UI
                self.window.update_fps()

                if self.debug_mode:
                    current_config = {
                        'gain': self.gaze_tracker.gain,
                        'deadzone': self.gaze_tracker.deadzone_filter.threshold,
                        'dwell_enabled': self.mouse_controller.dwell_enabled
                    }
                    self.window.draw_hud(
                        frame, current_config,
                        self.user_manager.get_current_user()
                    )

                self.window.show_frame(frame)

                # Procesar teclas
                key = self.window.wait_key(1)
                self.process_key(key)

        except KeyboardInterrupt:
            self.logger.info("Interrupción por teclado")
        except Exception as e:
            self.logger.error(f"Error en loop principal: {e}", exc_info=True)
        finally:
            self.cleanup()

    def process_key(self, key: int):
        """Procesa las teclas presionadas"""
        if key == ord('q'):
            self.running = False
        elif key == ord('d'):
            self.debug_mode = not self.debug_mode
            self.config.set('debug_mode', self.debug_mode)
        elif key == ord('c'):
            self.run_calibration()
        elif key == ord('r'):
            self.gaze_tracker.calibration.reset()
            self.logger.info("Calibración reseteada")
        elif key in (ord('+'), ord('=')):
            new_gain = min(2.5, self.gaze_tracker.gain + 0.05)
            self.gaze_tracker.set_gain(new_gain)
            self.config.set('gain', new_gain)
        elif key == ord('-'):
            new_gain = max(0.5, self.gaze_tracker.gain - 0.05)
            self.gaze_tracker.set_gain(new_gain)
            self.config.set('gain', new_gain)
        elif key == ord('g'):
            enabled = self.mouse_controller.toggle_dwell()
            self.config.set('dwell_enabled', enabled)

    def cleanup(self):
        """Limpia recursos"""
        self.logger.info("Limpiando recursos...")

        self.save_user_settings()

        if self.camera:
            self.camera.release()

        self.window.destroy()
        self.gaze_tracker.close()
        self.user_manager.logout()
        self.db.close()

        cv.destroyAllWindows()
        self.logger.info("Aplicación cerrada correctamente")

    def run(self):
        """Punto de entrada principal"""
        try:
            # Inicializar cámara
            if not self.initialize_camera():
                print("Error: No se pudo inicializar la cámara")
                return 1

            # Registrar usuario si es necesario
            if not self.register_user_if_needed():
                print("Error: No se pudo registrar el usuario")
                return 1

            # Autenticar usuario
            if not self.authenticate_user():
                print("Error: Autenticación fallida")
                return 1

            # Cargar configuraciones
            self.load_user_settings()

            # Iniciar loop principal
            print("\n" + "=" * 60)
            print("SISTEMA INICIADO")
            print("=" * 60)
            print("Controles Teclado:")
            print("  [c] - Calibrar")
            print("  [r] - Reset calibración")
            print("  [d] - Toggle debug")
            print("  [+/-] - Ajustar sensibilidad")
            print("  [g] - Toggle dwell click")
            print("  [q] - Salir")
            print("\nGestos Oculares:")
            print("  👁️  Guiño izquierdo corto → Click izquierdo")
            print("  👁️  Guiño izquierdo SOSTENIDO (~0.5s) → Click derecho")
            print("  👁️👁️ Doble guiño izquierdo → Página adelante")
            print("  👁️  Guiño derecho corto → Página atrás")
            print("  👁️  Ojo derecho cerrado + Mover derecha → Siguiente pestaña")
            print("  👁️  Ojo derecho cerrado + Mover izquierda → Pestaña anterior")
            print("=" * 60)

            self.main_loop()
            return 0

        except Exception as e:
            self.logger.error(f"Error fatal: {e}", exc_info=True)
            return 1


def main():
    """Función principal"""
    app = GazeControlApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
