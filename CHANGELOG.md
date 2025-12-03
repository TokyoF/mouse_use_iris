# Changelog - Vision Artificial Gaze Control

## [2.1.0] - 2025 (Gestos Avanzados)

### ⭐ Nuevas Características

**Gestos Avanzados Implementados**
- Click derecho con guiño izquierdo sostenido (~0.5s)
- Navegación entre pestañas con ojo derecho cerrado + movimiento horizontal
  - Mover derecha = Siguiente pestaña (Ctrl+Tab)
  - Mover izquierda = Pestaña anterior (Ctrl+Shift+Tab)
- Detección inteligente de duración de guiños
- Sistema de seguimiento de posición horizontal durante gestos

**Mejoras Técnicas**
- Nuevo parámetro `gaze_x` en `process_gestures()`
- Variables de estado para tracking de ojos cerrados
- Umbral configurable para cambio de pestañas (`tab_switch_threshold`)
- Tiempo configurable para click derecho (`right_click_hold_time`)

**Actualizaciones de UI**
- Instrucciones ampliadas en pantalla
- Mensajes informativos de gestos en consola
- Documentación actualizada (README, GUIDE, QUICKSTART)

---

## [2.0.0] - 2025

### 🎉 Nueva Versión Completa con Autenticación

#### Características Añadidas

**Sistema de Autenticación**
- Registro de usuario único con captura biométrica facial
- Autenticación continua durante el uso
- Verificación cada 2 segundos para seguridad
- Rechazo automático de usuarios no autorizados
- Embedding facial usando landmarks de MediaPipe

**Base de Datos SQLite**
- Almacenamiento de perfiles de usuario
- Persistencia de configuraciones personalizadas
- Historial de sesiones con timestamps
- Guardado automático de calibraciones
- Estadísticas de uso por usuario

**Arquitectura Modular**
- Separación en módulos: auth, core, database, ui, utils
- Código organizado según responsabilidades
- Fácil mantenimiento y extensibilidad
- Estructura MVC-like

**Sistema de Logging**
- Logs diarios en `data/logs/`
- Niveles: DEBUG, INFO, WARNING, ERROR
- Rotación automática de archivos
- Logs tanto en consola como en archivo

**Configuración Persistente**
- Archivo JSON para configuraciones globales
- Configuraciones por usuario en base de datos
- Carga automática al login
- Guardado automático al cerrar

**Mejoras en UI**
- HUD mejorado con información en tiempo real
- Indicador de autenticación visual
- Barra de progreso en calibración
- Mensajes de advertencia y notificaciones
- Contador de FPS suavizado

**Manejo Robusto de Errores**
- ErrorHandler centralizado
- Try-catch en operaciones críticas
- Logging detallado de errores
- Recuperación graceful

#### Módulos Creados

**src/auth/**
- `face_auth.py`: Autenticación facial con embeddings
- `user_manager.py`: Gestión de usuarios y sesiones

**src/core/**
- `filters.py`: Filtros OneEuro, EMA y DeadzoneFilter
- `face_detector.py`: Detector MediaPipe optimizado
- `gaze_tracker.py`: Seguimiento de mirada completo
- `mouse_controller.py`: Control del mouse con gestos
- `calibration.py`: Sistema de calibración afín 2D

**src/database/**
- `db_manager.py`: Gestor SQLite completo

**src/ui/**
- `main_window.py`: Ventana principal con UI mejorada

**src/utils/**
- `logger.py`: Sistema de logging
- `config.py`: Gestor de configuración
- `error_handler.py`: Manejo centralizado de errores

#### Scripts Nuevos
- `main.py`: Punto de entrada v2.0 completo
- `manage_user.py`: Utilidad para gestión de usuarios

#### Documentación
- `GUIDE.md`: Guía completa de usuario
- `CHANGELOG.md`: Este archivo
- `README.md`: Actualizado con nueva información

#### Mejoras Técnicas
- Filtro OneEuro adaptativo mejorado
- Sistema de calibración con persistencia
- Verificación continua de identidad
- Optimización de rendimiento
- Mejor manejo de recursos de cámara

---

## [1.0.0] - 2024

### Versión Original

**Características**
- Control básico del mouse por seguimiento de iris
- Filtro OneEuro para suavizado
- Sistema de calibración de 9 puntos
- Gestos por guiños (click, navegación)
- Scroll automático por zonas
- Dwell click opcional

**Archivos**
- `gaze_control.py`: Sistema completo
- `mouse_iris_min.py`: Versión minimalista
- `test_iris.py`: Script de prueba

**Limitaciones**
- Sin autenticación
- Sin persistencia de datos
- Código monolítico
- No hay logs
- Configuración solo en runtime

---

## Notas de Migración

### De v1.0 a v2.0

1. **Compatibilidad**: La versión 1.0 (`gaze_control.py`) sigue disponible
2. **Migración**: Ejecuta `python main.py` para usar v2.0
3. **Registro**: Primera vez requiere registro de usuario
4. **Configuraciones**: Ajustes de v1.0 deben aplicarse manualmente en `data/config.json`

### Requisitos Nuevos
- Python 3.10+ recomendado (v1.0 usaba 3.7+)
- Mismo hardware y dependencias base
- Espacio adicional para base de datos (~5-10 MB)

---

## Roadmap Futuro

### v2.1 (Planeado)
- [ ] Soporte para múltiples usuarios
- [ ] Cifrado de base de datos
- [ ] Exportación de estadísticas
- [ ] Perfiles de configuración predefinidos

### v3.0 (Ideas)
- [ ] Interfaz gráfica con Tkinter/Qt
- [ ] Calibración automática con machine learning
- [ ] Soporte para múltiples monitores
- [ ] API REST para integración externa
- [ ] Modo de accesibilidad mejorado
