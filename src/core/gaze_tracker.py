"""Seguimiento de mirada con filtrado y calibración"""
import time
import logging
import numpy as np
from typing import Optional, Tuple
from .face_detector import FaceDetector
from .filters import OneEuro, DeadzoneFilter
from .calibration import Calibration


class GazeTracker:
    """Rastrea la mirada y la convierte en coordenadas de pantalla"""

    def __init__(self, screen_width: int, screen_height: int,
                 gain: float = 1.2, deadzone: float = 0.015,
                 filter_min_cutoff: float = 1.2, filter_beta: float = 0.04,
                 logger: Optional[logging.Logger] = None):
        """
        Args:
            screen_width: Ancho de pantalla
            screen_height: Alto de pantalla
            gain: Factor de ganancia/sensibilidad
            deadzone: Umbral de zona muerta
            filter_min_cutoff: Parámetro del filtro OneEuro
            filter_beta: Parámetro del filtro OneEuro
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gain = gain
        self.logger = logger

        # Componentes
        self.face_detector = FaceDetector(logger=logger)
        self.calibration = Calibration(screen_width, screen_height, logger=logger)

        # Filtros
        self.filter_x = OneEuro(min_cutoff=filter_min_cutoff, beta=filter_beta)
        self.filter_y = OneEuro(min_cutoff=filter_min_cutoff, beta=filter_beta)
        self.deadzone_filter = DeadzoneFilter(threshold=deadzone)

        # Estado
        self.last_gaze_position: Optional[Tuple[float, float]] = None

    def process_frame(self, frame) -> Optional[Tuple[int, int]]:
        """
        Procesa un frame y retorna la posición del cursor

        Args:
            frame: Frame BGR de la cámara

        Returns:
            Tupla (x, y) de coordenadas de pantalla o None
        """
        # Detectar rostro
        results = self.face_detector.detect(frame)
        if not results:
            return None

        # Obtener posición de iris
        iris_pos = self.face_detector.get_iris_position(results)
        if not iris_pos:
            return None

        cx, cy = iris_pos
        now = time.time()

        # Aplicar zona muerta
        cx, cy = self.deadzone_filter.filter(cx, cy)

        # Aplicar filtro OneEuro
        fx = self.filter_x.filter(cx, now)
        fy = self.filter_y.filter(cy, now)

        # Aplicar ganancia y limitar
        gx = float(np.clip(fx * self.gain, 0.0, 1.0))
        gy = float(np.clip(fy * self.gain, 0.0, 1.0))

        # Mapear a coordenadas de pantalla
        screen_x, screen_y = self.calibration.map_to_screen(gx, gy)

        self.last_gaze_position = (gx, gy)
        return screen_x, screen_y

    def get_raw_gaze_position(self, frame) -> Optional[Tuple[float, float]]:
        """
        Obtiene la posición de mirada sin filtrar

        Returns:
            Tupla (cx, cy) normalizada o None
        """
        results = self.face_detector.detect(frame)
        if not results:
            return None

        return self.face_detector.get_iris_position(results)

    def detect_gestures(self, frame) -> dict:
        """
        Detecta gestos (guiños) en el frame

        Returns:
            Diccionario con información de gestos
        """
        results = self.face_detector.detect(frame)
        if not results:
            return {'left_wink': False, 'right_wink': False}

        ear_values = self.face_detector.get_eye_aspect_ratios(results)
        if not ear_values:
            return {'left_wink': False, 'right_wink': False}

        ear_left, ear_right = ear_values

        # Umbrales para detectar guiños
        WINK_THRESHOLD = 0.20

        return {
            'left_wink': ear_left < WINK_THRESHOLD and ear_right >= WINK_THRESHOLD,
            'right_wink': ear_right < WINK_THRESHOLD and ear_left >= WINK_THRESHOLD,
            'ear_left': ear_left,
            'ear_right': ear_right
        }

    def set_gain(self, gain: float):
        """Ajusta la ganancia/sensibilidad"""
        self.gain = max(0.5, min(2.5, gain))
        if self.logger:
            self.logger.info(f"Ganancia ajustada a {self.gain:.2f}")

    def set_deadzone(self, deadzone: float):
        """Ajusta el umbral de zona muerta"""
        self.deadzone_filter.threshold = deadzone
        if self.logger:
            self.logger.info(f"Zona muerta ajustada a {deadzone:.3f}")

    def reset_filters(self):
        """Resetea todos los filtros"""
        self.filter_x.reset()
        self.filter_y.reset()
        self.deadzone_filter.reset()
        if self.logger:
            self.logger.info("Filtros reseteados")

    def close(self):
        """Libera recursos"""
        self.face_detector.close()
