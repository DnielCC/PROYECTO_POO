from flask import Flask, render_template, redirect, url_for, request, flash, session
from forms import SignupForm, RegisterForm
from config import ConexionDB
from werkzeug.security import generate_password_hash, check_password_hash 

conexion = ConexionDB()

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/Registro', methods=["GET", "POST"])
def show_signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        contra = form.password.data
        tipo_usuario = 'aspirante'

        # Encriptar la contraseña 
        contra_hasheada = generate_password_hash(contra)

        resultado = conexion.insert_datos(
            f"INSERT INTO login (correo, contra, tipo_usuario) VALUES ('{email}', '{contra_hasheada}', '{tipo_usuario}')"
        )

        if resultado == 'ok':
            consulta = conexion.get_datos(f"SELECT id FROM login WHERE correo = '{email}' LIMIT 1")
            if consulta:
                session['user_id'] = consulta[0][0]
                session['user_type'] = tipo_usuario  
                return redirect(url_for('info'))
            else:
                flash('Error al obtener el ID del usuario después del registro.', 'error')
        else:
            flash(f'Error al registrar: {resultado}', 'error')

    return render_template("Registro.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def user_login():
    form = RegisterForm()
    if form.validate_on_submit():
        correo = form.Email.data
        password = form.password.data

        # Obtener usuario 
        query = f"SELECT id, contra, tipo_usuario FROM login WHERE correo = '{correo}'"
        resultado = conexion.get_datos(query)

        if resultado:
            user_id = resultado[0][0]
            stored_hash = resultado[0][1]  # Hash guardado en la BD
            user_type = resultado[0][2]

            # Verificar contraseña 
            if check_password_hash(stored_hash, password):
                session['user_id'] = user_id
                session['user_type'] = user_type
                flash('Inicio de sesión exitoso.', 'success')

                if user_type == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('inicio_usuarios'))
            else:
                form.Email.errors.append('Correo o contraseña incorrectos.')
        else:
            form.Email.errors.append('Correo o contraseña incorrectos.')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('inicio'))

@app.route('/Registro/informacion', methods=['GET', 'POST'])
def info():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para continuar.', 'error')
        return redirect(url_for('user_login'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        empleo = request.form.get('empleos_deseados')
        experiencia = request.form.get('experiencia_previa')
        grado = request.form.get('grado_estudio')
        ciudad = request.form.get('ciudad')
        cp = request.form.get('codigo_postal')

        # Obtener el ID del usuario desde la sesión
        id_usuario = session['user_id']

        try:

            # Buscar ID de empleo
            id_empleo = conexion.get_datos(
                f"SELECT id FROM empleos WHERE empleo LIKE BINARY '{empleo}' LIMIT 1")
            if not id_empleo:
                flash("Error: empleo no encontrado.", 'error')
                return redirect(url_for('info'))
            id_empleo = id_empleo[0][0]

            # Buscar ID de experiencia
            id_exp = conexion.get_datos(
                f"SELECT id FROM experiencia WHERE experiencia LIKE BINARY '{experiencia}' LIMIT 1")
            if not id_exp:
                flash("Error: experiencia no encontrada.", 'error')
                return redirect(url_for('info'))
            id_exp = id_exp[0][0]

            # Buscar ID de grado de estudios
            id_grado = conexion.get_datos(
                f"SELECT id FROM grado_estudios WHERE grado LIKE BINARY '{grado}' LIMIT 1")
            if not id_grado:
                flash("Error: grado de estudios no encontrado.", 'error')
                return redirect(url_for('info'))
            id_grado = id_grado[0][0]

            # Buscar ID de ciudad
            id_ciudad = conexion.get_datos(
                f"SELECT id FROM ciudad_referencia WHERE ciudad LIKE BINARY '{ciudad}' LIMIT 1")
            if not id_ciudad:
                flash("Error: ciudad no encontrada.", 'error')
                return redirect(url_for('info'))
            id_ciudad = id_ciudad[0][0]

            # Insertar CP si no existe
            id_cp_data = conexion.get_datos(f"SELECT id FROM cp WHERE cp = '{cp}' LIMIT 1")
            if not id_cp_data:
                conexion.insert_datos(f"INSERT INTO cp (cp) VALUES ('{cp}')")
                id_cp_data = conexion.get_datos(f"SELECT id FROM cp WHERE cp = '{cp}' ORDER BY id DESC LIMIT 1")
            id_cp = id_cp_data[0][0]

            insert_info = f"""
            INSERT INTO informacion (
                id_usuario, nombre, apellidos, id_empleos, id_experiencia, id_grado_estudios, id_ciudad, id_cp
            ) VALUES (
                {id_usuario}, '{nombre}', '{apellidos}', {id_empleo}, {id_exp}, {id_grado}, {id_ciudad}, {id_cp}
            )
            """
            resultado = conexion.insert_datos(insert_info)

            if resultado == 'ok':
                flash('Información guardada correctamente.', 'success')
                return redirect(url_for('inicio_usuarios'))
            else:
                flash(f'Error en el guardado: {resultado}', 'error')
        except Exception as e:
            flash(f'Error inesperado: {str(e)}', 'error')

    return render_template('Info_users.html')

@app.route('/inicio/usuarios')
def inicio_usuarios():
    return render_template('inicio_usuarios.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    query = """
        SELECT 
            login.correo,
            login.tipo_usuario,
            informacion.nombre,
            informacion.apellidos,
            empleos.empleo,
            experiencia.experiencia,
            grado_estudios.grado,
            ciudad_referencia.ciudad,
            cp.cp
        FROM informacion
        INNER JOIN login ON informacion.id_usuario = login.id
        INNER JOIN empleos ON informacion.id_empleos = empleos.id
        INNER JOIN experiencia ON informacion.id_experiencia = experiencia.id
        INNER JOIN grado_estudios ON informacion.id_grado_estudios = grado_estudios.id
        INNER JOIN ciudad_referencia ON informacion.id_ciudad = ciudad_referencia.id
        INNER JOIN cp ON informacion.id_cp = cp.id
    """
    usuarios = conexion.get_datos(query)
    return render_template('dashboard_admin.html', usuarios=usuarios)


@app.route('/usuario/perfil')
def perfil_usuario():
    return render_template('perfil.html')

if __name__ == "__main__":
    app.run(debug=True)
    