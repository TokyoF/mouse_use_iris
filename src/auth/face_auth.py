"""Autenticación facial usando MediaPipe y embeddings"""
import numpy as np
import cv2 as cv
import mediapipe as mp
from typing import Optional, Tuple
import pickle


class FaceAuthenticator:
    """Maneja la autenticación facial mediante embeddings de landmarks"""

    def __init__(self, similarity_threshold: float = 0.85, max_faces: int = 3):
        """
        Args:
            similarity_threshold: Umbral de similitud para considerar un match (0-1)
            max_faces: Número máximo de rostros a detectar simultáneamente
        """
        self.similarity_threshold = similarity_threshold
        self.max_faces = max_faces
        self.mp_face = mp.solutions.face_mesh
        self.face_mesh = None

    def initialize(self):
        """Inicializa el detector de rostros"""
        self.face_mesh = self.mp_face.FaceMesh(
            max_num_faces=self.max_faces,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def extract_face_embedding(self, frame: np.ndarray) -> Optional[bytes]:
        """
        Extrae el embedding facial de un frame

        Args:
            frame: Frame de la cámara en formato BGR

        Returns:
            Embedding serializado o None si no se detecta rostro
        """
        if self.face_mesh is None:
            self.initialize()

        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return None

        # Extraer landmarks como embedding
        landmarks = results.multi_face_landmarks[0].landmark

        # Crear vector de características con coordenadas normalizadas
        embedding = []
        for lm in landmarks:
            embedding.extend([lm.x, lm.y, lm.z])

        embedding_array = np.array(embedding, dtype=np.float32)

        # Normalizar el embedding
        embedding_array = self._normalize_embedding(embedding_array)

        return pickle.dumps(embedding_array)

    def _normalize_embedding(self, embedding: np.ndarray) -> np.ndarray:
        """Normaliza el embedding facial"""
        # Normalización L2
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding

    def verify_face(self, frame: np.ndarray, registered_embedding: bytes) -> Tuple[bool, float]:
        """
        Verifica si el rostro en el frame coincide con el embedding registrado

        Args:
            frame: Frame de la cámara
            registered_embedding: Embedding facial registrado

        Returns:
            Tupla (es_match, score_similitud)
        """
        current_embedding_bytes = self.extract_face_embedding(frame)

        if current_embedding_bytes is None:
            return False, 0.0

        current_embedding = pickle.loads(current_embedding_bytes)
        registered = pickle.loads(registered_embedding)

        # Calcular similitud usando cosine similarity
        similarity = self._cosine_similarity(current_embedding, registered)

        is_match = similarity >= self.similarity_threshold
        return is_match, similarity

    def verify_face_multi(self, frame: np.ndarray, registered_embedding: bytes) -> Tuple[bool, float, int]:
        """
        Verifica si algún rostro en el frame coincide con el embedding registrado.
        Detecta múltiples rostros y retorna el mejor match.

        Args:
            frame: Frame de la cámara
            registered_embedding: Embedding facial registrado

        Returns:
            Tupla (es_match, mejor_score_similitud, num_rostros_detectados)
        """
        if self.face_mesh is None:
            self.initialize()

        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return False, 0.0, 0

        num_faces = len(results.multi_face_landmarks)
        registered = pickle.loads(registered_embedding)
        
        best_similarity = 0.0
        is_match = False

        # Revisar cada rostro detectado
        for face_landmarks in results.multi_face_landmarks:
            # Crear embedding para este rostro
            embedding = []
            for lm in face_landmarks.landmark:
                embedding.extend([lm.x, lm.y, lm.z])
            
            embedding_array = np.array(embedding, dtype=np.float32)
            embedding_array = self._normalize_embedding(embedding_array)

            # Calcular similitud
            similarity = self._cosine_similarity(embedding_array, registered)
            
            if similarity > best_similarity:
                best_similarity = similarity

        is_match = best_similarity >= self.similarity_threshold
        return is_match, best_similarity, num_faces

    def _cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Calcula la similitud coseno entre dos embeddings"""
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)
        return float(similarity)

    def capture_multiple_embeddings(self, frames: list) -> Optional[bytes]:
        """
        Captura múltiples embeddings y retorna el promedio para mayor robustez

        Args:
            frames: Lista de frames para procesar

        Returns:
            Embedding promedio serializado
        """
        embeddings = []

        for frame in frames:
            emb_bytes = self.extract_face_embedding(frame)
            if emb_bytes:
                embeddings.append(pickle.loads(emb_bytes))

        if not embeddings:
            return None

        # Promediar los embeddings
        avg_embedding = np.mean(embeddings, axis=0)
        avg_embedding = self._normalize_embedding(avg_embedding)

        return pickle.dumps(avg_embedding)

    def close(self):
        """Libera recursos"""
        if self.face_mesh:
            self.face_mesh.close()
            self.face_mesh = None
