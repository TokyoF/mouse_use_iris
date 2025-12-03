"""Detector facial usando MediaPipe"""
import cv2 as cv
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple, List
import logging


class FaceDetector:
    """Detector facial con MediaPipe Face Mesh"""

    # Índices de landmarks
    LEFT_EYE = [33, 133, 160, 144, 159, 145]
    RIGHT_EYE = [263, 362, 387, 373, 386, 374]
    LEFT_IRIS_CENTER = 468
    RIGHT_IRIS_CENTER = 473

    def __init__(self, max_num_faces=1, min_detection_confidence=0.6,
                 min_tracking_confidence=0.6, logger: Optional[logging.Logger] = None):
        """
        Args:
            max_num_faces: Número máximo de rostros a detectar
            min_detection_confidence: Confianza mínima de detección
            min_tracking_confidence: Confianza mínima de tracking
        """
        self.max_num_faces = max_num_faces
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.logger = logger

        self.mp_face = mp.solutions.face_mesh
        self.face_mesh = None
        self._initialize()

    def _initialize(self):
        """Inicializa MediaPipe Face Mesh"""
        try:
            self.face_mesh = self.mp_face.FaceMesh(
                max_num_faces=self.max_num_faces,
                refine_landmarks=True,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence
            )
            if self.logger:
                self.logger.info("Face Mesh inicializado correctamente")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error inicializando Face Mesh: {e}")
            raise

    def detect(self, frame: np.ndarray) -> Optional[object]:
        """
        Detecta rostros en el frame

        Args:
            frame: Frame BGR de OpenCV

        Returns:
            Resultado de la detección o None
        """
        if self.face_mesh is None:
            self._initialize()

        try:
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb)
            return results
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error en detección: {e}")
            return None

    def get_iris_position(self, results) -> Optional[Tuple[float, float]]:
        """
        Obtiene la posición del centro de los iris

        Args:
            results: Resultado de MediaPipe

        Returns:
            Tupla (cx, cy) normalizada o None
        """
        if not results or not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0].landmark

        if len(landmarks) <= max(self.LEFT_IRIS_CENTER, self.RIGHT_IRIS_CENTER):
            return None

        # Promedio de ambos iris
        left_iris = landmarks[self.LEFT_IRIS_CENTER]
        right_iris = landmarks[self.RIGHT_IRIS_CENTER]

        cx = (left_iris.x + right_iris.x) / 2.0
        cy = (left_iris.y + right_iris.y) / 2.0

        return cx, cy

    def calculate_ear(self, landmarks, eye_indices: List[int]) -> float:
        """
        Calcula el Eye Aspect Ratio para detectar guiños

        Args:
            landmarks: Landmarks de MediaPipe
            eye_indices: Índices de los puntos del ojo

        Returns:
            EAR (Eye Aspect Ratio)
        """
        points = [np.array([landmarks[i].x, landmarks[i].y]) for i in eye_indices]

        # Distancias verticales
        v1 = np.linalg.norm(points[2] - points[5])
        v2 = np.linalg.norm(points[3] - points[4])

        # Distancia horizontal
        h = np.linalg.norm(points[0] - points[1])

        # EAR
        ear = (v1 + v2) / (2.0 * h + 1e-6)
        return ear

    def get_eye_aspect_ratios(self, results) -> Optional[Tuple[float, float]]:
        """
        Obtiene los EAR de ambos ojos

        Returns:
            Tupla (ear_izquierdo, ear_derecho) o None
        """
        if not results or not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0].landmark

        ear_left = self.calculate_ear(landmarks, self.LEFT_EYE)
        ear_right = self.calculate_ear(landmarks, self.RIGHT_EYE)

        return ear_left, ear_right

    def draw_landmarks(self, frame: np.ndarray, results):
        """
        Dibuja los landmarks en el frame

        Args:
            frame: Frame para dibujar
            results: Resultados de MediaPipe
        """
        if not results or not results.multi_face_landmarks:
            return

        landmarks = results.multi_face_landmarks[0].landmark
        h, w = frame.shape[:2]

        # Dibujar iris
        if len(landmarks) > max(self.LEFT_IRIS_CENTER, self.RIGHT_IRIS_CENTER):
            for idx in [self.LEFT_IRIS_CENTER, self.RIGHT_IRIS_CENTER]:
                x = int(landmarks[idx].x * w)
                y = int(landmarks[idx].y * h)
                cv.circle(frame, (x, y), 3, (0, 255, 0), -1)

        # Dibujar contornos de ojos
        for idx in self.LEFT_EYE + self.RIGHT_EYE:
            if idx < len(landmarks):
                x = int(landmarks[idx].x * w)
                y = int(landmarks[idx].y * h)
                cv.circle(frame, (x, y), 1, (255, 0, 0), -1)

    def close(self):
        """Libera recursos"""
        if self.face_mesh:
            self.face_mesh.close()
            self.face_mesh = None
            if self.logger:
                self.logger.info("Face Mesh cerrado")
