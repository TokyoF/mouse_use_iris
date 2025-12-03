"""
Script para migrar bases de datos existentes al nuevo esquema multi-usuario
Agrega la columna is_logged_in a la tabla users si no existe
"""
import sys
import sqlite3
from pathlib import Path

def migrate_database(db_path: str = "data/users.db"):
    """Migra la base de datos al nuevo esquema"""
    db_file = Path(db_path)
    
    if not db_file.exists():
        print(f"✓ Base de datos '{db_path}' no existe. Se creará con el nuevo esquema.")
        return True
    
    print(f"Migrando base de datos: {db_path}")
    
    try:
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'is_logged_in' in columns:
            print("✓ La base de datos ya tiene la columna 'is_logged_in'")
        else:
            print("Agregando columna 'is_logged_in' a la tabla users...")
            cursor.execute("ALTER TABLE users ADD COLUMN is_logged_in INTEGER DEFAULT 0")
            conn.commit()
            print("✓ Columna 'is_logged_in' agregada exitosamente")
        
        # Asegurar que todos los usuarios estén deslogueados
        cursor.execute("UPDATE users SET is_logged_in = 0")
        conn.commit()
        print("✓ Todos los usuarios marcados como deslogueados")
        
        conn.close()
        print("\n✓ Migración completada exitosamente")
        return True
        
    except Exception as e:
        print(f"\n✗ Error durante la migración: {e}")
        return False


def main():
    print("=" * 60)
    print("MIGRACIÓN DE BASE DE DATOS - Gaze Control v2.0")
    print("=" * 60)
    print("\nEste script actualizará tu base de datos al nuevo esquema multi-usuario.")
    print("IMPORTANTE: Se recomienda hacer un respaldo de data/users.db antes de continuar.")
    
    response = input("\n¿Deseas continuar? (si/no): ").strip().lower()
    
    if response not in ['si', 'sí', 's', 'yes', 'y']:
        print("\nMigración cancelada")
        return
    
    success = migrate_database()
    
    if success:
        print("\n" + "=" * 60)
        print("Ahora puedes ejecutar el programa normalmente con:")
        print("  python main.py")
        print("\nO gestionar usuarios con:")
        print("  python manage_user.py")
        print("=" * 60)
    else:
        print("\nPor favor, verifica los errores y vuelve a intentar.")
        sys.exit(1)


if __name__ == "__main__":
    main()
