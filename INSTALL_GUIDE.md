# 🚀 Guía de Instalación Rápida

## Opción 1: Instalación Automática (Recomendada)

### Windows
```bash
# Haz doble clic en el archivo o ejecuta:
install.bat
```

### macOS/Linux
```bash
# Ejecuta el instalador automático:
python install.py
```

## Opción 2: Instalación Manual

### 1. Requisitos Previos
- **Python 3.7+** (recomendado 3.10+)
- **Cámara web** funcional
- **8GB+ RAM** (para procesamiento de video)

### 2. Instalar Dependencias
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Crear Directorios
```bash
# Windows
mkdir data\data\logs

# macOS/Linux  
mkdir -p data/logs
```

### 4. Verificar Instalación
```bash
python main.py
```

## 📦 Paquetes Instalados

El sistema instala automáticamente:

| Paquete | Versión | Uso |
|---------|---------|-----|
| `numpy` | ≥1.21.0 | Procesamiento numérico |
| `opencv-python` | ≥4.5.0 | Visión por computadora |
| `mediapipe` | ≥0.10.0 | Detección facial y de iris |
| `pyautogui` | ≥0.9.53 | Control del mouse |
| `opencv-contrib-python` | ≥4.5.0 | Funciones adicionales de OpenCV |

## 🔧 Solución de Problemas

### Problema: "Python no encontrado"
**Solución:**
1. Descarga Python desde https://python.org
2. Durante instalación, marca "Add Python to PATH"
3. Reinicia tu terminal

### Problema: "MediaPipe no disponible"
**Solución:**
MediaPipe puede no estar disponible para algunas versiones de Python o arquitecturas. El sistema incluye alternativas:

```bash
# Opción 1: Usar el instalador actualizado (recomendado)
python install.py

# Opción 2: Instalar versión alternativa de MediaPipe
pip install mediapipe>=0.9.0

# Opción 3: Usar modo básico sin MediaPipe
python test_basic.py
```

### Problema: "La cámara no funciona"
**Solución:**
1. Verifica que la cámara no esté en uso por otra app
2. Reinicia tu computadora
3. Prueba con otra aplicación de cámara

### Problema: "Error de permisos" (Windows)
**Solución:**
1. Haz clic derecho en `install.bat`
2. Selecciona "Ejecutar como administrador"

### Problema: "ModuleNotFoundError"
**Solución:**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

## 🔄 Modos de Operación

### Modo Completo (con MediaPipe)
- Detección precisa de iris
- Seguimiento exacto de mirada
- Todos los gestos oculares disponibles
- Requiere: MediaPipe instalado

### Modo Básico (sin MediaPipe)
- Detección facial con OpenCV
- Seguimiento aproximado de mirada
- Gestos básicos (guiños)
- Compatible con más sistemas

**Para usar modo básico:**
```bash
python test_basic.py
```

## 🎯 Iniciar el Sistema

Una vez instalado:

### Método 1: Acceso Directo (Windows)
- Haz doble clic en "Gaze Control" del escritorio

### Método 2: Terminal
```bash
python main.py
```

### Método 3: Gestión de Usuarios
```bash
python manage_user.py
```

## 📋 Verificación de Instalación

El sistema debe mostrar:
```
✅ Python compatible
✅ Dependencias instaladas  
✅ Directorios creados
✅ Cámara verificada
✅ Prueba básica superada
```

## 🆘 Ayuda Adicional

Si tienes problemas:

1. **Revisa la documentación:**
   - `GUIDE.md` - Guía completa
   - `FLUJO_SISTEMA.md` - Documentación técnica
   - `QUICKSTART.md` - Inicio rápido

2. **Verifica los requisitos:**
   - Python 3.7+
   - 8GB+ RAM
   - Cámara web funcional

3. **Contacta soporte** si el problema persiste

---

**¡Listo para usar Gaze Control!** 🎉