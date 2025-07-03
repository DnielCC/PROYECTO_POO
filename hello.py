from flask import Flask, render_template, redirect, url_for, request, flash, session
from forms import SignupForm, RegisterForm
from models import db, Usuario, Empleo, Aplicacion
from config import config
import os

app = Flask(__name__)
app.config.from_object(config['development'])

# Inicializar la base de datos
db.init_app(app)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/Forms', methods=["GET", "POST"])
def show_signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Verificar si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(email=form.email.data).first()
        if usuario_existente:
            flash('El email ya está registrado. Por favor, usa otro email.', 'error')
            return render_template("Forms.html", form=form)
        
        # Verificar que las contraseñas coincidan
        if form.password.data != form.confirmpassword.data:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template("Forms.html", form=form)
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre=form.name.data,
            email=form.email.data
        )
        nuevo_usuario.set_password(form.password.data)
         
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('user_login'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar. Por favor, intenta de nuevo.', 'error')
            print(f"Error: {e}")
    
    return render_template("Forms.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def user_login():
    form = RegisterForm()
    if form.validate_on_submit():
        # Buscar usuario por email
        usuario = Usuario.query.filter_by(email=form.Email.data).first()
        
        if usuario and usuario.check_password(form.password.data):
            # Iniciar sesión
            session['user_id'] = usuario.id
            session['user_name'] = usuario.nombre
            session['user_type'] = usuario.tipo_usuario
            flash(f'¡Bienvenido, {usuario.nombre}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('inicio'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder al dashboard.', 'error')
        return redirect(url_for('user_login'))
    
    usuario = Usuario.query.get(session['user_id'])
    if usuario.tipo_usuario == 'empleador':
        # Mostrar empleos publicados por el empleador
        empleos = Empleo.query.filter_by(empleador_id=usuario.id).all()
        return render_template('dashboard_empleador.html', usuario=usuario, empleos=empleos)
    else:
        # Mostrar empleos disponibles para postulantes
        empleos = Empleo.query.filter_by(activo=True).all()
        return render_template('dashboard_postulante.html', usuario=usuario, empleos=empleos)

@app.route('/login/informacion', methods=['GET', 'POST'])
def info():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para completar tu perfil.', 'error')
        return redirect(url_for('user_login'))
    
    if request.method == 'POST':
        usuario = Usuario.query.get(session['user_id'])
        usuario.ciudad = request.form.get('ciudad')
        usuario.codigo_postal = request.form.get('codigo_postal')
        
        try:
            db.session.commit()
            flash('Información actualizada exitosamente.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar la información.', 'error')
            print(f"Error: {e}")
    
    return render_template('Vusuario.html')

# Crear las tablas de la base de datos
def create_tables():
    with app.app_context():
        db.create_all()
        print("✅ Tablas creadas exitosamente!")
        
        # Crear usuario administrador si no existe
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

if __name__ == "__main__":
    # Crear las tablas si no existen
    create_tables()
    app.run(debug=True)

