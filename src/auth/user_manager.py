"""Gestor de usuarios y autenticación"""
from typing import Optional, Dict, Any
import cv2 as cv
import time
from ..database.db_manager import DatabaseManager
from .face_auth import FaceAuthenticator


class UserManager:
    """Maneja el registro y autenticación de usuarios"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.face_auth = FaceAuthenticator(similarity_threshold=0.85, max_faces=3)
        self.current_user: Optional[Dict[str, Any]] = None
        self.current_session_id: Optional[int] = None

    def has_registered_user(self) -> bool:
        """Verifica si ya hay un usuario registrado"""
        user = self.db.get_registered_user()
        return user is not None

    def get_all_users(self):
        """Obtiene todos los usuarios registrados"""
        return self.db.get_all_users()

    def register_new_user(self, username: str, cap: cv.VideoCapture, num_samples: int = 10) -> bool:
        """
        Registra un nuevo usuario capturando múltiples muestras faciales

        Args:
            username: Nombre del usuario
            cap: VideoCapture de la cámara
            num_samples: Número de muestras a capturar

        Returns:
            True si el registro fue exitoso
        """

        self.face_auth.initialize()
        frames_captured = []

        print(f"Capturando {num_samples} muestras faciales...")
        print("Por favor, mira a la cámara y mueve ligeramente la cabeza")

        sample_count = 0
        last_capture_time = 0

        while sample_count < num_samples:
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv.flip(frame, 1)
            current_time = time.time()

            # Capturar una muestra cada 0.5 segundos
            if current_time - last_capture_time >= 0.5:
                # Verificar que se detecte un rostro
                embedding = self.face_auth.extract_face_embedding(frame)
                if embedding:
                    frames_captured.append(frame.copy())
                    sample_count += 1
                    last_capture_time = current_time
                    print(f"Muestra {sample_count}/{num_samples} capturada")

                    # Feedback visual
                    cv.putText(
                        frame,
                        f"Capturando: {sample_count}/{num_samples}",
                        (10, 30),
                        cv.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )
                else:
                    cv.putText(
                        frame,
                        "No se detecta rostro - Mira a la camara",
                        (10, 30),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )

            cv.imshow("Registro de Usuario", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                return False

        cv.destroyWindow("Registro de Usuario")

        # Crear embedding promedio
        face_embedding = self.face_auth.capture_multiple_embeddings(frames_captured)

        if not face_embedding:
            print("Error: No se pudo crear el embedding facial")
            return False

        # Guardar en la base de datos
        try:
            user_id = self.db.register_user(username, face_embedding)
            print(f"Usuario '{username}' registrado exitosamente (ID: {user_id})")
            return True
        except ValueError as e:
            print(f"Error al registrar usuario: {e}")
            return False

    def authenticate_user(self, frame) -> tuple[bool, float, int]:
        """
        Autentica al usuario logueado verificando entre múltiples rostros

        Returns:
            Tupla (autenticado, score_similitud, num_rostros_detectados)
        """
        # Obtener usuario logueado actualmente
        user = self.db.get_logged_in_user()
        if not user:
            return False, 0.0, 0

        self.face_auth.initialize()
        is_match, similarity, num_faces = self.face_auth.verify_face_multi(
            frame, user['face_embedding']
        )

        return is_match, similarity, num_faces

    def login(self, frame, user_id: Optional[int] = None) -> bool:
        """
        Realiza el login de un usuario verificando su rostro

        Args:
            frame: Frame de la cámara
            user_id: ID del usuario a loguear (si es None, intenta con el primer usuario registrado)

        Returns:
            True si el login fue exitoso
        """
        if user_id:
            user = self.db.get_user_by_id(user_id)
        else:
            user = self.db.get_registered_user()
        
        if not user:
            return False

        self.face_auth.initialize()
        is_match, similarity, _ = self.face_auth.verify_face_multi(frame, user['face_embedding'])

        if is_match:
            self.current_user = user
            self.db.set_user_logged_in(user['id'])
            self.current_session_id = self.db.start_session(user['id'])
            print(f"Login exitoso: {user['username']} (similitud: {similarity:.2%})")
            return True

        return False

    def select_and_login(self, frame) -> bool:
        """
        Muestra lista de usuarios y permite login con reconocimiento facial

        Returns:
            True si el login fue exitoso
        """
        users = self.db.get_all_users()
        if not users:
            print("No hay usuarios registrados")
            return False

        print("\n" + "=" * 60)
        print("USUARIOS REGISTRADOS")
        print("=" * 60)
        for i, user in enumerate(users, 1):
            print(f"{i}. {user['username']}")
        print("=" * 60)

        try:
            choice = input("\nSelecciona el número de usuario para login: ").strip()
            idx = int(choice) - 1
            
            if 0 <= idx < len(users):
                selected_user = users[idx]
                print(f"\nVerificando identidad de '{selected_user['username']}'...")
                print("Mira a la cámara...")
                
                return self.login(frame, user_id=selected_user['id'])
            else:
                print("Opción inválida")
                return False
        except (ValueError, IndexError):
            print("Entrada inválida")
            return False

    def logout(self):
        """Cierra la sesión actual"""
        if self.current_session_id:
            self.db.end_session(self.current_session_id)
        self.db.logout_all_users()
        self.current_user = None
        self.current_session_id = None
        self.face_auth.close()

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Retorna el usuario actual logueado"""
        return self.current_user

    def delete_current_user(self):
        """Elimina el usuario actual y todos sus datos"""
        user = self.db.get_registered_user()
        if user:
            self.db.delete_user(user['id'])
            self.current_user = None
            self.current_session_id = None
            print(f"Usuario {user['username']} eliminado")

    def save_user_config(self, key: str, value: Any):
        """Guarda una configuración del usuario actual"""
        if self.current_user:
            self.db.save_configuration(self.current_user['id'], key, value)

    def get_user_config(self, key: str, default: Any = None) -> Any:
        """Obtiene una configuración del usuario actual"""
        if self.current_user:
            return self.db.get_configuration(self.current_user['id'], key, default)
        return default

    def get_all_user_configs(self) -> Dict[str, Any]:
        """Obtiene todas las configuraciones del usuario actual"""
        if self.current_user:
            return self.db.get_all_configurations(self.current_user['id'])
        return {}
