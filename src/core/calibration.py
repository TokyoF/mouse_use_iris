"""Sistema de calibración para mapeo gaze-to-screen"""
import numpy as np
from typing import List, Tuple, Optional
import logging


class Calibration:
    """Maneja la calibración afín 2D para mapeo de mirada a pantalla"""

    def __init__(self, screen_width: int, screen_height: int,
                 logger: Optional[logging.Logger] = None):
        """
        Args:
            screen_width: Ancho de la pantalla en píxeles
            screen_height: Alto de la pantalla en píxeles
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.logger = logger

        self.calibration_matrix: Optional[np.ndarray] = None
        self.samples_src: List[Tuple[float, float]] = []
        self.samples_dst: List[Tuple[int, int]] = []

    def get_grid_points(self, rows: int = 3, cols: int = 3) -> List[Tuple[int, int]]:
        """
        Genera puntos de calibración en una grilla

        Args:
            rows: Número de filas
            cols: Número de columnas

        Returns:
            Lista de puntos (x, y) en coordenadas de pantalla
        """
        points = []
        margin_x = 0.15
        margin_y = 0.15

        for row in range(rows):
            y_ratio = margin_y + (row / max(1, rows - 1)) * (1 - 2 * margin_y)
            y = int(self.screen_height * y_ratio)

            for col in range(cols):
                x_ratio = margin_x + (col / max(1, cols - 1)) * (1 - 2 * margin_x)
                x = int(self.screen_width * x_ratio)
                points.append((x, y))

        return points

    def add_sample(self, gaze_x: float, gaze_y: float, screen_x: int, screen_y: int):
        """
        Añade una muestra de calibración

        Args:
            gaze_x: Coordenada x de la mirada (normalizada 0-1)
            gaze_y: Coordenada y de la mirada (normalizada 0-1)
            screen_x: Coordenada x de pantalla en píxeles
            screen_y: Coordenada y de pantalla en píxeles
        """
        self.samples_src.append((gaze_x, gaze_y))
        self.samples_dst.append((screen_x, screen_y))

        if self.logger:
            self.logger.debug(
                f"Muestra añadida: gaze=({gaze_x:.3f}, {gaze_y:.3f}) -> "
                f"screen=({screen_x}, {screen_y})"
            )

    def compute_calibration(self) -> bool:
        """
        Calcula la matriz de calibración usando mínimos cuadrados

        Returns:
            True si la calibración fue exitosa
        """
        if len(self.samples_src) < 3:
            if self.logger:
                self.logger.warning(
                    f"Muestras insuficientes para calibración: {len(self.samples_src)}/3"
                )
            return False

        try:
            # Preparar matrices para mínimos cuadrados
            X = []
            Yx = []
            Yy = []

            for (cx, cy), (px, py) in zip(self.samples_src, self.samples_dst):
                X.append([cx, cy, 1.0])
                Yx.append(px)
                Yy.append(py)

            X = np.array(X)
            Yx = np.array(Yx)
            Yy = np.array(Yy)

            # Resolver sistemas de ecuaciones
            ax, _residuals, _rank, _s = np.linalg.lstsq(X, Yx, rcond=None)
            ay, _residuals, _rank, _s = np.linalg.lstsq(X, Yy, rcond=None)

            # Construir matriz de transformación
            self.calibration_matrix = np.vstack([ax, ay])

            if self.logger:
                self.logger.info(
                    f"Calibración completada con {len(self.samples_src)} muestras"
                )

            return True

        except Exception as e:
            if self.logger:
                self.logger.error(f"Error en calibración: {e}")
            return False

    def map_to_screen(self, gaze_x: float, gaze_y: float) -> Tuple[int, int]:
        """
        Mapea coordenadas de mirada a coordenadas de pantalla

        Args:
            gaze_x: Coordenada x de mirada (normalizada 0-1)
            gaze_y: Coordenada y de mirada (normalizada 0-1)

        Returns:
            Tupla (x, y) en coordenadas de pantalla
        """
        if self.calibration_matrix is None:
            # Sin calibración, usar mapeo lineal simple
            x = int(gaze_x * self.screen_width)
            y = int(gaze_y * self.screen_height)
        else:
            # Aplicar transformación afín
            v = np.array([gaze_x, gaze_y, 1.0])
            xy = self.calibration_matrix @ v
            x = int(xy[0])
            y = int(xy[1])

        # Asegurar que está dentro de los límites
        x = np.clip(x, 0, self.screen_width - 1)
        y = np.clip(y, 0, self.screen_height - 1)

        return x, y

    def clear_samples(self):
        """Limpia las muestras de calibración"""
        self.samples_src.clear()
        self.samples_dst.clear()
        if self.logger:
            self.logger.info("Muestras de calibración limpiadas")

    def reset(self):
        """Resetea la calibración completamente"""
        self.calibration_matrix = None
        self.clear_samples()
        if self.logger:
            self.logger.info("Calibración reseteada")

    def is_calibrated(self) -> bool:
        """Verifica si hay una calibración activa"""
        return self.calibration_matrix is not None

    def get_calibration_data(self):
        """Retorna los datos de calibración para persistencia"""
        return {
            'matrix': self.calibration_matrix,
            'samples_src': self.samples_src.copy(),
            'samples_dst': self.samples_dst.copy()
        }

    def load_calibration_data(self, data: dict):
        """Carga datos de calibración desde persistencia"""
        self.calibration_matrix = data.get('matrix')
        self.samples_src = data.get('samples_src', [])
        self.samples_dst = data.get('samples_dst', [])

        if self.logger:
            self.logger.info("Calibración cargada desde datos guardados")
