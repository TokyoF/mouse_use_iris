"""Ventana principal de la aplicación con UI mejorada"""
import cv2 as cv
import numpy as np
import time
import logging
from typing import Optional


class MainWindow:
    """Maneja la ventana principal y el renderizado de UI"""

    def __init__(self, window_name: str = "Gaze Control", logger: Optional[logging.Logger] = None):
        self.window_name = window_name
        self.logger = logger

        # Estado de calibración
        self.calibration_mode = False
        self.calibration_targets = []
        self.current_target_index = 0
        self.hold_start_time: Optional[float] = None
        self.hold_duration = 0.4

        # FPS tracking
        self.fps = 0.0
        self.fps_smooth = 0.9
        self.last_fps_time = time.time()
        self.frame_count = 0

        # Estado de autenticación
        self.authenticated = False
        self.auth_similarity = 0.0

    def create_window(self):
        """Crea la ventana principal"""
        cv.namedWindow(self.window_name, cv.WINDOW_NORMAL)

    def update_fps(self):
        """Actualiza el contador de FPS"""
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            current_time = time.time()
            dt = current_time - self.last_fps_time
            self.fps = self.fps_smooth * self.fps + (1 - self.fps_smooth) * (10.0 / dt)
            self.last_fps_time = current_time

    def draw_hud(self, frame: np.ndarray, config: dict, user_info: Optional[dict] = None):
        """
        Dibuja el HUD (Heads-Up Display) con información del sistema

        Args:
            frame: Frame donde dibujar
            config: Configuración actual
            user_info: Información del usuario (opcional)
        """
        h, w = frame.shape[:2]

        # Fondo semi-transparente para el HUD
        overlay = frame.copy()
        cv.rectangle(overlay, (0, 0), (w, 100), (0, 0, 0), -1)
        cv.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

        # Información superior izquierda
        y_offset = 25
        info_texts = [
            f"FPS: {self.fps:.1f}",
            f"Ganancia: {config.get('gain', 1.2):.2f}",
            f"Deadzone: {config.get('deadzone', 0.015):.3f}",
            f"Dwell: {'ON' if config.get('dwell_enabled', False) else 'OFF'}"
        ]

        for i, text in enumerate(info_texts):
            cv.putText(
                frame, text, (10, y_offset + i * 20),
                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
            )

        # Usuario autenticado
        if user_info and self.authenticated:
            user_text = f"Usuario: {user_info.get('username', 'N/A')}"
            auth_text = f"Auth: {self.auth_similarity:.0%}"
            cv.putText(
                frame, user_text, (w - 250, 25),
                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
            )
            cv.putText(
                frame, auth_text, (w - 250, 45),
                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1
            )
            # Indicador visual
            color = (0, 255, 0) if self.auth_similarity > 0.85 else (0, 165, 255)
            cv.circle(frame, (w - 260, 20), 8, color, -1)
        else:
            cv.putText(
                frame, "No autenticado", (w - 250, 25),
                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1
            )

        # Instrucciones en la parte inferior
        instructions = [
            "Gestos: Ojo Izq (click) | Ojo Izq Sostenido (click derecho) | Ojo Der + Mover (pestanas)",
            "[c] Calibrar  [r] Reset  [d] Debug  [+/-] Ganancia  [g] Dwell  [q] Salir"
        ]

        for i, instruction in enumerate(instructions):
            cv.putText(
                frame, instruction, (10, h - 15 - (len(instructions) - 1 - i) * 20),
                cv.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1
            )

    def draw_calibration_target(self, frame: np.ndarray, target_x: int, target_y: int,
                               is_ready: bool = False):
        """
        Dibuja el objetivo de calibración

        Args:
            frame: Frame donde dibujar
            target_x: Coordenada x del objetivo
            target_y: Coordenada y del objetivo
            is_ready: Si el usuario está listo para capturar
        """
        # Círculo exterior
        color = (0, 255, 0) if is_ready else (0, 255, 255)
        cv.circle(frame, (target_x, target_y), 20, color, 2)
        cv.circle(frame, (target_x, target_y), 15, color, 1)

        # Punto central
        cv.circle(frame, (target_x, target_y), 5, color, -1)

        # Barra de progreso si está en hold
        if is_ready and self.hold_start_time:
            elapsed = time.time() - self.hold_start_time
            progress = min(1.0, elapsed / self.hold_duration)

            # Barra de progreso circular
            angle = int(360 * progress)
            cv.ellipse(
                frame, (target_x, target_y), (25, 25),
                -90, 0, angle, (0, 255, 0), 3
            )

    def start_calibration(self, target_points: list):
        """
        Inicia el modo de calibración

        Args:
            target_points: Lista de puntos objetivo para calibración
        """
        self.calibration_mode = True
        self.calibration_targets = target_points
        self.current_target_index = 0
        self.hold_start_time = None

        if self.logger:
            self.logger.info(f"Calibración iniciada con {len(target_points)} puntos")

    def process_calibration_frame(self, frame: np.ndarray, has_face: bool) -> Optional[tuple]:
        """
        Procesa un frame durante la calibración

        Args:
            frame: Frame actual
            has_face: Si se detectó un rostro

        Returns:
            Tupla (target_x, target_y) si se completó un punto, None en caso contrario
        """
        if not self.calibration_mode or not self.calibration_targets:
            return None

        target_x, target_y = self.calibration_targets[self.current_target_index]

        # Dibujar objetivo
        self.draw_calibration_target(frame, target_x, target_y, has_face)

        # Instrucciones
        h, w = frame.shape[:2]
        text = f"Mira al punto {self.current_target_index + 1}/{len(self.calibration_targets)}"
        cv.putText(
            frame, text, (w // 2 - 150, 50),
            cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2
        )

        if has_face:
            if self.hold_start_time is None:
                self.hold_start_time = time.time()

            # Verificar si se completó el hold
            if time.time() - self.hold_start_time >= self.hold_duration:
                result = (target_x, target_y)
                self.current_target_index += 1
                self.hold_start_time = None

                # Verificar si se completó la calibración
                if self.current_target_index >= len(self.calibration_targets):
                    self.calibration_mode = False
                    if self.logger:
                        self.logger.info("Calibración completada")

                return result
        else:
            self.hold_start_time = None

        return None

    def is_calibrating(self) -> bool:
        """Verifica si está en modo calibración"""
        return self.calibration_mode

    def draw_warning(self, frame: np.ndarray, message: str):
        """
        Dibuja un mensaje de advertencia en el centro

        Args:
            frame: Frame donde dibujar
            message: Mensaje a mostrar
        """
        h, w = frame.shape[:2]

        # Fondo semi-transparente
        overlay = frame.copy()
        cv.rectangle(
            overlay,
            (w // 4, h // 2 - 50),
            (3 * w // 4, h // 2 + 50),
            (0, 0, 255), -1
        )
        cv.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Texto
        text_size = cv.getTextSize(message, cv.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_x = (w - text_size[0]) // 2
        text_y = (h + text_size[1]) // 2

        cv.putText(
            frame, message, (text_x, text_y),
            cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2
        )

    def draw_notification(self, frame: np.ndarray, message: str, duration: float = 2.0):
        """
        Dibuja una notificación temporal

        Args:
            frame: Frame donde dibujar
            message: Mensaje a mostrar
            duration: Duración en segundos
        """
        h, w = frame.shape[:2]

        # Notificación en la parte superior central
        text_size = cv.getTextSize(message, cv.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        x = (w - text_size[0]) // 2
        y = 100

        # Fondo
        overlay = frame.copy()
        cv.rectangle(
            overlay,
            (x - 10, y - 30),
            (x + text_size[0] + 10, y + 10),
            (0, 200, 0), -1
        )
        cv.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        # Texto
        cv.putText(
            frame, message, (x, y),
            cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
        )

    def show_frame(self, frame: np.ndarray):
        """Muestra el frame en la ventana"""
        cv.imshow(self.window_name, frame)

    def wait_key(self, delay: int = 1) -> int:
        """
        Espera por una tecla

        Args:
            delay: Delay en milisegundos

        Returns:
            Código de la tecla presionada
        """
        return cv.waitKey(delay) & 0xFF

    def update_auth_status(self, authenticated: bool, similarity: float = 0.0):
        """Actualiza el estado de autenticación para el HUD"""
        self.authenticated = authenticated
        self.auth_similarity = similarity

    def destroy(self):
        """Destruye la ventana"""
        cv.destroyWindow(self.window_name)
        if self.logger:
            self.logger.info("Ventana principal cerrada")
