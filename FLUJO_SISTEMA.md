# Flujo del Sistema - Gaze Control v2.0

## Arquitectura General

El sistema sigue una arquitectura modular con separación clara de responsabilidades:

```
main.py (Punto de entrada)
    ↓
GazeControlApp (Controlador principal)
    ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   Autenticación │   Seguimiento   │   Interfaz      │
│                 │                 │                 │
│ UserManager     │ GazeTracker     │ MainWindow      │
│ FaceAuth        │ FaceDetector    │                 │
│ DatabaseManager │ MouseController │                 │
└─────────────────┴─────────────────┴─────────────────┘
```

## Flujo de Ejecución

### 1. Inicialización del Sistema

**Archivo:** `main.py` - Clase `GazeControlApp.__init__()`

```python
# Secuencia de inicialización:
1. Configuración de logging
2. Carga de configuración (Config)
3. Inicialización de base de datos (DatabaseManager)
4. Setup de autenticación (UserManager)
5. Inicialización de componentes principales:
   - GazeTracker (seguimiento de mirada)
   - MouseController (control de mouse)
   - MainWindow (interfaz visual)
6. Configuración de cámara
```

### 2. Registro de Usuario

**Archivo:** `main.py` - Método `register_user_if_needed()`

```python
# Flujo de registro:
1. Verificar si ya existe usuario registrado
2. Si no existe:
   - Solicitar nombre de usuario
   - Capturar 10 muestras faciales
   - Extraer embeddings faciales
   - Guardar en base de datos
3. Retornar estado del registro
```

### 3. Autenticación Facial

**Archivo:** `src/auth/face_auth.py` - Clase `FaceAuthenticator`

```python
# Proceso de autenticación:
1. Detección facial con MediaPipe
2. Extracción de características faciales (embeddings)
3. Comparación con embeddings almacenados
4. Cálculo de similitud (cosine similarity)
5. Retornar autenticación + score de confianza
```

### 4. Seguimiento de Mirada

**Archivo:** `src/core/gaze_tracker.py` - Clase `GazeTracker`

```python
# Pipeline de seguimiento:
1. Detección facial (FaceDetector)
2. Localización de puntos faciales (468 landmarks)
3. Extracción de coordenadas de iris:
   - Ojo izquierdo: landmark 468
   - Ojo derecho: landmark 473
4. Cálculo de punto central de mirada
5. Aplicación de filtros:
   - Filtro One-Euro (suavizado)
   - Deadzone (zona muerta)
6. Mapeo a coordenadas de pantalla
7. Aplicación de calibración (transformación afín)
```

### 5. Detección de Gestos

**Archivo:** `src/core/gaze_tracker.py` - Método `detect_gestures()`

```python
# Gestos oculares implementados:
1. Cálculo de EAR (Eye Aspect Ratio) para cada ojo
2. Detección de guiños:
   - Umbral: EAR < 0.20
   - Frames mínimos: 2
3. Clasificación de gestos:
   - Guiño izquierdo corto → Click izquierdo
   - Guiño izquierdo sostenido → Click derecho
   - Doble guiño izquierdo → Navegación adelante
   - Guiño derecho → Navegación atrás
```

### 6. Control de Mouse

**Archivo:** `src/core/mouse_controller.py` - Clase `MouseController`

```python
# Funcionalidades de control:
1. Movimiento del cursor:
   - Mapeo de coordenadas de mirada a pantalla
   - Aplicación de ganancia (sensibilidad)
   - Suavizado de movimiento

2. Acciones de mouse:
   - Click izquierdo/derecho
   - Dwell click (click por fijación)
   - Auto-scroll (bandas superior/inferior)
   - Navegación de pestañas (gestos combinados)
```

### 7. Calibración del Sistema

**Archivo:** `src/core/calibration.py` - Clase `Calibration`

```python
# Proceso de calibración:
1. Generación de rejilla de puntos (3x3)
2. Captura de muestras:
   - Usuario mira cada punto objetivo
   - Sistema registra (mirada → pantalla)
3. Cálculo de transformación afín:
   - Mínimos cuadrados para encontrar matriz
   - Mapeo óptimo de coordenadas
4. Validación y almacenamiento
```

### 8. Interfaz de Usuario

**Archivo:** `src/ui/main_window.py` - Clase `MainWindow`

```python
# Componentes visuales:
1. HUD (Heads-Up Display):
   - FPS en tiempo real
   - Configuración actual
   - Estado de autenticación
   - Instrucciones de control

2. Modo de calibración:
   - Objetivos visuales
   - Barra de progreso
   - Feedback en tiempo real

3. Notificaciones y advertencias:
   - Mensajes de estado
   - Alertas de seguridad
```

## Flujo de Datos

```
Cámara (Frame BGR)
    ↓
MediaPipe FaceMesh (468 landmarks)
    ↓
Extracción de coordenadas de iris
    ↓
Filtrado (One-Euro + Deadzone)
    ↓
Calibración (Transformación afín)
    ↓
Coordenadas de pantalla
    ↓
PyAutoGUI (Control de mouse)
```

## Algoritmos Clave

### 1. Filtro One-Euro
```python
# Suavizado adaptativo que reduce jitter
# pero preserva movimientos rápidos
x_filtrado = alpha * x_actual + (1 - alpha) * x_anterior
alpha = f(cutoff_frecuencia, velocidad)
```

### 2. Eye Aspect Ratio (EAR)
```python
# Métrica para detección de guiños
EAR = (distancia_vertical_1 + distancia_vertical_2) / (2 * distancia_horizontal)
```

### 3. Transformación Afín
```python
# Mapeo de coordenadas de mirada a pantalla
[screen_x]   [a11 a12 a13]   [gaze_x]
[screen_y] = [a21 a22 a23] × [gaze_y]
[    1    ]   [ 0   0   1 ]   [   1   ]
```

## Características de Seguridad

### 1. Autenticación Continua
- Verificación facial periódica (cada 5 segundos)
- Bloqueo automático si usuario no reconocido
- Cifrado de datos faciales en base de datos

### 2. Validación de Gestos
- Múltiples frames para evitar falsos positivos
- Umbrales adaptativos basados en usuario
- Timeout para gestos sostenidos

### 3. Protección de Datos
- Almacenamiento seguro de embeddings faciales
- Configuraciones personalizadas por usuario
- Logs de actividad y sesiones

## Optimizaciones de Rendimiento

### 1. Procesamiento en Tiempo Real
- Resolución de cámara optimizada (640x480)
- FPS objetivo: 30-60 fps
- Procesamiento asíncrono donde es posible

### 2. Gestión de Memoria
- Limpieza de frames no utilizados
- Cache de configuraciones
- Pool de objetos para cálculos repetitivos

### 3. Filtrado Eficiente
- Filtros con complejidad O(1)
- Actualización incremental de estado
- Parámetros adaptativos en tiempo real

## Arquitectura Modular

El sistema está diseñado con principios SOLID:

- **Single Responsibility**: Cada clase tiene una responsabilidad única
- **Open/Closed**: Extensible sin modificación del código existente
- **Liskov Substitution**: Las interfaces pueden ser intercambiadas
- **Interface Segregation**: Interfaces específicas y cohesivas
- **Dependency Inversion**: Dependencias abstraídas

Esta arquitectura permite fácil mantenimiento, testing y extensión del sistema.