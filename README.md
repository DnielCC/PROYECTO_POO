# 🚀 Bolsa de Trabajo - Workify

Una aplicación web moderna para conectar empleadores y postulantes, construida con Flask y MySQL.

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **ORM**: SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript
- **Formularios**: Flask-WTF
- **Autenticación**: Sesiones Flask

## 📋 Requisitos Previos

1. **Python 3.8+**
2. **MySQL Server 8.0+**
3. **pip** (gestor de paquetes de Python)

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd PROYECTO_POO
```

### 2. Instalar Dependencias de Python
```bash
py -m pip install flask flask-wtf wtforms flask-sqlalchemy pymysql
```

### 3. Configurar MySQL

#### Opción A: MySQL Local
1. **Instalar MySQL Server**
   - Descarga desde: https://dev.mysql.com/downloads/mysql/
   - O usa XAMPP: https://www.apachefriends.org/

2. **Configurar credenciales**
   - Edita `config.py` y cambia la contraseña:
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:TU_CONTRASEÑA@localhost/bolsa_trabajo'
   ```

#### Opción B: SQLite (Desarrollo Rápido)
Si no quieres instalar MySQL, puedes usar SQLite:
1. Edita `config.py`
2. Comenta la línea de MySQL y descomenta SQLite:
```python
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/bolsa_trabajo'
SQLALCHEMY_DATABASE_URI = 'sqlite:///bolsa_trabajo.db'
```

### 4. Configurar la Base de Datos

#### Con MySQL:
```bash
py setup_database.py
```

#### Con SQLite:
```bash
py hello.py
```
(Se creará automáticamente)

### 5. Ejecutar la Aplicación
```bash
py hello.py
```

La aplicación estará disponible en: **http://127.0.0.1:5000**

## 📊 Estructura de la Base de Datos

### Tablas Principales:

1. **usuarios**
   - id, nombre, email, password_hash
   - ciudad, codigo_postal, fecha_registro
   - tipo_usuario (postulante/empleador)

2. **empleos**
   - id, titulo, descripcion, empresa
   - ubicacion, salario, tipo_contrato
   - experiencia_requerida, fecha_publicacion
   - empleador_id (FK a usuarios)

3. **aplicaciones**
   - id, fecha_aplicacion, estado
   - mensaje, postulante_id, empleo_id

## 👤 Usuarios de Prueba

- **Administrador**: admin@workify.com / admin123
- **Tipo**: Empleador

## 🎯 Funcionalidades

### Para Postulantes:
- ✅ Registro e inicio de sesión
- ✅ Ver empleos disponibles
- ✅ Aplicar a empleos
- ✅ Ver estado de aplicaciones

### Para Empleadores:
- ✅ Publicar empleos
- ✅ Ver aplicaciones recibidas
- ✅ Gestionar empleos publicados

## 🔧 Configuración de Desarrollo

### Variables de Entorno (Opcional)
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### Estructura del Proyecto
```
PROYECTO_POO/
├── hello.py              # Aplicación principal
├── models.py             # Modelos de base de datos
├── forms.py              # Formularios
├── config.py             # Configuración
├── setup_database.py     # Script de configuración DB
├── static/               # Archivos estáticos
│   ├── *.css
│   └── images/
└── templates/            # Plantillas HTML
    ├── inicio.html
    ├── Forms.html
    ├── login.html
    └── Vusuario.html
```

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
py -m pip install flask flask-wtf wtforms flask-sqlalchemy pymysql
```

### Error: "Access denied for user 'root'"
- Verifica las credenciales en `config.py`
- Asegúrate de que MySQL esté corriendo
- Crea el usuario si es necesario

### Error: "Database doesn't exist"
```bash
py setup_database.py
```

## 📝 Próximas Mejoras

- [ ] Dashboard para empleadores
- [ ] Sistema de notificaciones
- [ ] Filtros de búsqueda avanzados
- [ ] Subida de CVs
- [ ] Sistema de mensajería
- [ ] API REST

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**Desarrollado con ❤️ para la UPQ** 