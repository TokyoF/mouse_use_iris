# Guía de Configuración de Sensibilidad

## Resumen de Mejoras

El sistema ahora tiene **configuración optimizada para alta performance** con movimientos más rápidos del cursor y menor movimiento de cabeza requerido.

---

## ⚡ Cambios Realizados

### Parámetros Anteriores vs Nuevos (Perfil Performance)

| Parámetro | Antes | Ahora | Mejora |
|-----------|-------|-------|--------|
| **Gain** | 1.20 | **1.85** | +54% más sensibilidad |
| **Deadzone** | 0.015 | **0.008** | -47% movimiento requerido |
| **Filter Min Cutoff** | 1.2 | **2.0** | +67% más responsivo |
| **Filter Beta** | 0.04 | **0.08** | +100% mejor respuesta a velocidad |

### Resultados Esperados:

✅ **Cursor se mueve ~50% más rápido** con el mismo movimiento de cabeza
✅ **Menor movimiento de cabeza necesario** para alcanzar los bordes de la pantalla
✅ **Respuesta más rápida** a movimientos bruscos
✅ **Menos latencia** entre movimiento y respuesta del cursor

---

## 🎯 Perfiles de Sensibilidad Disponibles

El sistema ahora incluye 4 perfiles predefinidos para diferentes necesidades:

### 1. CONSERVATIVE (Conservador)
**Ideal para:** Principiantes, usuarios que prefieren precisión sobre velocidad

```
Gain: 1.0
Deadzone: 0.020
Min Cutoff: 0.8
Beta: 0.03
```

**Características:**
- ⏱️ Movimiento lento y suave
- 🎯 Máxima precisión
- 😌 Fácil de controlar
- ⚠️ Requiere más movimiento de cabeza

---

### 2. BALANCED (Equilibrado)
**Ideal para:** Uso general, balance entre precisión y velocidad

```
Gain: 1.4
Deadzone: 0.012
Min Cutoff: 1.5
Beta: 0.05
```

**Características:**
- ⚖️ Balance óptimo
- 👌 Buena precisión
- 🏃 Velocidad moderada
- ✅ Recomendado para empezar

---

### 3. PERFORMANCE (Alta Performance) ⭐ **POR DEFECTO**
**Ideal para:** Usuarios experimentados, trabajo rápido, gaming

```
Gain: 1.85
Deadzone: 0.008
Min Cutoff: 2.0
Beta: 0.08
```

**Características:**
- ⚡ Alta velocidad
- 🚀 Respuesta rápida
- 💪 Menor esfuerzo físico
- ⭐ **Configuración por defecto del sistema**

---

### 4. EXTREME (Extremo)
**Ideal para:** Expertos, usuarios con excelente control, tareas muy rápidas

```
Gain: 2.3
Deadzone: 0.005
Min Cutoff: 2.5
Beta: 0.12
```

**Características:**
- 🔥 Máxima velocidad
- ⚡ Ultra responsivo
- 🎮 Requiere buen control
- ⚠️ Puede ser difícil de controlar para principiantes

---

## 🛠️ Cómo Cambiar el Perfil de Sensibilidad

### Método 1: Script de Cambio Rápido (Recomendado)

```bash
python change_sensitivity.py
```

Este script te permite:
1. Ver tu configuración actual
2. Seleccionar un perfil predefinido
3. Configurar parámetros manualmente
4. Ver descripciones de cada perfil

**Ejemplo de uso:**
```
CONFIGURACIÓN DE SENSIBILIDAD - Gaze Control v2.0
==================================================

Configuración actual:
  Gain (sensibilidad): 1.85
  Deadzone (zona muerta): 0.008
  Perfil actual: PERFORMANCE

Opciones:
1. Aplicar perfil CONSERVATIVE (lento y preciso)
2. Aplicar perfil BALANCED (equilibrado)
3. Aplicar perfil PERFORMANCE (rápido - recomendado)
4. Aplicar perfil EXTREME (ultra rápido)
5. Configuración manual
6. Salir sin cambios

Selecciona una opción (1-6): 4

✓ Perfil EXTREME aplicado
```

### Método 2: Durante la Ejecución (Teclas [+] y [-])

Mientras el programa está ejecutándose:
- Presiona **[+]** o **[=]** para aumentar sensibilidad (incrementos de 0.05)
- Presiona **[-]** para disminuir sensibilidad (decrementos de 0.05)
- Los cambios se guardan automáticamente

**Rango permitido:** 0.5 - 2.5

### Método 3: Editar Archivo de Configuración

Edita directamente: `data/config.json`

```json
{
    "gain": 1.85,
    "deadzone": 0.008,
    "filter_min_cutoff": 2.0,
    "filter_beta": 0.08
}
```

Guarda y reinicia la aplicación.

---

## 📊 Entendiendo los Parámetros

### 1. **GAIN** (Sensibilidad)

**¿Qué hace?** Multiplica el movimiento de tus ojos para convertirlo en movimiento del cursor.

- **Valor bajo (0.8-1.2):** Cursor se mueve lento, requiere más movimiento de cabeza
- **Valor medio (1.3-1.6):** Balance entre velocidad y control
- **Valor alto (1.7-2.3):** Cursor se mueve rápido, menos movimiento requerido
- **Valor muy alto (2.4+):** Puede ser difícil de controlar

**Rango recomendado:** 0.8 - 2.5  
**Por defecto:** 1.85

**Ejemplo visual:**
```
Gain = 1.0: Tu cabeza se mueve 5cm → Cursor se mueve 5cm
Gain = 1.85: Tu cabeza se mueve 5cm → Cursor se mueve 9.25cm
Gain = 2.3: Tu cabeza se mueve 5cm → Cursor se mueve 11.5cm
```

---

### 2. **DEADZONE** (Zona Muerta)

**¿Qué hace?** Define el movimiento mínimo necesario para que el cursor se mueva.

- **Valor bajo (0.005-0.010):** Muy sensible, cursor responde a micro-movimientos
- **Valor medio (0.011-0.015):** Balance, ignora temblores pequeños
- **Valor alto (0.016-0.025):** Menos sensible, ignora movimientos pequeños

**Rango recomendado:** 0.005 - 0.025  
**Por defecto:** 0.008

**Cuándo ajustar:**
- ⬇️ **Disminuir** si el cursor no responde a movimientos pequeños
- ⬆️ **Aumentar** si el cursor "tiembla" o se mueve sin querer

---

### 3. **FILTER_MIN_CUTOFF** (Suavizado Mínimo)

**¿Qué hace?** Controla cuánto se suaviza el movimiento del cursor.

- **Valor bajo (0.5-1.0):** Cursor muy suave pero con latencia
- **Valor medio (1.1-1.8):** Balance entre suavidad y respuesta
- **Valor alto (1.9-3.0):** Cursor más directo, menos suavizado

**Rango recomendado:** 0.5 - 3.0  
**Por defecto:** 2.0

**Cuándo ajustar:**
- ⬆️ **Aumentar** si el cursor se siente "lento" o "pegajoso"
- ⬇️ **Disminuir** si el cursor es muy "nervioso" o "inestable"

---

### 4. **FILTER_BETA** (Respuesta a Velocidad)

**¿Qué hace?** Controla cómo el filtro se adapta a movimientos rápidos.

- **Valor bajo (0.02-0.04):** El filtro no se adapta mucho a velocidad
- **Valor medio (0.05-0.08):** Adaptación moderada
- **Valor alto (0.09-0.15):** Adaptación agresiva a movimientos rápidos

**Rango recomendado:** 0.02 - 0.15  
**Por defecto:** 0.08

**Cuándo ajustar:**
- ⬆️ **Aumentar** si movimientos rápidos se sienten lentos
- ⬇️ **Disminuir** si el cursor es muy errático en movimientos rápidos

---

## 🔧 Configuración Manual Avanzada

Si ningún perfil se ajusta a tus necesidades:

```bash
python change_sensitivity.py
# Selecciona opción 5: "Configuración manual"
```

El script te guiará paso a paso para configurar cada parámetro.

**Ejemplo:**
```
CONFIGURACIÓN MANUAL
==================================================

Gain (sensibilidad del cursor):
  Rango recomendado: 0.8 - 2.5
  Valor actual: 1.85
  Nuevo valor (Enter para mantener): 2.0
  ✓ Gain configurado a 2.0

Deadzone (zona muerta - menor = más sensible):
  Rango recomendado: 0.005 - 0.025
  Valor actual: 0.008
  Nuevo valor (Enter para mantener): 0.006
  ✓ Deadzone configurado a 0.006
```

---

## 💡 Consejos para Encontrar tu Configuración Ideal

### Paso 1: Empieza con un Perfil
```bash
python change_sensitivity.py
# Selecciona PERFORMANCE (opción 3)
```

### Paso 2: Prueba el Sistema
```bash
python main.py
```

### Paso 3: Ajusta Durante el Uso
- Si es muy lento → Presiona **[+]** varias veces
- Si es muy rápido → Presiona **[-]** varias veces
- Prueba navegar por diferentes aplicaciones

### Paso 4: Refina con Configuración Manual
Si necesitas ajustes más finos:
```bash
python change_sensitivity.py
# Selecciona opción 5: Configuración manual
```

---

## 🎮 Configuraciones Recomendadas por Uso

### Navegación Web / Documentos
```
Perfil: BALANCED o PERFORMANCE
Gain: 1.4 - 1.85
Deadzone: 0.010 - 0.012
```

### Diseño Gráfico / Precisión
```
Perfil: CONSERVATIVE o BALANCED
Gain: 1.0 - 1.4
Deadzone: 0.015 - 0.020
```

### Gaming / Tareas Rápidas
```
Perfil: PERFORMANCE o EXTREME
Gain: 1.85 - 2.3
Deadzone: 0.005 - 0.008
```

### Presentaciones
```
Perfil: BALANCED
Gain: 1.4
Deadzone: 0.012
```

---

## ⚠️ Solución de Problemas

### Problema: "El cursor se mueve demasiado rápido, no puedo controlarlo"

**Solución:**
1. Aplica perfil BALANCED:
   ```bash
   python change_sensitivity.py
   # Selecciona opción 2
   ```
2. O reduce el gain durante ejecución: presiona **[-]** múltiples veces

---

### Problema: "El cursor es muy lento, necesito mover mucho la cabeza"

**Solución:**
1. Aplica perfil EXTREME:
   ```bash
   python change_sensitivity.py
   # Selecciona opción 4
   ```
2. O aumenta el gain durante ejecución: presiona **[+]** múltiples veces

---

### Problema: "El cursor 'tiembla' o se mueve sin querer"

**Solución:**
1. Aumenta el deadzone:
   ```bash
   python change_sensitivity.py
   # Selecciona opción 5: Configuración manual
   # Aumenta deadzone a 0.015-0.020
   ```
2. Verifica la iluminación de tu ambiente
3. Asegúrate de estar a distancia adecuada de la cámara

---

### Problema: "El cursor no responde a movimientos pequeños"

**Solución:**
1. Disminuye el deadzone:
   ```bash
   python change_sensitivity.py
   # Selecciona opción 5: Configuración manual
   # Disminuye deadzone a 0.005-0.008
   ```

---

### Problema: "El cursor se siente 'pesado' o con latencia"

**Solución:**
1. Aumenta filter_min_cutoff y filter_beta:
   ```bash
   python change_sensitivity.py
   # Selecciona opción 5: Configuración manual
   # Aumenta filter_min_cutoff a 2.0-2.5
   # Aumenta filter_beta a 0.08-0.12
   ```

---

## 📈 Comparación de Perfiles

| Característica | Conservative | Balanced | Performance | Extreme |
|----------------|-------------|----------|-------------|---------|
| Velocidad | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Precisión | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Facilidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Esfuerzo físico | Alto | Medio | Bajo | Muy bajo |
| Recomendado para | Principiantes | Uso general | Expertos | Profesionales |

---

## 🚀 Comandos Rápidos

```bash
# Ver y cambiar perfil de sensibilidad
python change_sensitivity.py

# Ejecutar con nueva configuración
python main.py

# Durante ejecución:
# [+] o [=] - Aumentar sensibilidad
# [-] - Disminuir sensibilidad
# [d] - Toggle modo debug (ver configuración actual)
```

---

## 📝 Notas Importantes

1. **Los cambios se guardan automáticamente** tanto desde `change_sensitivity.py` como desde las teclas durante ejecución
2. **Cada usuario tiene su propia configuración** - Los cambios solo afectan al usuario logueado
3. **La configuración se carga al inicio** - Si cambias el perfil, reinicia la aplicación
4. **No hay configuración "incorrecta"** - Lo mejor es lo que funcione para ti
5. **Puedes volver al perfil por defecto** en cualquier momento ejecutando `change_sensitivity.py`

---

## 🎯 Mejores Prácticas

1. **Empieza con PERFORMANCE** (configuración por defecto)
2. **Da tiempo de adaptación** (15-30 minutos) antes de cambiar
3. **Ajusta en pequeños incrementos** (0.1-0.2 para gain)
4. **Mantén buena iluminación** para mejor detección facial
5. **Siéntate a distancia adecuada** de la cámara (50-80cm)

---

**¡El sistema ahora es significativamente más rápido y requiere menos movimiento de cabeza! 🚀**

Para cualquier duda, consulta la documentación completa en `README.md` o `MULTI_USER_GUIDE.md`.
