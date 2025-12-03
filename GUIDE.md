# Guía de Usuario - Gaze Control v2.0

## Introducción

Gaze Control es un sistema avanzado de control del cursor mediante seguimiento de la mirada, con autenticación facial y persistencia de configuraciones.

## Características Principales

### Autenticación de Usuario Único
- Al iniciar por primera vez, se registra un usuario único
- El sistema captura 10 muestras faciales para crear un perfil biométrico
- Solo el usuario registrado puede usar el sistema
- Verificación continua de identidad durante el uso

### Sistema de Calibración
- Calibración de 9 puntos para mapeo preciso
- Guardado automático de calibraciones
- Carga automática al iniciar sesión

### Control del Mouse
- Movimiento suave con filtros OneEuro
- Zona muerta configurable para estabilidad
- Sensibilidad ajustable en tiempo real

### Gestos Inteligentes
- **Guiño izquierdo**: Click izquierdo
- **Doble guiño izquierdo**: Avanzar página (navegador)
- **Guiño derecho**: Retroceder página (navegador)
- **Dwell click**: Click por mirada sostenida (opcional)

### Scroll Automático
- Scroll hacia arriba: Mirar zona superior de pantalla
- Scroll hacia abajo: Mirar zona inferior de pantalla

## Instalación

### Requisitos
- Python 3.10+ (recomendado)
- Cámara web
- Windows, macOS o Linux

### Pasos

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

## Primer Uso

### 1. Registro de Usuario

Al ejecutar por primera vez:

```bash
python main.py
```

Se te pedirá:
1. Ingresar un nombre de usuario
2. Mirar a la cámara mientras se capturan 10 muestras faciales
3. Mover ligeramente la cabeza para capturar diferentes ángulos

**Importante**: Solo puedes registrar UN usuario. Para cambiar de usuario, debes eliminar la base de datos en `data/users.db`

### 2. Autenticación

En cada inicio:
1. Mira a la cámara
2. El sistema verificará tu identidad
3. Si la autenticación es exitosa, el sistema se iniciará

### 3. Calibración Inicial

Recomendado realizar calibración la primera vez:
1. Presiona `c` para iniciar calibración
2. Mira fijamente cada círculo amarillo que aparece
3. Mantén la mirada 0.4 segundos en cada punto
4. El sistema calibrará automáticamente

## Controles

### Teclas

| Tecla | Acción |
|-------|--------|
| `c` | Iniciar calibración |
| `r` | Resetear calibración |
| `d` | Activar/desactivar modo debug |
| `+` o `=` | Aumentar sensibilidad |
| `-` | Disminuir sensibilidad |
| `g` | Activar/desactivar dwell click |
| `q` | Salir |

### Gestos con Ojos

| Gesto | Acción |
|-------|--------|
| Guiño izquierdo corto | Click izquierdo |
| Guiño izquierdo SOSTENIDO (~0.5s) | **Click derecho** ⭐ NUEVO |
| Doble guiño izquierdo | Avanzar página |
| Guiño derecho corto | Retroceder página |
| Ojo derecho cerrado + Mover derecha | **Siguiente pestaña** ⭐ NUEVO |
| Ojo derecho cerrado + Mover izquierda | **Pestaña anterior** ⭐ NUEVO |
| Mirada sostenida (con dwell) | Click |

## Configuración Avanzada

### Archivo de Configuración

El archivo `data/config.json` contiene todas las configuraciones:

```json
{
    "gain": 1.20,                    // Sensibilidad del movimiento
    "deadzone": 0.015,               // Zona muerta (0.01-0.05)
    "wink_threshold": 0.20,          // Umbral de guiño (0.15-0.25)
    "dwell_time": 0.70,              // Tiempo para dwell click
    "scroll_band": 0.08,             // Tamaño de banda de scroll
    "camera_index": 0,               // Índice de cámara
    "face_similarity_threshold": 0.85 // Umbral de autenticación
}
```

### Ajuste de Parámetros

**Sensibilidad (gain)**
- Valores: 0.5 - 2.5
- Más alto = más sensible
- Ajustar con `+` / `-`

**Zona Muerta (deadzone)**
- Valores: 0.005 - 0.050
- Más alto = más estable, menos sensible
- Editar en config.json

**Umbral de Guiño (wink_threshold)**
- Valores: 0.15 - 0.30
- Más bajo = más fácil activar guiño
- Editar en config.json

## Base de Datos

El sistema usa SQLite en `data/users.db` para almacenar:

- Perfil biométrico del usuario
- Configuraciones personalizadas
- Calibraciones guardadas
- Historial de sesiones
- Estadísticas de uso

### Resetear Usuario

Para eliminar el usuario y empezar de nuevo:

1. Cierra la aplicación
2. Elimina el archivo `data/users.db`
3. Inicia la aplicación nuevamente

## Logs

Los logs se guardan en `data/logs/` con formato:
- `gaze_control_YYYYMMDD.log`

Útiles para diagnosticar problemas.

## Solución de Problemas

### La cámara no se abre
- Verifica que no esté siendo usada por otra aplicación
- Prueba cambiar `camera_index` en config.json (0, 1, 2...)

### Movimientos muy bruscos
- Reduce la sensibilidad con tecla `-`
- Aumenta `deadzone` en config.json
- Realiza una nueva calibración

### No detecta guiños
- Aumenta `wink_threshold` en config.json
- Asegúrate de tener buena iluminación
- Guiña de forma más pronunciada

### Autenticación falla frecuentemente
- Mejora la iluminación del entorno
- Reduce `face_similarity_threshold` en config.json (con precaución)
- Re-registra el usuario

### El cursor se mueve solo
- Aumenta `deadzone` en config.json
- Verifica que no haya reflejos en tus lentes
- Asegúrate de estar solo frente a la cámara

## Rendimiento

### Requisitos Recomendados
- CPU: Procesador moderno (i5/Ryzen 5 o superior)
- RAM: 4GB mínimo
- Cámara: 720p o superior, 30 FPS
- Iluminación: Buena iluminación frontal

### Optimización
- Cierra aplicaciones en segundo plano
- Usa una cámara de calidad
- Mantén buena iluminación
- Reduce la resolución de cámara si es necesario (en config.json)

## Estructura del Proyecto

```
vision-artificial/
├── main.py                 # Punto de entrada principal
├── gaze_control.py         # Versión legacy (mantener como backup)
├── requirements.txt        # Dependencias
├── GUIDE.md               # Esta guía
├── README.md              # Documentación general
├── src/                   # Código fuente modular
│   ├── auth/             # Autenticación facial
│   ├── core/             # Componentes principales
│   ├── database/         # Gestor de base de datos
│   ├── ui/               # Interfaz de usuario
│   └── utils/            # Utilidades
└── data/                  # Datos de usuario
    ├── users.db          # Base de datos
    ├── config.json       # Configuración
    └── logs/             # Archivos de log
```

## Seguridad y Privacidad

- Los datos biométricos se almacenan **localmente** en tu computadora
- No se envía información a servidores externos
- La base de datos está en formato SQLite sin cifrar
- Para mayor seguridad, puedes cifrar la carpeta `data/`

## Limitaciones Conocidas

- Solo puede haber un usuario registrado a la vez
- Requiere buena iluminación para funcionar correctamente
- No funciona bien con lentes muy reflectivos
- El rendimiento depende de la potencia de la CPU

## Soporte

Para reportar bugs o solicitar características:
- GitHub Issues: [repositorio/issues]
- Email: tu-email@ejemplo.com

## Licencia

MIT License - Ver archivo LICENSE para detalles

---

**Versión**: 2.0.0
**Última actualización**: 2025
**Desarrollado con**: Python, OpenCV, MediaPipe, PyAutoGUI
