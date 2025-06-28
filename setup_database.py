import pymysql
from config import DevelopmentConfig
from models import db, Usuario, Empleo, Aplicacion
from flask import Flask

def create_database():
    """Crear la base de datos MySQL si no existe"""
    try:
        # Conectar a MySQL sin especificar base de datos
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='12345',  # Cambiar por tu contraseña de MySQL
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Crear la base de datos
        cursor.execute("CREATE DATABASE IF NOT EXISTS bolsa_trabajo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Base de datos 'bolsa_trabajo' creada exitosamente!")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error al crear la base de datos: {e}")
        print("\n📋 Pasos para configurar MySQL:")
        print("1. Instala MySQL Server")
        print("2. Configura un usuario root con contraseña")
        print("3. Actualiza la contraseña en config.py")
        return False
    
    return True

def create_tables():
    """Crear las tablas usando SQLAlchemy"""
    try:
        # Crear aplicación Flask temporal
        app = Flask(__name__)
        app.config.from_object(DevelopmentConfig)
        
        # Inicializar la base de datos
        db.init_app(app)
        
        with app.app_context():
            # Crear todas las tablas
            db.create_all()
            print("✅ Tablas creadas exitosamente!")
            
            # Crear usuario administrador de ejemplo
            admin = Usuario.query.filter_by(email='admin@workify.com').first()
            if not admin:
                admin = Usuario(
                    nombre='Administrador',
                    email='admin@workify.com',
                    tipo_usuario='empleador'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario administrador creado (admin@workify.com / admin123)")
            
            # Crear algunos empleos de ejemplo
            if Empleo.query.count() == 0:
                empleos_ejemplo = [
                    {
                        'titulo': 'Desarrollador Python',
                        'descripcion': 'Buscamos un desarrollador Python con experiencia en Flask y Django.',
                        'empresa': 'TechCorp',
                        'ubicacion': 'Querétaro, QRO',
                        'salario': '$25,000 - $35,000 MXN',
                        'tipo_contrato': 'tiempo_completo',
                        'experiencia_requerida': '2-3 años'
                    },
                    {
                        'titulo': 'Diseñador UX/UI',
                        'descripcion': 'Diseñador creativo para mejorar la experiencia de usuario.',
                        'empresa': 'DesignStudio',
                        'ubicacion': 'Querétaro, QRO',
                        'salario': '$20,000 - $30,000 MXN',
                        'tipo_contrato': 'tiempo_completo',
                        'experiencia_requerida': '1-2 años'
                    }
                ]
                
                for empleo_data in empleos_ejemplo:
                    empleo = Empleo(**empleo_data, empleador_id=admin.id)
                    db.session.add(empleo)
                
                db.session.commit()
                print("✅ Empleos de ejemplo creados!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear las tablas: {e}")
        return False

def main():
    print("🚀 Configurando base de datos para Bolsa de Trabajo...")
    print("=" * 50)
    
    # Crear base de datos
    if create_database():
        # Crear tablas
        if create_tables():
            print("\n🎉 ¡Configuración completada exitosamente!")
            print("\n📋 Próximos pasos:")
            print("1. Ejecuta: py hello.py")
            print("2. Abre: http://127.0.0.1:5000")
            print("3. Registra un nuevo usuario o usa admin@workify.com / admin123")
        else:
            print("\n❌ Error al crear las tablas")
    else:
        print("\n❌ Error al crear la base de datos")

if __name__ == "__main__":
    main() 