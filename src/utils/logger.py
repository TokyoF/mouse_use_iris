"""Sistema de logging para la aplicación"""
import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "GazeControl", log_dir: str = "data/logs") -> logging.Logger:
    """
    Configura el sistema de logging

    Args:
        name: Nombre del logger
        log_dir: Directorio para guardar los logs

    Returns:
        Logger configurado
    """
    # Crear directorio de logs
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Evitar duplicar handlers
    if logger.handlers:
        return logger

    # Formato de logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para archivo (rotación diaria)
    log_file = log_path / f"gaze_control_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
