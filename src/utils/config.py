"""Configuración global de la aplicación"""
import json
from pathlib import Path
from typing import Any, Dict


class Config:
    """Maneja la configuración de la aplicación"""

    # Perfiles de sensibilidad predefinidos
    SENSITIVITY_PROFILES = {
        'conservative': {
            'gain': 1.0,
            'deadzone': 0.020,
            'filter_min_cutoff': 0.8,
            'filter_beta': 0.03,
            'description': 'Movimiento lento y suave, ideal para principiantes'
        },
        'balanced': {
            'gain': 1.4,
            'deadzone': 0.012,
            'filter_min_cutoff': 1.5,
            'filter_beta': 0.05,
            'description': 'Balance entre precisión y velocidad'
        },
        'performance': {
            'gain': 1.85,
            'deadzone': 0.008,
            'filter_min_cutoff': 2.0,
            'filter_beta': 0.08,
            'description': 'Alta velocidad, menor movimiento de cabeza requerido (por defecto)'
        },
        'extreme': {
            'gain': 2.3,
            'deadzone': 0.005,
            'filter_min_cutoff': 2.5,
            'filter_beta': 0.12,
            'description': 'Máxima velocidad, requiere buen control'
        }
    }

    # Valores por defecto (Perfil Performance)
    DEFAULTS = {
        # Gaze tracking - OPTIMIZADO PARA ALTA PERFORMANCE
        'gain': 1.85,  # Aumentado de 1.20 → Mayor sensibilidad
        'deadzone': 0.008,  # Reducido de 0.015 → Menor movimiento requerido
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

        # Filtros - OPTIMIZADO PARA RESPUESTA RÁPIDA
        'filter_min_cutoff': 2.0,  # Aumentado de 1.2 → Más responsivo
        'filter_beta': 0.08,  # Aumentado de 0.04 → Mejor respuesta a movimientos rápidos

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

    def apply_sensitivity_profile(self, profile_name: str) -> bool:
        """
        Aplica un perfil de sensibilidad predefinido
        
        Args:
            profile_name: Nombre del perfil ('conservative', 'balanced', 'performance', 'extreme')
            
        Returns:
            True si el perfil existe y fue aplicado
        """
        if profile_name not in self.SENSITIVITY_PROFILES:
            return False
        
        profile = self.SENSITIVITY_PROFILES[profile_name]
        
        # Aplicar parámetros del perfil
        self.config['gain'] = profile['gain']
        self.config['deadzone'] = profile['deadzone']
        self.config['filter_min_cutoff'] = profile['filter_min_cutoff']
        self.config['filter_beta'] = profile['filter_beta']
        
        self.save()
        return True
    
    def list_sensitivity_profiles(self):
        """Muestra todos los perfiles de sensibilidad disponibles"""
        print("\n" + "=" * 60)
        print("PERFILES DE SENSIBILIDAD DISPONIBLES")
        print("=" * 60)
        for name, profile in self.SENSITIVITY_PROFILES.items():
            print(f"\n[{name.upper()}]")
            print(f"  Descripción: {profile['description']}")
            print(f"  Gain: {profile['gain']}")
            print(f"  Deadzone: {profile['deadzone']}")
            print(f"  Min Cutoff: {profile['filter_min_cutoff']}")
            print(f"  Beta: {profile['filter_beta']}")
        print("=" * 60)
