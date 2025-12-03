"""Manejo centralizado de errores"""
import logging
import traceback
from functools import wraps
from typing import Callable, Any


class ErrorHandler:
    """Maneja errores de forma centralizada"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def handle_camera_error(self, func: Callable) -> Callable:
        """Decorator para manejar errores de cámara"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error en cámara: {e}")
                self.logger.debug(traceback.format_exc())
                return None
        return wrapper

    def handle_mediapipe_error(self, func: Callable) -> Callable:
        """Decorator para manejar errores de MediaPipe"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error en MediaPipe: {e}")
                self.logger.debug(traceback.format_exc())
                return None
        return wrapper

    def handle_database_error(self, func: Callable) -> Callable:
        """Decorator para manejar errores de base de datos"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error en base de datos: {e}")
                self.logger.debug(traceback.format_exc())
                raise
        return wrapper

    def log_error(self, error: Exception, context: str = ""):
        """Registra un error con contexto"""
        self.logger.error(f"Error en {context}: {error}")
        self.logger.debug(traceback.format_exc())

    def safe_execute(self, func: Callable, default_return: Any = None,
                     error_msg: str = "Error en ejecución") -> Any:
        """
        Ejecuta una función de forma segura

        Args:
            func: Función a ejecutar
            default_return: Valor por defecto si hay error
            error_msg: Mensaje de error personalizado

        Returns:
            Resultado de la función o default_return en caso de error
        """
        try:
            return func()
        except Exception as e:
            self.logger.error(f"{error_msg}: {e}")
            self.logger.debug(traceback.format_exc())
            return default_return
