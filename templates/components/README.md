# Componentes Reutilizables

Este directorio contiene componentes HTML reutilizables para mantener consistencia en toda la aplicación.

## 📁 Componentes Disponibles

### 1. `navbar_usuarios.html`
**Descripción**: Barra de navegación principal para usuarios registrados.

**Uso**:
```html
{% include 'components/navbar_usuarios.html' %}
```

**Características**:
- Logo "Workify" que enlaza al inicio
- Enlaces a: Inicio, Perfil, Postulaciones
- Diseño responsive
- Usa `url_for()` para enlaces dinámicos

### 2. `navbar_usuarios.html` (Usado en todas las páginas de usuarios)
**Descripción**: Barra de navegación principal para usuarios registrados, utilizada en todas las páginas de usuarios.

**Uso**:
```html
{% include 'components/navbar_usuarios.html' %}
```

**Características**:
- Logo "Workify" con imagen
- Enlaces a: Inicio, Perfil, Postulaciones
- Indicador visual de página activa
- Diseño responsive
- Usa `url_for()` para enlaces dinámicos

### 3. `sidebar_admin.html`
**Descripción**: Barra lateral para el dashboard de administrador.

**Uso**:
```html
{% include 'components/sidebar_admin.html' %}
```

**Características**:
- Navegación por pestañas: Usuarios, Empleos, Reportes
- Iconos SVG de Heroicons
- Botón de cerrar sesión
- Funcionalidad de colapso
- Enlaces dinámicos con `url_for()`

## 🔧 Cómo Agregar Nuevos Componentes

1. Crea un nuevo archivo `.html` en este directorio
2. Usa la sintaxis de Jinja2 para enlaces dinámicos: `{{ url_for('nombre_ruta') }}`
3. Documenta el componente en este README
4. Incluye el componente en los templates usando: `{% include 'components/nombre_componente.html' %}`

## 📝 Convenciones

- **Nombres de archivos**: Usar snake_case (ej: `navbar_usuarios.html`)
- **Comentarios**: Incluir descripción del componente al inicio del archivo
- **Enlaces**: Usar `url_for()` en lugar de URLs hardcodeadas
- **Responsive**: Todos los componentes deben ser responsive

## 🎨 Estilos

Los componentes utilizan los archivos CSS existentes:
- `Inicio_usuarios.css` para navbar de usuarios (usado en todas las páginas de usuarios)
- CSS del dashboard para sidebar de admin

## 🔄 Mantenimiento

Para actualizar un componente:
1. Modifica el archivo del componente
2. Los cambios se reflejarán automáticamente en todos los templates que lo incluyan
3. No es necesario modificar cada template individualmente 