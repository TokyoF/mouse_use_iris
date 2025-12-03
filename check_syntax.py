"""
Verificador de sintaxis Python
Compila todos los archivos .py para detectar errores de sintaxis
"""
import py_compile
import sys
from pathlib import Path


def check_file(filepath):
    """Verifica la sintaxis de un archivo Python"""
    try:
        py_compile.compile(str(filepath), doraise=True)
        return True, None
    except py_compile.PyCompileError as e:
        return False, str(e)


def main():
    """Función principal"""
    print("=" * 60)
    print("VERIFICACIÓN DE SINTAXIS PYTHON")
    print("=" * 60)

    # Buscar todos los archivos .py
    root = Path(__file__).parent
    python_files = []

    # Archivos principales
    for file in root.glob("*.py"):
        if file.name not in ["check_syntax.py"]:  # Excluir este script
            python_files.append(file)

    # Archivos en src/
    for file in root.glob("src/**/*.py"):
        python_files.append(file)

    errors = []
    success_count = 0

    for filepath in sorted(python_files):
        relative_path = filepath.relative_to(root)
        success, error = check_file(filepath)

        if success:
            print(f"OK   {relative_path}")
            success_count += 1
        else:
            print(f"FAIL {relative_path}")
            errors.append((relative_path, error))

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"Archivos verificados: {len(python_files)}")
    print(f"Sin errores: {success_count}")
    print(f"Con errores: {len(errors)}")

    if errors:
        print("\nERRORES ENCONTRADOS:")
        for path, error in errors:
            print(f"\n{path}:")
            print(f"  {error}")
        return 1
    else:
        print("\nTODOS LOS ARCHIVOS TIENEN SINTAXIS CORRECTA")
        return 0


if __name__ == "__main__":
    sys.exit(main())
