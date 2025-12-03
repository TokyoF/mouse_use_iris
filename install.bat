@echo off
REM Instalador Rápido - Gaze Control v2.0
REM Este script instala todas las dependencias automáticamente

echo ====================================================
echo 🎯 GAZE CONTROL v2.0 - INSTALADOR RÁPIDO
echo ====================================================
echo.
echo Este script instalará automáticamente todo lo necesario
echo para ejecutar el sistema de control por mirada.
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo    Por favor, instala Python 3.7+ desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
python --version

REM Actualizar pip
echo.
echo 🔄 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo.
echo 📦 Instalando dependencias...
echo ====================================================

python -m pip install numpy>=1.21.0
if errorlevel 1 goto :error

python -m pip install opencv-python>=4.5.0
if errorlevel 1 goto :error

python -m pip install mediapipe>=0.10.0
if errorlevel 1 (
    echo ⚠️ MediaPipe 0.10.0 no disponible, intentando versión alternativa...
    python -m pip install mediapipe>=0.9.0
    if errorlevel 1 (
        echo ⚠️ MediaPipe no disponible - sistema funcionará con detección básica
    )
)

python -m pip install pyautogui>=0.9.53
if errorlevel 1 goto :error

python -m pip install opencv-contrib-python>=4.5.0
if errorlevel 1 goto :error

echo ====================================================
echo ✅ Todas las dependencias instaladas

REM Crear directorios
echo.
echo 📁 Creando estructura de directorios...
if not exist "data" mkdir data
if not exist "data\logs" mkdir data\logs
if not exist "data\config" mkdir data\config
if not exist "data\calibrations" mkdir data\calibrations
echo ✅ Directorios creados

REM Verificar instalación
echo.
echo 🔍 Verificando instalación...
python -c "import numpy, cv2, mediapipe, pyautogui; print('✅ Todos los módulos importados correctamente')"
if errorlevel 1 goto :error

REM Crear acceso directo
echo.
echo 🖥️ Creando acceso directo...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Gaze Control.lnk'); $Shortcut.Target = 'python'; $Shortcut.Arguments = '%cd%\main.py'; $Shortcut.WorkingDirectory = '%cd%'; $Shortcut.Save()"
echo ✅ Acceso directo creado en el escritorio

echo.
echo ====================================================
echo 🎉 ¡INSTALACIÓN COMPLETADA CON ÉXITO!
echo ====================================================
echo.
echo Para iniciar la aplicación:
echo    python main.py
echo.
echo O haz doble clic en el acceso directo "Gaze Control"
echo que se ha creado en tu escritorio.
echo.
echo Para gestionar usuarios:
echo    python manage_user.py
echo.
echo ====================================================
pause
exit /b 0

:error
echo.
echo ❌ Error durante la instalación
echo    Por favor, revisa los mensajes de error arriba
echo    e intenta ejecutar como administrador.
echo.
echo Si el problema persiste, intenta instalar manualmente:
echo    python -m pip install -r requirements.txt
echo.
pause
exit /b 1