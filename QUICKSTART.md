# Quick Start - Gaze Control v2.0

## Inicio Rápido en 3 Pasos

### 1️⃣ Verificar Sistema
```bash
python check_syntax.py
```
Verifica que todos los archivos Python tengan sintaxis correcta.

### 2️⃣ Instalar (Primera vez)
```bash
python setup.py
```
Instala dependencias y prepara el sistema.

### 3️⃣ Ejecutar
```bash
python main.py
```

## Primera Ejecución

Al ejecutar por primera vez:

1. **Registro de Usuario**
   - Ingresa tu nombre
   - Mira a la cámara
   - Se capturarán 10 muestras de tu rostro
   - Mueve ligeramente la cabeza

2. **Autenticación**
   - Mira a la cámara
   - El sistema verificará tu identidad

3. **Calibración** (recomendado)
   - Presiona `c`
   - Mira cada círculo amarillo durante 0.4 segundos
   - 9 puntos en total

4. **¡Usar!**
   - Mueve los ojos para mover el cursor
   - Guiña el ojo izquierdo para hacer click
   - Guiña el ojo derecho para ir atrás

## Controles Rápidos

| Tecla | Acción |
|-------|--------|
| `c` | Calibrar |
| `r` | Reset calibración |
| `d` | Toggle debug |
| `+/-` | Sensibilidad |
| `g` | Dwell click |
| `q` | Salir |

## Gestos

### Básicos
- 👁️ Guiño izquierdo corto = Click izquierdo
- 👁️👁️ Doble guiño izquierdo = Página adelante
- 👁️ Guiño derecho corto = Página atrás

### Avanzados ⭐ NUEVO
- 👁️ Guiño izquierdo SOSTENIDO (~0.5s) = **Click derecho**
- 👁️ Ojo derecho cerrado + Mover derecha = **Siguiente pestaña**
- 👁️ Ojo derecho cerrado + Mover izquierda = **Pestaña anterior**

## Scripts Útiles

### Gestión de Usuario
```bash
python manage_user.py
```
Ver info, estadísticas o eliminar usuario.

### Validar Sistema
```bash
python validate.py
```
Verifica que todos los módulos se importen correctamente.

### Verificar Sintaxis
```bash
python check_syntax.py
```
Compila todos los archivos para detectar errores.

## Solución Rápida de Problemas

### ❌ Error: "No se pudo abrir la cámara"
- Cierra otras apps que usen la cámara
- Verifica que la cámara esté conectada

### ❌ Error: "ModuleNotFoundError"
```bash
python setup.py
```

### ❌ Error: "Autenticación fallida"
- Mejora la iluminación
- Acércate más a la cámara
- Si persiste, elimina `data/users.db` y registra nuevamente

### ❌ El cursor se mueve muy rápido
- Presiona `-` para reducir sensibilidad
- Presiona `r` para resetear calibración
- Presiona `c` para recalibrar

### ❌ El cursor no se mueve
- Presiona `+` para aumentar sensibilidad
- Verifica que estés mirando a la cámara
- Presiona `c` para calibrar

## Estructura de Archivos

```
vision-artificial/
├── main.py              ← Ejecutar este
├── setup.py             ← Primera vez
├── manage_user.py       ← Gestión
├── validate.py          ← Validar
├── check_syntax.py      ← Sintaxis
├── src/                 ← Código fuente
└── data/                ← Datos (se crea automáticamente)
    ├── users.db
    ├── config.json
    └── logs/
```

## Documentación Completa

- **README.md** - Información general
- **GUIDE.md** - Guía detallada
- **CHANGELOG.md** - Cambios
- **IMPLEMENTATION_SUMMARY.md** - Detalles técnicos

## Soporte

Si encuentras problemas:
1. Revisa los logs en `data/logs/`
2. Consulta GUIDE.md
3. Ejecuta `python validate.py`

---

**Versión**: 2.0.0
**¿Listo para empezar?** → `python main.py`
