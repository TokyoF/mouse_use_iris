"""Filtros para suavizado de movimientos"""
import math
import numpy as np


class OneEuro:
    """Filtro One-Euro para suavizado adaptativo"""

    def __init__(self, freq=60.0, min_cutoff=1.0, beta=0.02, dcutoff=1.0):
        """
        Args:
            freq: Frecuencia de muestreo en Hz
            min_cutoff: Frecuencia de corte mínima
            beta: Factor de adaptación a la velocidad
            dcutoff: Frecuencia de corte para la derivada
        """
        self.freq = freq
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.dcutoff = dcutoff
        self.x_prev = None
        self.dx_prev = None
        self.t_prev = None

    def alpha(self, cutoff):
        """Calcula el factor de suavizado"""
        te = 1.0 / self.freq
        tau = 1.0 / (2 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / te)

    def filter(self, x, t):
        """
        Aplica el filtro

        Args:
            x: Valor actual
            t: Timestamp actual

        Returns:
            Valor filtrado
        """
        if self.t_prev is None:
            self.t_prev = t
            self.x_prev = x
            self.dx_prev = 0.0
            return x

        # Calcular frecuencia actual
        self.freq = 1.0 / max(1e-6, t - self.t_prev)

        # Filtrar derivada
        dx = (x - self.x_prev) * self.freq
        a_d = self.alpha(self.dcutoff)
        dx_hat = a_d * dx + (1 - a_d) * self.dx_prev

        # Filtrar señal
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = self.alpha(cutoff)
        x_hat = a * x + (1 - a) * self.x_prev

        # Guardar estado
        self.t_prev = t
        self.x_prev = x_hat
        self.dx_prev = dx_hat

        return x_hat

    def reset(self):
        """Resetea el filtro"""
        self.x_prev = None
        self.dx_prev = None
        self.t_prev = None


class EMA:
    """Filtro de Media Móvil Exponencial (Exponential Moving Average)"""

    def __init__(self, alpha=0.7):
        """
        Args:
            alpha: Factor de suavizado (0-1). Valores más altos = menos suavizado
        """
        self.alpha = alpha
        self.x = None
        self.y = None

    def update(self, x, y):
        """
        Actualiza el filtro con nuevos valores

        Args:
            x: Coordenada x
            y: Coordenada y

        Returns:
            Tupla (x_filtrado, y_filtrado)
        """
        if self.x is None:
            self.x, self.y = x, y
        else:
            self.x = self.alpha * self.x + (1 - self.alpha) * x
            self.y = self.alpha * self.y + (1 - self.alpha) * y
        return self.x, self.y

    def reset(self):
        """Resetea el filtro"""
        self.x = None
        self.y = None


class DeadzoneFilter:
    """Filtro de zona muerta para eliminar micro-movimientos"""

    def __init__(self, threshold=0.015):
        """
        Args:
            threshold: Umbral de movimiento mínimo para considerar cambio
        """
        self.threshold = threshold
        self.last_x = None
        self.last_y = None

    def filter(self, x, y):
        """
        Aplica el filtro de zona muerta

        Args:
            x: Coordenada x actual
            y: Coordenada y actual

        Returns:
            Tupla (x, y) filtrada
        """
        if self.last_x is None or self.last_y is None:
            self.last_x, self.last_y = x, y
            return x, y

        # Solo actualizar si el movimiento supera el umbral
        if abs(x - self.last_x) < self.threshold and abs(y - self.last_y) < self.threshold:
            return self.last_x, self.last_y

        self.last_x, self.last_y = x, y
        return x, y

    def reset(self):
        """Resetea el filtro"""
        self.last_x = None
        self.last_y = None
