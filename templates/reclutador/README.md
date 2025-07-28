# Módulo de Reclutador - Workify

Este módulo proporciona una interfaz completa para que los reclutadores gestionen vacantes, postulaciones y candidatos en la plataforma Workify.

## 📁 Estructura de Archivos

```
templates/reclutador/
├── base.html              # Plantilla base con sidebar y navegación
├── dashboard.html         # Dashboard principal del reclutador
├── vacantes.html         # Gestión de vacantes publicadas
├── crear_vacante.html    # Formulario para crear nueva vacante
├── postulaciones.html    # Lista de postulaciones recibidas
├── candidato.html        # Perfil detallado del candidato
└── README.md            # Esta documentación

static/reclutador/
├── base.css             # Estilos base del módulo
└── base.js              # JavaScript base con funcionalidades
```

## 🎨 Características de Diseño

### Diseño Moderno
- **Sidebar fijo** con navegación principal
- **Gradientes azules** para elementos principales
- **Cards con sombras suaves** y bordes redondeados
- **Badges de estado** con colores distintivos
- **Iconos Font Awesome** para mejor UX

### Componentes Reutilizables
- **Cards**: Contenedores con header, body y footer
- **Badges**: Estados con colores (success, warning, danger, info)
- **Buttons**: Botones con variantes (primary, secondary, danger)
- **Tables**: Tablas responsivas con hover effects
- **Forms**: Campos de entrada con validación

### Responsive Design
- **Desktop**: Layout de 3 columnas con sidebar fijo
- **Tablet**: Sidebar colapsado, contenido adaptado
- **Mobile**: Stack vertical, navegación optimizada

## 📄 Páginas del Módulo

### 1. Dashboard (`/reclutador/dashboard`)
- **Estadísticas principales**: Vacantes activas, postulaciones totales, nuevas hoy, candidatos aceptados
- **Postulaciones recientes**: Tabla con las últimas 3 aplicaciones
- **Acciones rápidas**: Enlaces directos a funciones principales
- **Actividad reciente**: Timeline de eventos importantes

### 2. Vacantes Publicadas (`/reclutador/vacantes`)
- **Filtros avanzados**: Buscar, estado, tipo de trabajo
- **Tabla de vacantes**: Título, empresa, ubicación, fecha, postulaciones, estado
- **Acciones por vacante**: Ver, editar, eliminar, reabrir
- **Paginación**: Navegación entre páginas de resultados

### 3. Crear Vacante (`/reclutador/crear-vacante`)
- **Formulario completo**: Información básica, detalles, descripción, habilidades
- **Secciones organizadas**: Información básica, adicional, descripción, contacto
- **Vista previa**: Preview de cómo se verá la vacante
- **Auto-guardado**: Funcionalidad de guardado automático

### 4. Postulaciones Recibidas (`/reclutador/postulaciones`)
- **Estadísticas de estado**: Total, en revisión, aceptadas, rechazadas
- **Filtros múltiples**: Candidato, estado, vacante, fecha
- **Tabla detallada**: Información del candidato, vacante, fecha, puntuación
- **Acciones rápidas**: Ver perfil, aceptar, rechazar, entrevista

### 5. Perfil del Candidato (`/reclutador/candidato/<id>`)
- **Información personal**: Datos de contacto, educación, experiencia
- **Evaluación visual**: Puntuación general y por categorías
- **Habilidades técnicas**: Organizadas por categorías
- **Documentos**: CV, carta de presentación, portfolio
- **Acciones**: Programar entrevista, enviar mensaje, cambiar estado

## 🎯 Funcionalidades JavaScript

### Utilidades Base
- **Tooltips**: Información adicional al hacer hover
- **Validación de formularios**: Campos requeridos con mensajes de error
- **Interacciones de tabla**: Selección de filas con highlight
- **Animaciones de badges**: Efectos sutiles en hover

### Notificaciones
- **Sistema de notificaciones**: Mensajes temporales en la esquina superior derecha
- **Tipos**: Success, error, warning, info
- **Auto-dismiss**: Desaparecen automáticamente después de 3 segundos

### Confirmaciones
- **Modales de confirmación**: Para acciones destructivas
- **Personalizables**: Mensaje y callback personalizados
- **Estilo consistente**: Diseño uniforme con el resto de la UI

## 🎨 Paleta de Colores

### Colores Principales
- **Azul primario**: `#3B82F6` (botones, enlaces, elementos activos)
- **Azul oscuro**: `#1E40AF` (gradientes, elementos destacados)
- **Gris claro**: `#F8FAFC` (fondo principal)
- **Gris medio**: `#6B7280` (texto secundario)

### Estados
- **Success**: `#10B981` (aceptado, completado)
- **Warning**: `#F59E0B` (en revisión, pendiente)
- **Danger**: `#EF4444` (rechazado, error)
- **Info**: `#3B82F6` (información, neutral)

## 📱 Responsive Breakpoints

### Desktop (1024px+)
- Sidebar fijo de 280px
- Layout de 3 columnas
- Navegación completa visible

### Tablet (768px - 1023px)
- Sidebar reducido a 240px
- Grid adaptativo
- Contenido ajustado

### Mobile (< 768px)
- Sidebar colapsado
- Stack vertical
- Navegación optimizada para touch

## 🔧 Integración con Flask

### Rutas Sugeridas
```python
@app.route('/reclutador/dashboard')
def reclutador_dashboard():
    return render_template('reclutador/dashboard.html')

@app.route('/reclutador/vacantes')
def reclutador_vacantes():
    return render_template('reclutador/vacantes.html')

@app.route('/reclutador/crear-vacante')
def reclutador_crear_vacante():
    return render_template('reclutador/crear_vacante.html')

@app.route('/reclutador/postulaciones')
def reclutador_postulaciones():
    return render_template('reclutador/postulaciones.html')

@app.route('/reclutador/candidato/<int:id>')
def reclutador_candidato(id):
    return render_template('reclutador/candidato.html')
```

### Autenticación
- Verificar que el usuario sea de tipo 'reclutador'
- Redirigir a login si no está autenticado
- Proteger todas las rutas del módulo

## 🚀 Próximas Mejoras

### Funcionalidades Planificadas
- **Búsqueda avanzada**: Filtros por múltiples criterios
- **Exportación de datos**: PDF, Excel, CSV
- **Notificaciones en tiempo real**: WebSockets para actualizaciones
- **Calendario de entrevistas**: Integración con Google Calendar
- **Evaluación automática**: IA para scoring de candidatos

### Mejoras de UX
- **Drag & drop**: Para reordenar elementos
- **Bulk actions**: Acciones en lote
- **Keyboard shortcuts**: Atajos de teclado
- **Dark mode**: Tema oscuro opcional

## 📝 Notas de Desarrollo

### Convenciones
- **Nomenclatura**: BEM para CSS, camelCase para JavaScript
- **Espaciado**: 1rem = 16px base
- **Tipografía**: Inter como fuente principal
- **Iconos**: Font Awesome 6.0

### Accesibilidad
- **ARIA labels**: Para elementos interactivos
- **Contraste**: Cumple estándares WCAG
- **Navegación por teclado**: Tab order lógico
- **Screen readers**: Textos alternativos

### Performance
- **Lazy loading**: Para imágenes y contenido pesado
- **CSS optimizado**: Sin reglas duplicadas
- **JavaScript modular**: Funciones reutilizables
- **Caching**: Headers apropiados para assets estáticos 