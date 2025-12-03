"""
Detector facial alternativo sin MediaPipe
Usa OpenCV Cascade Classifier como fallback
"""
import cv2 as cv
import numpy as np
from typing import Optional, Tuple, List


class AlternativeFaceDetector:
    """Detector facial usando OpenCV sin MediaPipe"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_eye.xml')
        
        if self.face_cascade.empty():
            if logger:
                logger.error("No se pudo cargar el clasificador de rostros")
            raise RuntimeError("Error cargando haarcascade")
            
    def detect_face(self, frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detecta el rostro más grande en el frame
        
        Returns:
            Tuple (x, y, w, h) o None si no se detecta rostro
        """
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Retornar el rostro más grande
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            return tuple(largest_face)
            
        return None
        
    def get_gaze_position(self, frame: np.ndarray) -> Optional[Tuple[float, float]]:
        """
        Estima la posición de la mirada basada en el centro del rostro
        
        Returns:
            Tuple (x, y) normalizadas (0-1) o None
        """
        face_rect = self.detect_face(frame)
        if face_rect is None:
            return None
            
        x, y, w, h = face_rect
        
        # El centro del rostro es una aproximación de la mirada
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Normalizar a 0-1
        h_img, w_img = frame.shape[:2]
        norm_x = center_x / w_img
        norm_y = center_y / h_img
        
        return (norm_x, norm_y)
        
    def detect_eyes(self, frame: np.ndarray, face_rect: Tuple[int, int, int, int]) -> List[Tuple[int, int, int, int]]:
        """
        Detecta ojos dentro de un rostro
        
        Returns:
            Lista de rectángulos de ojos [(x, y, w, h), ...]
        """
        x, y, w, h = face_rect
        roi_gray = cv.cvtColor(frame[y:y+h, x:x+w], cv.COLOR_BGR2GRAY)
        
        eyes = self.eye_cascade.detectMultiScale(roi_gray)
        
        # Ajustar coordenadas relativas al frame completo
        eye_rects = []
        for (ex, ey, ew, eh) in eyes:
            eye_rects.append((x + ex, y + ey, ew, eh))
            
        return eye_rects
        
    def get_eye_aspect_ratio(self, frame: np.ndarray, eye_rect: Tuple[int, int, int, int]) -> float:
        """
        Calcula una métrica simple para detectar si el ojo está cerrado
        
        Returns:
            EAR-like value (menor = ojo más cerrado)
        """
        x, y, w, h = eye_rect
        
        # Métrica simple: ratio altura/anchura
        if w > 0:
            return h / w
        return 0.0
        
    def draw_detections(self, frame: np.ndarray, face_rect: Optional[Tuple] = None, 
                       eye_rects: List[Tuple] = None) -> np.ndarray:
        """
        Dibuja las detecciones en el frame
        """
        result = frame.copy()
        
        if face_rect:
            x, y, w, h = face_rect
            cv.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Dibujar punto central (mirada estimada)
            center_x = x + w // 2
            center_y = y + h // 2
            cv.circle(result, (center_x, center_y), 5, (0, 0, 255), -1)
            
        if eye_rects:
            for (ex, ey, ew, eh) in eye_rects:
                cv.rectangle(result, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
                
        return result


class AlternativeGazeTracker:
    """Seguimiento de mirada alternativo sin MediaPipe"""
    
    def __init__(self, screen_width: int, screen_height: int, 
                 gain: float = 1.2, deadzone: float = 0.015, logger=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gain = gain
        self.deadzone = deadzone
        self.logger = logger
        
        self.face_detector = AlternativeFaceDetector(logger)
        self.last_position = None
        
    def process_frame(self, frame: np.ndarray) -> Optional[Tuple[int, int]]:
        """
        Procesa un frame y retorna la posición del cursor
        """
        gaze_pos = self.face_detector.get_gaze_position(frame)
        
        if gaze_pos is None:
            return None
            
        gaze_x, gaze_y = gaze_pos
        
        # Aplicar ganancia
        gaze_x = np.clip(gaze_x * self.gain, 0.0, 1.0)
        gaze_y = np.clip(gaze_y * self.gain, 0.0, 1.0)
        
        # Deadzone simple
        if self.last_position:
            last_x, last_y = self.last_position
            if abs(gaze_x - last_x) < self.deadzone and abs(gaze_y - last_y) < self.deadzone:
                gaze_x, gaze_y = last_x, last_y
                
        self.last_position = (gaze_x, gaze_y)
        
        # Mapear a coordenadas de pantalla
        screen_x = int(gaze_x * self.screen_width)
        screen_y = int(gaze_y * self.screen_height)
        
        return (screen_x, screen_y)
        
    def detect_gestures(self, frame: np.ndarray) -> dict:
        """
        Detecta gestos básicos (simplificado sin MediaPipe)
        """
        face_rect = self.face_detector.detect_face(frame)
        
        if face_rect is None:
            return {}
            
        # Detectar ojos
        eye_rects = self.face_detector.detect_eyes(frame, face_rect)
        
        gestures = {}
        
        # Calcular EAR para cada ojo
        ear_values = []
        for eye_rect in eye_rects:
            ear = self.face_detector.get_eye_aspect_ratio(frame, eye_rect)
            ear_values.append(ear)
            
        # Detección simple de guiños
        if len(ear_values) >= 2:
            left_ear, right_ear = ear_values[:2]
            
            # Umbral simple para detección de guiño
            wink_threshold = 0.3
            
            if left_ear < wink_threshold and right_ear >= wink_threshold:
                gestures['left_wink'] = True
            elif right_ear < wink_threshold and left_ear >= wink_threshold:
                gestures['right_wink'] = True
                
        return gestures
        
    def draw_debug_info(self, frame: np.ndarray) -> np.ndarray:
        """
        Dibuja información de depuración
        """
        face_rect = self.face_detector.detect_face(frame)
        eye_rects = []
        
        if face_rect:
            eye_rects = self.face_detector.detect_eyes(frame, face_rect)
            
        return self.face_detector.draw_detections(frame, face_rect, eye_rects)