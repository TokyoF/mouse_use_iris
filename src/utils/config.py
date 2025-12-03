"""Configuración global de la aplicación"""
import json
from pathlib import Path
from typing import Any, Dict


class Config:
    """Maneja la configuración de la aplicación"""

    # Valores por defecto
    DEFAULTS = {
        # Gaze tracking
        'gain': 1.20,
        'deadzone': 0.015,
        'debug_mode': True,

        # Gestos
        'wink_threshold': 0.20,
        'wink_min_frames': 2,
        'double_wink_window': 0.60,

        # Dwell click
        'dwell_enabled': False,
        'dwell_time': 0.70,

        # Scroll
        'scroll_band': 0.08,
        'scroll_step': 80,

        # Filtros
        'filter_min_cutoff': 1.2,
        'filter_beta': 0.04,

        # Cámara
        'camera_index': 0,
        'camera_width': 640,
        'camera_height': 480,
        'camera_fps': 30,

        # MediaPipe
        'max_num_faces': 1,
        'min_detection_confidence': 0.6,
        'min_tracking_confidence': 0.6,

        # Autenticación
        'face_similarity_threshold': 0.85,
        'auth_check_interval': 2.0,  # segundos entre verificaciones

        # UI
        'show_camera_preview': True,
        'show_fps': True,
        'window_name': 'Gaze Control'
    }

    def __init__(self, config_file: str = "data/config.json"):
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Carga la configuración desde archivo"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Error cargando configuración: {e}")
                self.config = {}

        # Aplicar valores por defecto para claves faltantes
        for key, value in self.DEFAULTS.items():
            if key not in self.config:
                self.config[key] = value

    def save(self):
        """Guarda la configuración a archivo"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Establece un valor de configuración"""
        self.config[key] = value

    def get_all(self) -> Dict[str, Any]:
        """Obtiene toda la configuración"""
        return self.config.copy()

    def reset_to_defaults(self):
        """Resetea la configuración a valores por defecto"""
        self.config = self.DEFAULTS.copy()
        self.save()
