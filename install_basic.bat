@echo off
REM Instalación Rápida de Dependencias Básicas
echo ====================================================
echo 🚀 INSTALACIÓN RÁPIDA - DEPENDENCIAS BÁSICAS
echo ====================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado
    pause
    exit /b 1
)

echo ✅ Python detectado
python --version

REM Actualizar pip
echo.
echo 🔄 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias básicas una por una
echo.
echo 📦 Instalando dependencias básicas...

echo Instalando numpy...
python -m pip install numpy
if errorlevel 1 (
    echo ❌ Error instalando numpy
    pause
    exit /b 1
)

echo Instalando opencv-python...
python -m pip install opencv-python
if errorlevel 1 (
    echo ❌ Error instalando opencv-python
    pause
    exit /b 1
)

echo Instalando pyautogui...
python -m pip install pyautogui
if errorlevel 1 (
    echo ❌ Error instalando pyautogui
    pause
    exit /b 1
)

echo.
echo ✅ Todas las dependencias básicas instaladas

REM Verificar instalación
echo.
echo 🔍 Verificando instalación...
python -c "import numpy, cv2, pyautogui; print('✅ Todas las dependencias funcionan correctamente')"
if errorlevel 1 (
    echo ❌ Error en verificación
    pause
    exit /b 1
)

echo.
echo ====================================================
echo 🎉 ¡INSTALACIÓN BÁSICA COMPLETADA!
echo ====================================================
echo.
echo Ahora puedes ejecutar:
echo    python test_basic.py
echo.
echo Para el sistema completo, intenta:
echo    python install.py
echo ====================================================
pause