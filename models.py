# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash

# db = SQLAlchemy()

# class Usuario(db.Model):
#     __tablename__ = 'usuarios'
    
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     ciudad = db.Column(db.String(100))
#     codigo_postal = db.Column(db.String(10))
#     fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
#     tipo_usuario = db.Column(db.String(20), default='postulante')  # 'postulante' o 'empleador'
    
#     # Relaciones
#     empleos_publicados = db.relationship('Empleo', backref='empleador', lazy=True)
#     aplicaciones = db.relationship('Aplicacion', backref='postulante', lazy=True)
    
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
    
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     def __repr__(self):
#         return f'<Usuario {self.nombre}>'

# class Empleo(db.Model):
#     __tablename__ = 'empleos'
    
#     id = db.Column(db.Integer, primary_key=True)
#     titulo = db.Column(db.String(200), nullable=False)
#     descripcion = db.Column(db.Text, nullable=False)
#     empresa = db.Column(db.String(200), nullable=False)
#     ubicacion = db.Column(db.String(200), nullable=False)
#     salario = db.Column(db.String(100))
#     tipo_contrato = db.Column(db.String(50))  # 'tiempo_completo', 'medio_tiempo', 'freelance'
#     experiencia_requerida = db.Column(db.String(100))
#     fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
#     activo = db.Column(db.Boolean, default=True)
    
#     # Claves foráneas
#     empleador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
#     # Relaciones
#     aplicaciones = db.relationship('Aplicacion', backref='empleo', lazy=True)
    
#     def __repr__(self):
#         return f'<Empleo {self.titulo}>'

# class Aplicacion(db.Model):
#     __tablename__ = 'aplicaciones'
    
#     id = db.Column(db.Integer, primary_key=True)
#     fecha_aplicacion = db.Column(db.DateTime, default=datetime.utcnow)
#     estado = db.Column(db.String(20), default='pendiente')  # 'pendiente', 'revisada', 'aceptada', 'rechazada'
#     mensaje = db.Column(db.Text)
    
#     # Claves foráneas
#     postulante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
#     empleo_id = db.Column(db.Integer, db.ForeignKey('empleos.id'), nullable=False)
    
#     def __repr__(self):
#         return f'<Aplicacion {self.id}>' 