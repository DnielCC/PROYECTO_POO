# Sistema de Postulaciones y Calificaciones

## Descripción General

Este sistema permite a los usuarios (aspirantes) ver las vacantes creadas por reclutadores, postularse a ellas, calificarlas y gestionar sus postulaciones. El sistema está integrado con la base de datos existente y mantiene la funcionalidad sin modificar la estructura de datos.

## Funcionalidades Implementadas

### 1. Visualización de Vacantes
- **Ubicación**: `/inicio/usuarios`
- **Descripción**: Muestra todas las vacantes activas creadas por reclutadores
- **Características**:
  - Lista de vacantes con información completa
  - Sistema de calificación con estrellas (1-5)
  - Botón para postularse
  - Filtros por modalidad, tipo de contrato y salario

### 2. Sistema de Postulaciones
- **Ruta**: `/aplicar_vacante` (POST)
- **Funcionalidad**: Permite a los usuarios postularse a vacantes
- **Validaciones**:
  - Usuario debe estar logueado
  - No puede postularse dos veces a la misma vacante
  - Verifica que la vacante esté activa

### 3. Sistema de Calificaciones
- **Ruta**: `/calificar_vacante` (POST)
- **Funcionalidad**: Permite calificar vacantes con estrellas (1-5)
- **Características**:
  - Calificación interactiva con estrellas
  - Actualización en tiempo real
  - Una calificación por usuario por vacante
  - Actualización si ya existe una calificación

### 4. Gestión de Postulaciones
- **Ubicación**: `/user/postulaciones`
- **Funcionalidades**:
  - Ver todas las postulaciones del usuario
  - Filtrar por estado (pendiente, revisando, aceptada, rechazada, cancelada)
  - Buscar por empresa o puesto
  - Cancelar postulaciones pendientes o en revisión
  - Ver detalles completos de cada postulación

### 5. Cancelación de Postulaciones
- **Ruta**: `/cancelar_postulacion` (POST)
- **Funcionalidad**: Permite cancelar postulaciones en estados específicos
- **Estados permitidos**: pendiente, revisando

## Estructura de la Base de Datos

### Tablas Utilizadas
1. **vacantes**: Almacena la información de las vacantes
2. **postulaciones**: Registra las postulaciones de usuarios
3. **calificaciones_vacantes**: Almacena las calificaciones de usuarios a vacantes
4. **login**: Información de usuarios
5. **informacion**: Información adicional de usuarios

### Campos Clave
- `postulaciones.id_usuario`: ID del usuario que se postula
- `postulaciones.id_vacante`: ID de la vacante
- `postulaciones.id_estatus`: Estado de la postulación
- `calificaciones_vacantes.calificacion`: Puntuación (1-5)

## Flujo de Usuario

### 1. Explorar Vacantes
1. Usuario accede a `/inicio/usuarios`
2. Ve lista de vacantes disponibles
3. Puede calificar vacantes con estrellas
4. Hace clic en "Aplicar ahora" para postularse

### 2. Postularse
1. Sistema verifica que el usuario esté logueado
2. Valida que no se haya postulado antes
3. Crea registro en tabla `postulaciones`
4. Confirma la postulación exitosa

### 3. Gestionar Postulaciones
1. Usuario accede a `/user/postulaciones`
2. Ve todas sus postulaciones con estados
3. Puede filtrar y buscar
4. Puede cancelar postulaciones permitidas

## Archivos Modificados/Creados

### Backend (Python)
- `hello.py`: Agregadas rutas para postulaciones y calificaciones
- `config.py`: Agregado método `insert_datos_parametrizados`

### Frontend (HTML/CSS/JS)
- `templates/inicio_usuarios.html`: Sistema de calificación y postulación
- `templates/mis_postulaciones.html`: Gestión de postulaciones
- `static/Perfil.css`: Estilos para el sistema
- `static/Postulaciones.css`: Estilos específicos para postulaciones
- `static/script.js`: Funcionalidades JavaScript

## Estados de Postulación

| Estado | Descripción | Acciones Permitidas |
|--------|-------------|---------------------|
| Pendiente | Postulación recién enviada | Cancelar |
| Revisando | En proceso de revisión | Cancelar |
| Aceptada | Postulación aceptada | Ver detalles |
| Rechazada | Postulación rechazada | Ver detalles |
| Cancelada | Postulación cancelada por usuario | Ver detalles |

## Características Técnicas

### Seguridad
- Validación de sesión en todas las operaciones
- Verificación de propiedad de postulaciones
- Sanitización de datos de entrada

### UX/UI
- Notificaciones en tiempo real
- Animaciones suaves
- Diseño responsivo
- Filtros y búsqueda intuitivos

### Performance
- Consultas SQL optimizadas
- Carga asíncrona de datos
- Validaciones del lado del cliente y servidor

## Instalación y Configuración

### Requisitos
- Python 3.7+
- Flask
- MySQL/MariaDB
- Base de datos configurada según `config.py`

### Pasos
1. Asegurar que la base de datos esté configurada
2. Verificar que las tablas existan
3. Ejecutar la aplicación Flask
4. Acceder a las rutas correspondientes

## Uso del Sistema

### Para Usuarios (Aspirantes)
1. **Registrarse/Iniciar sesión**
2. **Explorar vacantes**: Ir a `/inicio/usuarios`
3. **Postularse**: Hacer clic en "Aplicar ahora"
4. **Calificar**: Usar sistema de estrellas
5. **Gestionar**: Ir a `/user/postulaciones`

### Para Reclutadores
1. **Crear vacantes**: Usar panel de reclutador
2. **Revisar postulaciones**: Panel de postulaciones
3. **Cambiar estados**: Aceptar/rechazar candidatos

## Notas Importantes

- El sistema no modifica la estructura de la base de datos existente
- Las calificaciones son opcionales y no afectan el proceso de postulación
- Los usuarios solo pueden ver sus propias postulaciones
- El sistema mantiene un historial completo de todas las acciones

## Solución de Problemas

### Error: "Usuario no logueado"
- Verificar que la sesión esté activa
- Redirigir al login si es necesario

### Error: "Ya te has postulado"
- Verificar duplicados en la base de datos
- Limpiar registros duplicados si es necesario

### Error: "Vacante no encontrada"
- Verificar que la vacante exista y esté activa
- Comprobar permisos de acceso

## Futuras Mejoras

- Sistema de notificaciones por email
- Dashboard de estadísticas para usuarios
- Historial de calificaciones
- Recomendaciones de vacantes
- Sistema de favoritos
- Exportación de postulaciones
