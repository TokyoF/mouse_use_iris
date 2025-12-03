"""Controlador del mouse con gestos"""
import pyautogui
import platform
import time
import logging
from collections import deque
from typing import Optional


class MouseController:
    """Controla el mouse y ejecuta acciones basadas en gestos"""

    def __init__(self, wink_threshold: float = 0.20, wink_min_frames: int = 2,
                 double_wink_window: float = 0.60, dwell_time: float = 0.70,
                 scroll_band: float = 0.08, scroll_step: int = 80,
                 logger: Optional[logging.Logger] = None):
        """
        Args:
            wink_threshold: Umbral EAR para detectar guiño
            wink_min_frames: Frames mínimos para confirmar guiño
            double_wink_window: Ventana de tiempo para doble guiño (segundos)
            dwell_time: Tiempo para dwell click (segundos)
            scroll_band: Tamaño de banda para scroll automático (0-1)
            scroll_step: Pasos de scroll
        """
        self.wink_threshold = wink_threshold
        self.wink_min_frames = wink_min_frames
        self.double_wink_window = double_wink_window
        self.dwell_time = dwell_time
        self.scroll_band = scroll_band
        self.scroll_step = scroll_step
        self.logger = logger

        # Configurar pyautogui
        pyautogui.FAILSAFE = True
        self.is_mac = platform.system() == "Darwin"

        # Estado de gestos
        self.left_wink_frames = 0
        self.right_wink_frames = 0
        self.last_left_winks = deque()

        # Nuevos gestos avanzados
        self.left_closed_frames = 0  # Para click derecho
        self.right_closed_frames = 0  # Para cambio de pestañas
        self.right_closed_start_x = None  # Posición inicial cuando se cierra ojo derecho
        self.tab_switch_threshold = 0.15  # Umbral de movimiento para cambiar pestaña
        self.right_click_hold_time = 15  # Frames sostenidos para click derecho (~0.5s)

        # Dwell click
        self.dwell_enabled = False
        self.dwell_start_time: Optional[float] = None
        self.dwell_ref_position: Optional[tuple] = None

    def move_to(self, x: int, y: int):
        """
        Mueve el cursor a la posición especificada

        Args:
            x: Coordenada x
            y: Coordenada y
        """
        try:
            pyautogui.moveTo(x, y, _pause=False)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error moviendo mouse: {e}")

    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = 'left'):
        """
        Ejecuta un click

        Args:
            x: Coordenada x (None = posición actual)
            y: Coordenada y (None = posición actual)
            button: Botón del mouse ('left' o 'right')
        """
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y, button=button)
            else:
                pyautogui.click(button=button)

            if self.logger:
                self.logger.debug(f"Click {button} en ({x}, {y})")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error en click: {e}")

    def right_click(self, x: Optional[int] = None, y: Optional[int] = None):
        """
        Ejecuta un click derecho

        Args:
            x: Coordenada x (None = posición actual)
            y: Coordenada y (None = posición actual)
        """
        self.click(x, y, button='right')
        if self.logger:
            self.logger.debug(f"Click derecho en ({x}, {y})")

    def page_forward(self):
        """Navega hacia adelante en el navegador"""
        try:
            key = "command" if self.is_mac else "alt"
            pyautogui.hotkey(key, "right")
            if self.logger:
                self.logger.debug("Página adelante")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error en página adelante: {e}")

    def page_back(self):
        """Navega hacia atrás en el navegador"""
        try:
            key = "command" if self.is_mac else "alt"
            pyautogui.hotkey(key, "left")
            if self.logger:
                self.logger.debug("Página atrás")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error en página atrás: {e}")

    def switch_tab_next(self):
        """Cambia a la siguiente pestaña del navegador"""
        try:
            key = "command" if self.is_mac else "ctrl"
            pyautogui.hotkey(key, "tab")
            if self.logger:
                self.logger.debug("Cambio a siguiente pestaña")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error cambiando pestaña: {e}")

    def switch_tab_prev(self):
        """Cambia a la pestaña anterior del navegador"""
        try:
            key = "command" if self.is_mac else "ctrl"
            pyautogui.hotkey(key, "shift", "tab")
            if self.logger:
                self.logger.debug("Cambio a pestaña anterior")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error cambiando pestaña: {e}")

    def switch_window_next(self):
        """Cambia a la siguiente ventana/aplicación"""
        try:
            if self.is_mac:
                pyautogui.hotkey("command", "tab")
            else:
                pyautogui.hotkey("alt", "tab")
            if self.logger:
                self.logger.debug("Cambio a siguiente ventana")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error cambiando ventana: {e}")

    def scroll(self, amount: int):
        """
        Ejecuta scroll

        Args:
            amount: Cantidad de scroll (positivo = arriba, negativo = abajo)
        """
        try:
            pyautogui.scroll(amount)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error en scroll: {e}")

    def process_gestures(self, gestures: dict, x: int, y: int, gaze_x: Optional[float] = None):
        """
        Procesa gestos y ejecuta acciones

        Args:
            gestures: Diccionario con información de gestos
            x: Posición x actual del cursor
            y: Posición y actual del cursor
            gaze_x: Posición x normalizada de la mirada (0-1) para detectar movimiento horizontal
        """
        ear_left = gestures.get('ear_left', 1.0)
        ear_right = gestures.get('ear_right', 1.0)

        # ===== NUEVO: Ojo izquierdo cerrado sostenido = Click derecho =====
        if ear_left < self.wink_threshold and ear_right >= self.wink_threshold:
            self.left_closed_frames += 1

            # Click derecho si se mantiene cerrado suficiente tiempo
            if self.left_closed_frames == self.right_click_hold_time:
                self.right_click(x, y)
                if self.logger:
                    self.logger.info("Click derecho activado (ojo izquierdo sostenido)")

            # Click izquierdo normal para guiños cortos
            self.left_wink_frames += 1
        else:
            # Guiño corto = Click izquierdo
            if self.wink_min_frames <= self.left_wink_frames < self.right_click_hold_time:
                self.click(x, y)

                # Registrar para doble guiño
                now = time.time()
                self.last_left_winks.append(now)

                # Limpiar ventana de tiempo
                while (self.last_left_winks and
                       now - self.last_left_winks[0] > self.double_wink_window):
                    self.last_left_winks.popleft()

                # Detectar doble guiño = Página adelante
                if len(self.last_left_winks) >= 2:
                    self.page_forward()
                    self.last_left_winks.clear()

            self.left_wink_frames = 0
            self.left_closed_frames = 0

        # ===== NUEVO: Ojo derecho cerrado + movimiento = Cambio de pestañas =====
        if ear_right < self.wink_threshold and ear_left >= self.wink_threshold:
            self.right_closed_frames += 1

            # Guardar posición inicial cuando se cierra el ojo
            if self.right_closed_frames == 1 and gaze_x is not None:
                self.right_closed_start_x = gaze_x

            # Detectar movimiento horizontal con ojo cerrado
            elif self.right_closed_frames > 5 and gaze_x is not None and self.right_closed_start_x is not None:
                movement = gaze_x - self.right_closed_start_x

                # Movimiento a la derecha = Siguiente pestaña
                if movement > self.tab_switch_threshold:
                    self.switch_tab_next()
                    self.right_closed_start_x = gaze_x  # Reset para evitar múltiples cambios
                    if self.logger:
                        self.logger.info("Cambio a siguiente pestaña (ojo derecho + derecha)")

                # Movimiento a la izquierda = Pestaña anterior
                elif movement < -self.tab_switch_threshold:
                    self.switch_tab_prev()
                    self.right_closed_start_x = gaze_x  # Reset
                    if self.logger:
                        self.logger.info("Cambio a pestaña anterior (ojo derecho + izquierda)")

            # Guiño corto tradicional
            self.right_wink_frames += 1
        else:
            # Guiño derecho corto = Página atrás (comportamiento original)
            if self.wink_min_frames <= self.right_wink_frames < 10:
                self.page_back()

            self.right_wink_frames = 0
            self.right_closed_frames = 0
            self.right_closed_start_x = None

    def process_dwell_click(self, gaze_x: float, gaze_y: float,
                           screen_x: int, screen_y: int):
        """
        Procesa dwell click (click por mirada sostenida)

        Args:
            gaze_x: Coordenada x de mirada normalizada
            gaze_y: Coordenada y de mirada normalizada
            screen_x: Coordenada x de pantalla
            screen_y: Coordenada y de pantalla
        """
        if not self.dwell_enabled:
            self.dwell_start_time = None
            self.dwell_ref_position = None
            return

        now = time.time()
        current_pos = (gaze_x, gaze_y)

        if self.dwell_start_time is None:
            self.dwell_start_time = now
            self.dwell_ref_position = current_pos
        else:
            # Verificar si se mantiene en la misma posición
            dx = abs(current_pos[0] - self.dwell_ref_position[0])
            dy = abs(current_pos[1] - self.dwell_ref_position[1])

            deadzone = 0.02  # Zona muerta para dwell

            if dx < deadzone and dy < deadzone:
                if now - self.dwell_start_time > self.dwell_time:
                    self.click(screen_x, screen_y)
                    self.dwell_start_time = now
            else:
                self.dwell_start_time = now
                self.dwell_ref_position = current_pos

    def process_auto_scroll(self, gaze_y: float):
        """
        Procesa scroll automático en los bordes de la pantalla

        Args:
            gaze_y: Coordenada y de mirada normalizada (0-1)
        """
        if gaze_y < self.scroll_band:
            # Scroll hacia arriba
            self.scroll(self.scroll_step)
        elif gaze_y > 1.0 - self.scroll_band:
            # Scroll hacia abajo
            self.scroll(-self.scroll_step)

    def toggle_dwell(self):
        """Activa/desactiva dwell click"""
        self.dwell_enabled = not self.dwell_enabled
        if self.logger:
            state = "activado" if self.dwell_enabled else "desactivado"
            self.logger.info(f"Dwell click {state}")
        return self.dwell_enabled
