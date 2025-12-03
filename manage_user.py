"""
Script de utilidad para gestionar usuarios - Multi-usuario
"""
import sys
import cv2 as cv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.database.db_manager import DatabaseManager
from src.auth.user_manager import UserManager


def list_users(db: DatabaseManager):
    """Lista todos los usuarios"""
    users = db.get_all_users()
    
    if not users:
        print("\nNo hay usuarios registrados en el sistema")
        return
    
    print("\n" + "=" * 60)
    print("USUARIOS REGISTRADOS")
    print("=" * 60)
    
    for user in users:
        print(f"\nID: {user['id']}")
        print(f"Username: {user['username']}")
        print(f"Registrado: {user['created_at']}")
        print(f"Último login: {user['last_login'] or 'Nunca'}")
        
        # Obtener estadísticas
        stats = db.get_user_stats(user['id'])
        print(f"Estadísticas:")
        print(f"  - Sesiones: {stats['total_sessions']}")
        print(f"  - Tiempo total: {stats['total_time_seconds']:.1f}s")
        print(f"  - Calibraciones: {stats['total_calibrations']}")
        print("-" * 60)


def view_user_configs(db: DatabaseManager, user_id: int):
    """Muestra las configuraciones de un usuario"""
    configs = db.get_all_configurations(user_id)
    
    print("\nConfiguraciones guardadas:")
    if configs:
        for key, value in configs.items():
            print(f"  - {key}: {value}")
    else:
        print("  (No hay configuraciones guardadas)")


def add_new_user(db: DatabaseManager, user_manager: UserManager):
    """Registra un nuevo usuario"""
    print("\n" + "=" * 60)
    print("REGISTRAR NUEVO USUARIO")
    print("=" * 60)
    
    username = input("Ingresa el nombre del nuevo usuario: ").strip()
    if not username:
        print("✗ El nombre de usuario no puede estar vacío")
        return
    
    # Verificar si el nombre ya existe
    existing_users = db.get_all_users()
    if any(u['username'] == username for u in existing_users):
        print(f"✗ Ya existe un usuario con el nombre '{username}'")
        return
    
    print(f"\nRegistrando usuario: {username}")
    print("Se capturarán 10 muestras de su rostro.")
    print("Presiona ENTER para iniciar la cámara...")
    input()
    
    # Inicializar cámara
    camera = cv.VideoCapture(0, cv.CAP_DSHOW)
    if not camera.isOpened():
        print("✗ Error: No se pudo abrir la cámara")
        return
    
    try:
        success = user_manager.register_new_user(username, camera, num_samples=10)
        
        if success:
            print(f"\n✓ Usuario '{username}' registrado exitosamente!")
        else:
            print("\n✗ Error en el registro del usuario")
    finally:
        camera.release()
        cv.destroyAllWindows()


def delete_user(db: DatabaseManager):
    """Elimina un usuario"""
    users = db.get_all_users()
    
    if not users:
        print("\nNo hay usuarios para eliminar")
        return
    
    print("\n" + "=" * 60)
    print("ELIMINAR USUARIO")
    print("=" * 60)
    
    for i, user in enumerate(users, 1):
        print(f"{i}. {user['username']} (ID: {user['id']})")
    
    try:
        choice = input("\nSelecciona el número del usuario a eliminar: ").strip()
        idx = int(choice) - 1
        
        if 0 <= idx < len(users):
            user = users[idx]
            confirm = input(f"\n¿Estás SEGURO de eliminar '{user['username']}'? (si/no): ").strip().lower()
            
            if confirm in ['si', 'sí', 's', 'yes', 'y']:
                db.delete_user(user['id'])
                print(f"\n✓ Usuario '{user['username']}' eliminado correctamente")
            else:
                print("\nOperación cancelada")
        else:
            print("✗ Opción inválida")
    except (ValueError, IndexError):
        print("✗ Entrada inválida")


def main():
    db = DatabaseManager()
    user_manager = UserManager(db)

    while True:
        print("\n" + "=" * 60)
        print("GESTOR DE USUARIOS - Gaze Control v2.0")
        print("=" * 60)
        print("\nOpciones:")
        print("1. Listar usuarios")
        print("2. Registrar nuevo usuario")
        print("3. Ver configuraciones de un usuario")
        print("4. Eliminar usuario")
        print("5. Salir")
        print("=" * 60)

        choice = input("\nSelecciona una opción (1-5): ").strip()

        if choice == "1":
            list_users(db)
        
        elif choice == "2":
            add_new_user(db, user_manager)
        
        elif choice == "3":
            users = db.get_all_users()
            if not users:
                print("\nNo hay usuarios registrados")
                continue
            
            print("\nUsuarios:")
            for i, user in enumerate(users, 1):
                print(f"{i}. {user['username']}")
            
            try:
                user_choice = input("\nSelecciona el número de usuario: ").strip()
                idx = int(user_choice) - 1
                if 0 <= idx < len(users):
                    view_user_configs(db, users[idx]['id'])
                else:
                    print("✗ Opción inválida")
            except (ValueError, IndexError):
                print("✗ Entrada inválida")
        
        elif choice == "4":
            delete_user(db)
        
        elif choice == "5":
            print("\n¡Hasta luego!")
            break
        
        else:
            print("\n✗ Opción inválida")

    db.close()


if __name__ == "__main__":
    main()
