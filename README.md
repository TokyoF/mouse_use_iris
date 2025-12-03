# Vision Artificial - Control por Mirada v2.0

Sistema avanzado de control del cursor mediante seguimiento de la mirada con **autenticación facial**, arquitectura modular y persistencia de datos.

## 🎯 Descripción

Sistema profesional de control por mirada que incluye:

- **Autenticación facial biométrica**: Solo el usuario registrado puede usar el sistema
- **Base de datos SQLite**: Persistencia de usuarios, configuraciones y calibraciones
- **Arquitectura modular**: Código organizado, mantenible y escalable
- **Sistema de logging**: Diagnóstico completo de eventos y errores
- **Configuración persistente**: Tus ajustes se guardan automáticamente

## 📂 Versiones Disponibles

- **`main.py`**: Nueva versión 2.0 con autenticación y arquitectura modular (RECOMENDADO)
- **`gaze_control.py`**: Versión legacy sin autenticación (para referencia)
- **`mouse_iris_min.py`**: Versión minimalista de prueba
- **`test_iris.py`**: Script de verificación de detección de iris

## ✨ Características Principales (v2.0)

### 🔐 Autenticación y Seguridad
- ✅ Registro de usuario único con captura de múltiples muestras faciales
- ✅ Autenticación biométrica continua durante el uso
- ✅ Base de datos SQLite local para almacenar perfiles
- ✅ Rechazo automático de usuarios no autorizados

### 🎮 Control por Mirada
- ✅ Filtro OneEuro adaptativo para movimientos suaves
- ✅ Sistema de calibración de 9 puntos con persistencia
- ✅ Zona muerta configurable para estabilidad
- ✅ Sensibilidad ajustable en tiempo real
- ✅ Scroll automático por zonas de pantalla

### 👁️ Gestos Inteligentes
- ✅ Guiño izquierdo corto → Click izquierdo
- ✅ Guiño izquierdo SOSTENIDO (~0.5s) → **Click derecho** (NUEVO)
- ✅ Doble guiño izquierdo → Avanzar página
- ✅ Guiño derecho corto → Retroceder página
- ✅ Ojo derecho cerrado + Mover derecha → **Siguiente pestaña** (NUEVO)
- ✅ Ojo derecho cerrado + Mover izquierda → **Pestaña anterior** (NUEVO)
- ✅ Dwell click → Click por mirada sostenida (opcional)

### 🗂️ Sistema Modular
- ✅ Arquitectura de código organizada y mantenible
- ✅ Sistema de logging completo con archivos diarios
- ✅ Manejo robusto de errores
- ✅ Configuración JSON persistente
- ✅ Separación de responsabilidades (MVC-like)

### 📊 Persistencia de Datos
- ✅ Historial de sesiones de usuario
- ✅ Estadísticas de uso
- ✅ Calibraciones guardadas automáticamente
- ✅ Configuraciones personalizadas por usuario

## 🛠️ Requisitos

- **Python 3.10** (recomendado) o Python 3.7+
- Cámara web
- Windows (probado), macOS o Linux

## 📦 Instalación

> **⚠️ Importante**: Se recomienda usar **Python 3.10** para mejor compatibilidad con MediaPipe y todas las dependencias.

1. Verifica tu versión de Python:
```bash
python --version
```
Si no tienes Python 3.10, descárgalo desde [python.org](https://www.python.org/downloads/)

2. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/vision-artificial.git
cd vision-artificial
```

3. Crea un entorno virtual:
```bash
python -m venv .venv
```

4. Activa el entorno virtual:
- Windows:
```bash
.venv\Scripts\activate
```
- macOS/Linux:
```bash
source .venv/bin/activate
```

5. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Versión 2.0 con Autenticación (RECOMENDADA)

```bash
python main.py
```

**Primera vez:**
1. Ingresa tu nombre de usuario
2. Mira a la cámara para registrar tu rostro (10 muestras)
3. Autentícate mirando a la cámara
4. Realiza la calibración presionando `c`

**Siguientes usos:**
1. Autentica mirando a la cámara
2. El sistema carga automáticamente tu calibración y configuraciones
3. ¡Listo para usar!

### Versión Legacy (sin autenticación)

```bash
python gaze_control.py
```

#### Controles:
- `c`: Iniciar calibración de 9 puntos
- `r`: Resetear calibración
- `d`: Activar/desactivar modo debug
- `+/-`: Ajustar sensibilidad (GAIN)
- `g`: Activar/desactivar dwell click
- `q`: Salir

#### Proceso de calibración:
1. Presiona `c` para iniciar
2. Mira fijamente cada uno de los 9 círculos amarillos que aparecen
3. Mantén la mirada durante 0.4 segundos en cada punto
4. El sistema se calibrará automáticamente

## ⚙️ Configuración

Puedes ajustar los parámetros en `gaze_control.py`:

```python
GAIN = 1.20              # Sensibilidad del movimiento
DEADZONE = 0.015         # Zona muerta para micro-movimientos
WINK_THRESH = 0.20       # Umbral de detección de guiño
DWELL_TIME = 0.70        # Tiempo para dwell click (segundos)
SCROLL_BAND = 0.08       # Tamaño de banda de scroll
SCROLL_STEP = 80         # Velocidad de scroll
```

## 🎯 Cómo funciona

### Pipeline de Procesamiento (v2.0)

1. **Autenticación Inicial**
   - Captura embedding facial del usuario
   - Almacena en base de datos SQLite
   - Verifica identidad usando similitud coseno

2. **Detección Facial** (MediaPipe Face Mesh)
   - 478 landmarks faciales
   - Centros de iris (puntos 468 y 473)
   - Eye Aspect Ratio para gestos

3. **Filtrado y Suavizado**
   - Filtro OneEuro adaptativo
   - Zona muerta configurable
   - Reducción de jitter

4. **Calibración Personalizada**
   - Transformación afín 2D
   - 9 puntos de calibración
   - Guardado automático por usuario

5. **Control del Mouse**
   - Mapeo gaze-to-screen
   - Gestos mediante guiños
   - Dwell click opcional
   - Scroll automático

6. **Verificación Continua**
   - Re-autenticación cada 2 segundos
   - Bloqueo si usuario no reconocido

## 🔧 Solución de problemas

### La cámara no se abre
- Verifica que no haya otras aplicaciones usando la cámara
- Prueba cambiar `cv.CAP_DSHOW` por `0` en el código

### Movimientos muy bruscos
- Aumenta la zona muerta (DEADZONE)
- Ajusta los parámetros del filtro OneEuro
- Realiza la calibración

### No detecta guiños
- Ajusta WINK_THRESH (valores más altos = más sensible)
- Asegúrate de tener buena iluminación

## 📝 Licencia

MIT License - Ver archivo LICENSE para más detalles

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📖 Documentación Adicional

Para una guía detallada de uso, consulta [GUIDE.md](GUIDE.md)

## 🏗️ Arquitectura del Proyecto

```
vision-artificial/
├── main.py                     # Punto de entrada v2.0
├── gaze_control.py             # Versión legacy
├── src/
│   ├── auth/                   # Autenticación facial
│   │   ├── face_auth.py        # Detector y verificador facial
│   │   └── user_manager.py     # Gestor de usuarios
│   ├── core/                   # Componentes principales
│   │   ├── filters.py          # Filtros OneEuro y EMA
│   │   ├── face_detector.py    # Detector MediaPipe
│   │   ├── gaze_tracker.py     # Seguimiento de mirada
│   │   ├── mouse_controller.py # Control del mouse
│   │   └── calibration.py      # Sistema de calibración
│   ├── database/               # Persistencia
│   │   └── db_manager.py       # Gestor SQLite
│   ├── ui/                     # Interfaz de usuario
│   │   └── main_window.py      # Ventana principal
│   └── utils/                  # Utilidades
│       ├── logger.py           # Sistema de logs
│       ├── config.py           # Configuración
│       └── error_handler.py    # Manejo de errores
└── data/                       # Datos generados
    ├── users.db                # Base de datos
    ├── config.json             # Configuración
    └── logs/                   # Archivos de log
```

## 🔄 Migración desde v1.0

Si usabas `gaze_control.py`:

1. La versión legacy sigue funcionando
2. Para usar v2.0, ejecuta `python main.py`
3. Registra tu usuario la primera vez
4. Tus configuraciones anteriores en `gaze_control.py` se pueden aplicar manualmente en `data/config.json`

## 👤 Autor

Desarrollado como proyecto de Inteligencia Artificial

## 🙏 Agradecimientos

- [MediaPipe](https://google.github.io/mediapipe/) por la detección facial
- [OpenCV](https://opencv.org/) por el procesamiento de video
- [PyAutoGUI](https://pyautogui.readthedocs.io/) por el control del mouse
