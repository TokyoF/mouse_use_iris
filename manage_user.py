"""
Script de utilidad para gestionar usuarios
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.database.db_manager import DatabaseManager


def main():
    db = DatabaseManager()

    print("=" * 60)
    print("GESTOR DE USUARIOS - Gaze Control v2.0")
    print("=" * 60)

    # Verificar usuario actual
    user = db.get_registered_user()

    if user:
        print(f"\nUsuario registrado: {user['username']}")
        print(f"ID: {user['id']}")
        print(f"Registrado: {user['created_at']}")

        # Obtener estadísticas
        stats = db.get_user_stats(user['id'])
        print(f"\nEstadísticas:")
        print(f"  - Sesiones totales: {stats['total_sessions']}")
        print(f"  - Tiempo total: {stats['total_time_seconds']:.1f} segundos")
        print(f"  - Calibraciones: {stats['total_calibrations']}")

        # Opciones
        print("\n" + "=" * 60)
        print("Opciones:")
        print("1. Ver configuraciones")
        print("2. Eliminar usuario (CUIDADO: no se puede deshacer)")
        print("3. Salir")

        choice = input("\nSelecciona una opción (1-3): ").strip()

        if choice == "1":
            configs = db.get_all_configurations(user['id'])
            print("\nConfiguraciones guardadas:")
            if configs:
                for key, value in configs.items():
                    print(f"  - {key}: {value}")
            else:
                print("  (No hay configuraciones guardadas)")

        elif choice == "2":
            confirm = input(f"\n¿Estás seguro de eliminar el usuario '{user['username']}'? (si/no): ").strip().lower()
            if confirm in ['si', 'sí', 's', 'yes', 'y']:
                db.delete_user(user['id'])
                print(f"\n✓ Usuario '{user['username']}' eliminado correctamente")
            else:
                print("\nOperación cancelada")

    else:
        print("\nNo hay usuario registrado en el sistema")
        print("Ejecuta 'python main.py' para registrar un usuario")

    db.close()
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
