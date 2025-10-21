# Vision Artificial - Control por Mirada

Sistema de control del cursor del mouse mediante el seguimiento de la mirada usando visión por computadora y MediaPipe.

## 📋 Descripción

Este proyecto implementa tres scripts para controlar el mouse de tu computadora usando la cámara web y seguimiento ocular:

- **`gaze_control.py`**: Sistema completo de control por mirada con calibración, filtrado OneEuro, gestos por guiños y scroll automático
- **`mouse_iris_min.py`**: Versión minimalista del control de mouse por seguimiento de iris
- **`test_iris.py`**: Script de prueba para verificar la detección de iris

## ✨ Características

### gaze_control.py
- ✅ Filtro OneEuro para suavizado de movimientos
- ✅ Sistema de calibración de 9 puntos
- ✅ Gestos por guiños de ojos:
  - Guiño izquierdo: Click izquierdo
  - Doble guiño izquierdo: Avanzar página
  - Guiño derecho: Retroceder página
- ✅ Scroll automático por zonas (superior/inferior de pantalla)
- ✅ Dwell click (click por mirada sostenida - opcional)
- ✅ Zona muerta (deadzone) para evitar micro-movimientos
- ✅ Ajuste de sensibilidad en tiempo real

### mouse_iris_min.py
- ✅ Control básico del mouse
- ✅ Filtro EMA (Exponential Moving Average)
- ✅ Mínimo código, fácil de entender

### test_iris.py
- ✅ Visualización de puntos de iris
- ✅ Indicador de FPS
- ✅ Prueba de detección de landmarks

## 🛠️ Requisitos

- Python 3.7+
- Cámara web
- Windows (probado), macOS o Linux

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/vision-artificial.git
cd vision-artificial
```

2. Crea un entorno virtual:
```bash
python -m venv .venv
```

3. Activa el entorno virtual:
- Windows:
```bash
.venv\Scripts\activate
```
- macOS/Linux:
```bash
source .venv/bin/activate
```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Test de detección de iris
```bash
python test_iris.py
```
Verifica que tu cámara detecta correctamente los puntos del iris.

### Control básico del mouse
```bash
python mouse_iris_min.py
```
Mueve la mirada para controlar el cursor.

### Control completo con gestos
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

El sistema utiliza MediaPipe Face Mesh para detectar 478 landmarks faciales, incluyendo los centros de los iris (puntos 468 y 473). El proceso es:

1. **Captura**: Lee frames de la cámara web
2. **Detección**: MediaPipe detecta los landmarks faciales
3. **Filtrado**: Aplica filtro OneEuro para suavizar movimientos
4. **Mapeo**: Convierte coordenadas de iris a coordenadas de pantalla
5. **Calibración**: Sistema afín 2D para mapeo personalizado
6. **Gestos**: Detecta guiños mediante EAR (Eye Aspect Ratio)

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

## 👤 Autor

Tu nombre - [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- [MediaPipe](https://google.github.io/mediapipe/) por la detección facial
- [OpenCV](https://opencv.org/) por el procesamiento de video
- [PyAutoGUI](https://pyautogui.readthedocs.io/) por el control del mouse
