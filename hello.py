from flask import Flask, render_template, redirect, url_for, request, flash, session
from forms import SignupForm, RegisterForm
from config import ConexionDB

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

        consulta = conexion.get_datos(f"SELECT * FROM login WHERE correo = '{email}'")

        if len(consulta) > 0:
            return render_template("Registro.html", form=form)

        if form.password.data != form.confirmpassword.data:
            return render_template("Registro.html", form=form)

        resultado = conexion.insert_datos(
            f"INSERT INTO login (correo, contra, tipo_usuario) VALUES ('{email}', '{contra}', '{tipo_usuario}')"
        )

        if resultado == 'ok':
            flash('¡Registro exitoso!', 'success')
            return redirect(url_for('info'))
        else:
            flash(f'Error al registrar: {resultado}', 'error')

    return render_template("Registro.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def user_login():
    form = RegisterForm()
    if form.validate_on_submit():
        correo = form.Email.data
        password = form.password.data

        query = f"SELECT id, tipo_usuario FROM login WHERE correo = '{correo}' AND contra = '{password}'"
        resultado = conexion.get_datos(query)

        if resultado:
            session['user_id'] = resultado[0][0]
            session['user_type'] = resultado[0][1]
            flash('Inicio de sesión exitoso.', 'success')

            if session['user_type'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('inicio_usuarios'))
        else:
            flash('Correo o contraseña incorrectos.', 'error')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('inicio'))

@app.route('/reclutador/dashboard')
def reclutador_dashboard():
    
    return render_template('reclutador/dashboard.html')

@app.route('/reclutador/vacantes')
def reclutador_vacantes():

    return render_template('reclutador/vacantes.html')

@app.route('/reclutador/postulaciones')
def reclutador_postulaciones():
    
    return render_template('reclutador/postulaciones.html')

@app.route('/reclutador/candidato/<int:id>')
def reclutador_candidato(id):
  
    return render_template('reclutador/candidato.html')

@app.route('/reclutador/crear_vacante')
def reclutador_crear_vacante():
  
    return render_template('reclutador/crear_vacante.html')    



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

#----------ADMIN DASHBOARD----------
@app.route('/admin/dashboard')
def admin_dashboard():
    query = """
        SELECT 
            id, correo, tipo_usuario
        FROM login
        WHERE tipo_usuario IN ('admin', 'reclutador')
    """
    usuarios = conexion.get_datos(query)
    return render_template('dashboard_admin.html', usuarios=usuarios)

@app.route('/admin/agregar_usuario', methods=['POST'])
def agregar_usuario():
    correo = request.form['correo']
    contra = request.form['contra']
    tipo_usuario = request.form['tipo_usuario']
    # Solo admins y reclutadores
    if tipo_usuario in ['admin', 'reclutador']:
        conexion.insert_datos(f"INSERT INTO login (correo, contra, tipo_usuario) VALUES ('{correo}', '{contra}', '{tipo_usuario}')")
        flash('Usuario agregado correctamente.', 'success')
    else:
        flash('Solo puedes agregar administradores o reclutadores.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    usuario = conexion.get_datos(f"SELECT tipo_usuario FROM login WHERE id={id}")
    if usuario and usuario[0][0] in ['admin', 'reclutador']:
        conexion.insert_datos(f"DELETE FROM login WHERE id={id}")
        flash('Usuario eliminado correctamente.', 'success')
    else:
        flash('No puedes eliminar aspirantes desde aquí.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/editar_usuario/<int:id>', methods=['POST'])
def editar_usuario(id):
    correo = request.form['correo']
    contra = request.form['contra']
    tipo_usuario = request.form['tipo_usuario']
    # Solo admins y reclutadores
    if tipo_usuario in ['admin', 'reclutador']:
        update_fields = []
        if correo:
            update_fields.append(f"correo='{correo}'")
        if contra:  # Solo actualiza si se escribió algo
            update_fields.append(f"contra='{contra}'")
        update_fields.append(f"tipo_usuario='{tipo_usuario}'")
        update_query = f"UPDATE login SET {', '.join(update_fields)} WHERE id={id}"
        conexion.insert_datos(update_query)
        flash('Usuario editado correctamente.', 'success')
    else:
        flash('Solo puedes editar administradores o reclutadores.', 'error')
    return redirect(url_for('admin_dashboard'))
#----------END ADMIN DASHBOARD----------

@app.route('/user/perfil')
def perfil():
   return render_template('user_perfil.html')

@app.route('/user/postulaciones')
def mis_postulaciones():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para continuar.', 'error')
        return redirect(url_for('user_login'))
    
    return render_template('mis_postulaciones.html')


if __name__ == "__main__":
    app.run(debug=True)
    