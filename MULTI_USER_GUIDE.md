# Guía de Sistema Multi-Usuario

## Resumen de Cambios

El sistema ahora soporta **múltiples usuarios** y garantiza que **solo el usuario autenticado** pueda controlar el mouse, incluso si hay múltiples rostros en la pantalla.

## Problemas Resueltos

### 1. **Un Solo Usuario Registrado (RESUELTO)**
**Antes:** Solo se podía registrar un usuario en el sistema.

**Ahora:** Puedes registrar múltiples usuarios usando `manage_user.py`.

### 2. **Múltiples Rostros Causan Conflictos (RESUELTO)**
**Antes:** Si había 2+ personas frente a la cámara, cualquier rostro detectado podía mover el mouse.

**Ahora:** El sistema detecta hasta 3 rostros simultáneamente y solo permite control al usuario **logueado activamente**. Si detecta múltiples rostros o el rostro del usuario no coincide, **BLOQUEA COMPLETAMENTE** el control del mouse.

### 3. **No Había Sistema de Login (RESUELTO)**
**Antes:** El sistema solo verificaba si había un usuario registrado.

**Ahora:** 
- Al iniciar, seleccionas tu usuario de una lista
- El sistema verifica tu identidad con reconocimiento facial
- Solo el usuario logueado puede controlar el mouse

### 4. **Validación de Seguridad Mejorada**
- Verificación periódica cada X segundos (configurable)
- Si se detecta un rostro no autorizado → **CONTROL BLOQUEADO**
- Si se detectan múltiples rostros → **CONTROL BLOQUEADO**
- Mensajes claros en pantalla indicando el estado de seguridad

---

## Cómo Usar el Sistema Multi-Usuario

### Primer Uso (Sin Usuarios Registrados)

```bash
python main.py
```

El sistema detectará que no hay usuarios y te guiará para registrar el primer usuario:
1. Ingresa tu nombre de usuario
2. Mira a la cámara durante la captura (10 muestras)
3. ¡Listo! Tu usuario está registrado

### Agregar Más Usuarios

```bash
python manage_user.py
```

Menú de opciones:
1. **Listar usuarios** - Ver todos los usuarios registrados y sus estadísticas
2. **Registrar nuevo usuario** - Agregar un usuario adicional al sistema
3. **Ver configuraciones de un usuario** - Ver ajustes personalizados
4. **Eliminar usuario** - Borrar un usuario del sistema
5. **Salir**

#### Ejemplo: Registrar un segundo usuario

```
> python manage_user.py

GESTOR DE USUARIOS - Gaze Control v2.0
Opciones:
1. Listar usuarios
2. Registrar nuevo usuario
3. Ver configuraciones de un usuario
4. Eliminar usuario
5. Salir

Selecciona una opción (1-5): 2

REGISTRAR NUEVO USUARIO
Ingresa el nombre del nuevo usuario: Maria

Registrando usuario: Maria
Se capturarán 10 muestras de su rostro.
Presiona ENTER para iniciar la cámara...
[Captura facial inicia...]
✓ Usuario 'Maria' registrado exitosamente!
```

### Login con Múltiples Usuarios

Al ejecutar `python main.py` con múltiples usuarios registrados:

```
SELECCIÓN DE USUARIO
==================================================
1. Juan
2. Maria
3. Pedro
==================================================

Selecciona tu usuario (número): 2

AUTENTICACIÓN FACIAL
==================================================
Verificando identidad de: Maria
Por favor, mira a la cámara...

✓ Autenticación exitosa! Bienvenido Maria
```

---

## Flujo de Seguridad Durante la Ejecución

### Escenario 1: Usuario Autenticado Solo
✅ **Control del mouse ACTIVADO**
- El usuario logueado es detectado
- Mouse responde a la mirada
- Gestos funcionan normalmente

### Escenario 2: Usuario No Reconocido
🚫 **Control del mouse BLOQUEADO**
- Mensaje en pantalla: "USUARIO NO RECONOCIDO - CONTROL BLOQUEADO"
- El mouse no se mueve
- Los gestos no funcionan
- El sistema continúa verificando hasta reconocer al usuario correcto

### Escenario 3: Múltiples Rostros Detectados
🚫 **Control del mouse BLOQUEADO**
- Mensaje en pantalla: "MULTIPLES ROSTROS DETECTADOS (2) - CONTROL BLOQUEADO"
- Aunque uno de los rostros sea el usuario logueado, el control permanece bloqueado
- Esto previene conflictos y asegura control exclusivo

### Escenario 4: No Se Detecta Rostro
⏸️ **Control en espera**
- Mensaje: "NO SE DETECTA ROSTRO"
- El sistema espera a que el usuario regrese frente a la cámara

---

## Migración de Base de Datos Existente

Si ya tenías usuarios registrados con la versión anterior:

```bash
python migrate_db.py
```

Este script:
1. Agrega la columna `is_logged_in` a la tabla de usuarios
2. Marca todos los usuarios como deslogueados
3. Preserva todos tus datos existentes (usuarios, configuraciones, calibraciones)

**Importante:** Se recomienda hacer un respaldo de `data/users.db` antes de ejecutar la migración.

---

## Arquitectura Técnica

### Cambios en la Base de Datos

**Tabla `users` - Campo nuevo:**
- `is_logged_in` (INTEGER): Indica si el usuario está actualmente logueado (0 o 1)

**Nuevos métodos en `DatabaseManager`:**
- `get_all_users()`: Obtiene lista de todos los usuarios
- `get_user_by_id(user_id)`: Obtiene usuario por ID
- `get_logged_in_user()`: Obtiene el usuario actualmente logueado
- `set_user_logged_in(user_id)`: Marca usuario como logueado (y desloguea a los demás)
- `logout_all_users()`: Desloguea a todos los usuarios

### Cambios en Autenticación Facial

**`FaceAuthenticator` - Nuevo parámetro:**
- `max_faces=3`: Detecta hasta 3 rostros simultáneamente

**Nuevo método:**
- `verify_face_multi(frame, registered_embedding)`: Verifica si el usuario registrado está entre múltiples rostros detectados
  - Retorna: `(es_match, mejor_similitud, num_rostros_detectados)`

### Cambios en `UserManager`

**Métodos actualizados:**
- `authenticate_user(frame)`: Ahora retorna también el número de rostros detectados
- `login(frame, user_id)`: Permite especificar qué usuario loguear
- `logout()`: Desloguea correctamente al usuario en la BD

**Nuevos métodos:**
- `get_all_users()`: Lista usuarios disponibles
- `select_and_login(frame)`: Modo interactivo de selección de usuario

### Cambios en Main Loop (`main.py`)

**Verificación de seguridad mejorada (líneas 283-295):**
```python
is_match, similarity, num_faces = self.user_manager.authenticate_user(frame)

if not is_match:
    # BLOQUEAR TODO CONTROL
    if num_faces > 1:
        warning = "MULTIPLES ROSTROS DETECTADOS - CONTROL BLOQUEADO"
    elif num_faces == 0:
        warning = "NO SE DETECTA ROSTRO"
    else:
        warning = "USUARIO NO RECONOCIDO - CONTROL BLOQUEADO"
    
    # Mostrar advertencia y NO procesar control del mouse
    continue
```

**El control del mouse SOLO se ejecuta si:**
1. El usuario está autenticado
2. Solo hay un rostro detectado
3. Ese rostro coincide con el usuario logueado

---

## Parámetros de Configuración

### Intervalo de Verificación de Autenticación
En `src/utils/config.py`:

```python
'auth_check_interval': 2.0  # Verificar cada 2 segundos
```

Ajusta este valor según tus necesidades:
- **Valor bajo (0.5-1s)**: Mayor seguridad, más procesamiento
- **Valor alto (3-5s)**: Menos procesamiento, menor frecuencia de verificación

### Umbral de Similitud Facial
En `src/auth/user_manager.py` (línea 14):

```python
self.face_auth = FaceAuthenticator(similarity_threshold=0.85)
```

- **0.85**: Equilibrio entre seguridad y usabilidad (recomendado)
- **0.90-0.95**: Mayor seguridad, puede rechazar al usuario legítimo con cambios de iluminación
- **0.75-0.80**: Más permisivo, menor seguridad

---

## Solución de Problemas

### "USUARIO NO RECONOCIDO" continuamente

**Posibles causas:**
1. Iluminación diferente a la del registro
2. Cambios en apariencia (lentes, gorra, barba)
3. Umbral de similitud muy alto

**Soluciones:**
1. Mejorar iluminación
2. Re-registrar el usuario: `python manage_user.py` → eliminar y crear nuevo
3. Ajustar el `similarity_threshold` (ver arriba)

### "MULTIPLES ROSTROS DETECTADOS" aunque estoy solo

**Posibles causas:**
1. Fotos o monitores con rostros en el fondo
2. Reflejos en ventanas/espejos

**Soluciones:**
1. Cambiar ángulo de la cámara
2. Ocultar/remover fotos del fondo
3. Evitar espejos en el campo de visión

### Base de datos corrupta después de migración

**Solución:**
1. Restaurar el respaldo de `data/users.db`
2. Volver a ejecutar `python migrate_db.py`
3. Si persiste, eliminar `data/users.db` y re-registrar usuarios

---

## Comandos Rápidos

```bash
# Ejecutar la aplicación
python main.py

# Gestionar usuarios (agregar/eliminar)
python manage_user.py

# Migrar base de datos existente
python migrate_db.py

# Instalación completa (primera vez)
install.bat  # Windows
# o
bash install.sh  # Linux/Mac
```

---

## Resumen de Archivos Modificados

### Archivos Principales Actualizados:
- `src/database/db_manager.py` - Soporte multi-usuario y campo `is_logged_in`
- `src/auth/face_auth.py` - Detección de múltiples rostros
- `src/auth/user_manager.py` - Login multi-usuario
- `main.py` - Validación estricta de seguridad en el loop principal

### Archivos Nuevos:
- `migrate_db.py` - Script de migración de BD
- `MULTI_USER_GUIDE.md` - Esta documentación

### Archivos Re-escritos:
- `manage_user.py` - Gestor completo de usuarios con interfaz mejorada

---

## Preguntas Frecuentes

**P: ¿Cuántos usuarios puedo registrar?**
R: No hay límite técnico. Puedes registrar tantos usuarios como necesites.

**P: ¿Puedo tener dos usuarios logueados simultáneamente?**
R: No. Solo un usuario puede estar logueado a la vez. Esto previene conflictos de control.

**P: ¿Se pueden compartir configuraciones entre usuarios?**
R: No. Cada usuario tiene sus propias configuraciones, calibración y preferencias.

**P: ¿Qué pasa si dos personas con usuarios registrados están frente a la cámara?**
R: El sistema detecta múltiples rostros y **BLOQUEA** el control hasta que solo quede una persona.

**P: ¿El sistema funciona con hermanos gemelos?**
R: El reconocimiento facial puede tener dificultades con gemelos idénticos debido a la alta similitud facial. Se recomienda usar nombres de usuario claramente diferentes y asegurarse de que cada gemelo se registre en condiciones de iluminación ligeramente diferentes.

---

## Contacto y Soporte

Para reportar problemas o sugerir mejoras, consulta el archivo `README.md` principal del proyecto.
