"""Gestor de base de datos SQLite para usuarios y configuraciones"""
import sqlite3
import json
import pickle
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


class DatabaseManager:
    """Maneja todas las operaciones de base de datos"""

    def __init__(self, db_path: str = "data/users.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: Optional[sqlite3.Connection] = None
        self._initialize_database()

    def _initialize_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                face_embedding BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        """)

        # Tabla de configuraciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS configurations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                config_key TEXT NOT NULL,
                config_value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, config_key)
            )
        """)

        # Tabla de calibraciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calibrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                calibration_matrix BLOB NOT NULL,
                samples_src BLOB NOT NULL,
                samples_dst BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Tabla de sesiones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                duration_seconds INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        self.conn.commit()

    def register_user(self, username: str, face_embedding: bytes) -> int:
        """Registra un nuevo usuario con su embedding facial"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, face_embedding) VALUES (?, ?)",
                (username, face_embedding)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"El usuario '{username}' ya existe")

    def get_registered_user(self) -> Optional[Dict[str, Any]]:
        """Obtiene el usuario registrado activo (solo debe haber uno)"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, username, face_embedding, created_at FROM users WHERE is_active = 1 LIMIT 1"
        )
        row = cursor.fetchone()
        if row:
            return {
                'id': row['id'],
                'username': row['username'],
                'face_embedding': row['face_embedding'],
                'created_at': row['created_at']
            }
        return None

    def update_last_login(self, user_id: int):
        """Actualiza el último login del usuario"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
            (user_id,)
        )
        self.conn.commit()

    def save_configuration(self, user_id: int, config_key: str, config_value: Any):
        """Guarda o actualiza una configuración del usuario"""
        cursor = self.conn.cursor()
        value_str = json.dumps(config_value)
        cursor.execute("""
            INSERT INTO configurations (user_id, config_key, config_value, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, config_key) DO UPDATE SET
                config_value = excluded.config_value,
                updated_at = CURRENT_TIMESTAMP
        """, (user_id, config_key, value_str))
        self.conn.commit()

    def get_configuration(self, user_id: int, config_key: str, default: Any = None) -> Any:
        """Obtiene una configuración del usuario"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT config_value FROM configurations WHERE user_id = ? AND config_key = ?",
            (user_id, config_key)
        )
        row = cursor.fetchone()
        if row:
            return json.loads(row['config_value'])
        return default

    def get_all_configurations(self, user_id: int) -> Dict[str, Any]:
        """Obtiene todas las configuraciones del usuario"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT config_key, config_value FROM configurations WHERE user_id = ?",
            (user_id,)
        )
        configs = {}
        for row in cursor.fetchall():
            configs[row['config_key']] = json.loads(row['config_value'])
        return configs

    def save_calibration(self, user_id: int, calibration_matrix, samples_src, samples_dst):
        """Guarda una nueva calibración"""
        # Desactivar calibraciones anteriores
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE calibrations SET is_active = 0 WHERE user_id = ?",
            (user_id,)
        )

        # Guardar nueva calibración
        cursor.execute("""
            INSERT INTO calibrations (user_id, calibration_matrix, samples_src, samples_dst)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            pickle.dumps(calibration_matrix),
            pickle.dumps(samples_src),
            pickle.dumps(samples_dst)
        ))
        self.conn.commit()

    def get_active_calibration(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene la calibración activa del usuario"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT calibration_matrix, samples_src, samples_dst, created_at
            FROM calibrations
            WHERE user_id = ? AND is_active = 1
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                'calibration_matrix': pickle.loads(row['calibration_matrix']),
                'samples_src': pickle.loads(row['samples_src']),
                'samples_dst': pickle.loads(row['samples_dst']),
                'created_at': row['created_at']
            }
        return None

    def start_session(self, user_id: int) -> int:
        """Inicia una nueva sesión"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (user_id) VALUES (?)",
            (user_id,)
        )
        self.conn.commit()
        return cursor.lastrowid

    def end_session(self, session_id: int):
        """Finaliza una sesión"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE sessions
            SET end_time = CURRENT_TIMESTAMP,
                duration_seconds = (julianday(CURRENT_TIMESTAMP) - julianday(start_time)) * 86400
            WHERE id = ?
        """, (session_id,))
        self.conn.commit()

    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Obtiene estadísticas del usuario"""
        cursor = self.conn.cursor()

        # Total de sesiones
        cursor.execute(
            "SELECT COUNT(*) as total_sessions FROM sessions WHERE user_id = ?",
            (user_id,)
        )
        total_sessions = cursor.fetchone()['total_sessions']

        # Tiempo total de uso
        cursor.execute(
            "SELECT SUM(duration_seconds) as total_time FROM sessions WHERE user_id = ?",
            (user_id,)
        )
        total_time = cursor.fetchone()['total_time'] or 0

        # Total de calibraciones
        cursor.execute(
            "SELECT COUNT(*) as total_calibrations FROM calibrations WHERE user_id = ?",
            (user_id,)
        )
        total_calibrations = cursor.fetchone()['total_calibrations']

        return {
            'total_sessions': total_sessions,
            'total_time_seconds': total_time,
            'total_calibrations': total_calibrations
        }

    def delete_user(self, user_id: int):
        """Elimina un usuario y todos sus datos"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM calibrations WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM configurations WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()

    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.conn:
            self.conn.close()
