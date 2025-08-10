from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from forms import SignupForm, RegisterForm
from config import ConexionDB
import mysql.connector

conexion = ConexionDB()

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

# ------------ RUTA DE INICIO --------
@app.route('/')
def inicio():
    return render_template('inicio.html')
#----------------------------------------

# ---------- RUTA DE REGISTRO Y LOGIN ----------
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

        query = f"SELECT id, tipo_usuario, username FROM login WHERE correo = '{correo}' AND contra = '{password}'"
        resultado = conexion.get_datos(query)

        if resultado:
            session['user_id'] = resultado[0][0]
            session['user_type'] = resultado[0][1]
            session['username'] = resultado[0][2]  # Almacenar el username en sesión
            flash('Inicio de sesión exitoso.', 'success')

            if session['user_type'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif session['user_type'] == 'reclutador':
                return redirect(url_for('reclutador_dashboard'))
            else:
                return redirect(url_for('inicio_usuarios'))
        else:
            flash('Correo o contraseña incorrectos.', 'error')

    return render_template('login.html', form=form)
#------------END RUTA DE REGISTRO Y LOGIN ----------


# ---------- RUTA DE INFORMACIÓN DEL USUARIO ----------
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


@app.route('/user/perfil')
def perfil_usuario():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    user_id = session['user_id']

    query = f"""
        SELECT nombre, apellidos, 
               empleos.empleo, experiencia.experiencia, 
               grado_estudios.grado, ciudad_referencia.ciudad, cp.cp
        FROM informacion
        INNER JOIN empleos ON informacion.id_empleos = empleos.id
        INNER JOIN experiencia ON informacion.id_experiencia = experiencia.id
        INNER JOIN grado_estudios ON informacion.id_grado_estudios = grado_estudios.id
        INNER JOIN ciudad_referencia ON informacion.id_ciudad = ciudad_referencia.id
        INNER JOIN cp ON informacion.id_cp = cp.id
        WHERE informacion.id_usuario = {user_id}
    """

    resultado = conexion.get_datos(query)

    if resultado:
        datos = resultado[0]
        usuario = {
            'nombre_completo': datos[0] + ' ' + datos[1],
            'empleo': datos[2],
            'experiencia': datos[3],
            'grado': datos[4],
            'ciudad': datos[5],
            'codigo_postal': datos[6]
        }
    else:
        flash("Perfil no encontrado. Completa tu información.", "info")
        usuario = None

    return render_template('user_perfil.html', usuario=usuario)


@app.route('/user/postulaciones')
def mis_postulaciones():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para continuar.', 'error')
        return redirect(url_for('user_login'))
    
    return render_template('mis_postulaciones.html')

#----------END RUTA DE INFORMACIÓN DEL USUARIO ----------

#----------ADMIN DASHBOARD----------
@app.route('/admin/dashboard')
def admin_dashboard():
    query = """
        SELECT 
            id, correo, tipo_usuario, username
        FROM login
        WHERE tipo_usuario IN ('admin', 'reclutador')
    """
    usuarios = conexion.get_datos(query)
    return render_template('dashboard_admin.html', usuarios=usuarios)

@app.route('/admin/agregar_usuario', methods=['POST'])
def agregar_usuario():
    username = request.form['username']
    correo = request.form['correo']
    contra = request.form['contra']
    tipo_usuario = request.form['tipo_usuario']
    
    if tipo_usuario in ['admin', 'reclutador']:
        query = f"""
            INSERT INTO login (username, correo, contra, tipo_usuario) 
            VALUES ('{username}', '{correo}', '{contra}', '{tipo_usuario}')
        """
        conexion.insert_datos(query)
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
    username = request.form['username']
    correo = request.form['correo']
    contra = request.form['contra']
    tipo_usuario = request.form['tipo_usuario']
    
    if tipo_usuario in ['admin', 'reclutador']:
        update_fields = [
            f"username='{username}'",
            f"correo='{correo}'",
            f"tipo_usuario='{tipo_usuario}'"
        ]
        if contra:  # Solo actualiza si se escribió algo
            update_fields.append(f"contra='{contra}'")
        
        update_query = f"UPDATE login SET {', '.join(update_fields)} WHERE id={id}"
        conexion.insert_datos(update_query)
        flash('Usuario editado correctamente.', 'success')
    else:
        flash('Solo puedes editar administradores o reclutadores.', 'error')
    return redirect(url_for('admin_dashboard'))
#----------END ADMIN DASHBOARD----------


# --------- RECLUTADOR DASHBOARD ---------
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

@app.route('/reclutador/crear_vacante', methods=['GET', 'POST'])
def reclutador_crear_vacante():
    if request.method == 'POST':
        conexion = None
        cursor = None
        try:
            # Obtener datos del formulario
            titulo = request.form['job_title']
            nombre_empresa = request.form['company']
            ubicacion_str = request.form['location']
            tipo_trabajo = request.form['job_type']
            modalidad = request.form['work_mode']
            salario_min = request.form.get('salary_min')
            salario_max = request.form.get('salary_max')
            experiencia = request.form['experience_level']
            fecha_limite = request.form.get('deadline')
            num_vacantes = request.form.get('vacancies_count', 1)
            descripcion = request.form['job_description']
            requisitos = request.form['requirements']
            beneficios = request.form.get('benefits', '')
            email_contacto = request.form['contact_email']
            telefono_contacto = request.form.get('contact_phone', '')
            habilidades_req = [h.strip() for h in request.form.get('skills', '').split(',') if h.strip()]
            habilidades_des = [h.strip() for h in request.form.get('nice_to_have', '').split(',') if h.strip()]

            # Procesar ubicación (ciudad, estado, país)
            ubicacion_parts = [part.strip() for part in ubicacion_str.split(',')]
            ciudad = ubicacion_parts[0] if len(ubicacion_parts) > 0 else ''
            estado = ubicacion_parts[1] if len(ubicacion_parts) > 1 else ''
            pais = ubicacion_parts[2] if len(ubicacion_parts) > 2 else ''

            # Mapear valores de los select a IDs de la base de datos
            tipo_trabajo_map = {
                'full-time': 1,
                'part-time': 2,
                'contract': 3,
                'internship': 4
            }
            
            modalidad_map = {
                'presencial': 1,
                'remote': 2,
                'hybrid': 3
            }
            
            experiencia_map = {
                'entry': 1,
                'junior': 2,
                'mid': 3,
                'senior': 4,
                'lead': 5
            }

            # Iniciar conexión usando tu clase ConexionDB
            conexion = ConexionDB()
            if not conexion.connection:
                flash(f'Error de conexión: {conexion.errMss}', 'danger')
                return redirect(url_for('reclutador_crear_vacante'))

            cursor = conexion.connection.cursor(dictionary=True)

            # 1. Insertar empresa si no existe
            cursor.execute("SELECT id FROM empresas WHERE nombre = %s", (nombre_empresa,))
            empresa = cursor.fetchone()
            if not empresa:
                cursor.execute("INSERT INTO empresas (nombre) VALUES (%s)", (nombre_empresa,))
                empresa_id = cursor.lastrowid
                conexion.connection.commit()
            else:
                empresa_id = empresa['id']

            # 2. Insertar ubicación si no existe
            cursor.execute(
                "SELECT id FROM ubicaciones WHERE ciudad = %s AND estado = %s AND pais = %s",
                (ciudad, estado, pais)
            )
            ubicacion = cursor.fetchone()
            if not ubicacion:
                cursor.execute(
                    "INSERT INTO ubicaciones (ciudad, estado, pais) VALUES (%s, %s, %s)",
                    (ciudad, estado, pais)
                )
                ubicacion_id = cursor.lastrowid
                conexion.connection.commit()
            else:
                ubicacion_id = ubicacion['id']

            # 3. Insertar la vacante
            cursor.execute(
                """INSERT INTO vacantes (
                    id_empresa, titulo, id_ubicacion, id_tipo_trabajo, 
                    id_modalidad_trabajo, salario_minimo, salario_maximo, 
                    id_nivel_experiencia, fecha_limite, numero_vacantes, 
                    descripcion, requisitos, beneficios, email_contacto, 
                    telefono_contacto
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    empresa_id, titulo, ubicacion_id, tipo_trabajo_map[tipo_trabajo],
                    modalidad_map[modalidad], salario_min, salario_max,
                    experiencia_map[experiencia], fecha_limite, num_vacantes,
                    descripcion, requisitos, beneficios, email_contacto,
                    telefono_contacto
                )
            )
            vacante_id = cursor.lastrowid
            conexion.connection.commit()

            # 4. Procesar habilidades requeridas
            for habilidad in habilidades_req:
                # Verificar si la habilidad existe
                cursor.execute("SELECT id FROM habilidades WHERE nombre = %s", (habilidad,))
                habilidad_db = cursor.fetchone()
                if not habilidad_db:
                    cursor.execute("INSERT INTO habilidades (nombre) VALUES (%s)", (habilidad,))
                    habilidad_id = cursor.lastrowid
                    conexion.connection.commit()
                else:
                    habilidad_id = habilidad_db['id']
                
                # Relacionar habilidad con vacante
                cursor.execute(
                    "INSERT INTO vacantes_habilidades_requeridas (id_vacante, id_habilidad) VALUES (%s, %s)",
                    (vacante_id, habilidad_id)
                )
                conexion.connection.commit()

            # 5. Procesar habilidades deseadas
            for habilidad in habilidades_des:
                # Verificar si la habilidad existe
                cursor.execute("SELECT id FROM habilidades WHERE nombre = %s", (habilidad,))
                habilidad_db = cursor.fetchone()
                if not habilidad_db:
                    cursor.execute("INSERT INTO habilidades (nombre) VALUES (%s)", (habilidad,))
                    habilidad_id = cursor.lastrowid
                    conexion.connection.commit()
                else:
                    habilidad_id = habilidad_db['id']
                
                # Relacionar habilidad con vacante
                cursor.execute(
                    "INSERT INTO vacantes_habilidades_deseadas (id_vacante, id_habilidad) VALUES (%s, %s)",
                    (vacante_id, habilidad_id)
                )
                conexion.connection.commit()

            flash('Vacante creada exitosamente!', 'success')
            return redirect(url_for('reclutador_vacantes'))

        except mysql.connector.Error as err:
            if conexion and conexion.connection:
                conexion.connection.rollback()
            flash(f'Error al crear la vacante: {err}', 'danger')
        except Exception as ex:
            flash(f'Error inesperado: {ex}', 'danger')
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.connection:
                conexion.connection.close()

    # Para el método GET, simplemente renderizar el template
    return render_template('reclutador/crear_vacante.html')   

#---------- END RECLUTADOR DASHBOARD ---------


#---------- RUTA DE CIERRE DE SESIÓN ----------
@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('inicio'))
#----------------------------------------------

#---------- RUTA DE EDITAR PERFIL ----------
@app.route('/user/editar_perfil', methods=['GET', 'POST'])
def editar_perfil_usuario():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para continuar.', 'error')
        return redirect(url_for('user_login'))

    user_id = session['user_id']

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        empleo = request.form.get('empleos_deseados')
        experiencia = request.form.get('experiencia_previa')
        grado = request.form.get('grado_estudio')
        ciudad = request.form.get('ciudad')
        cp = request.form.get('codigo_postal')

        try:
            # Buscar IDs relacionados igual que en info()
            id_empleo = conexion.get_datos(f"SELECT id FROM empleos WHERE empleo LIKE BINARY '{empleo}' LIMIT 1")[0][0]
            id_exp = conexion.get_datos(f"SELECT id FROM experiencia WHERE experiencia LIKE BINARY '{experiencia}' LIMIT 1")[0][0]
            id_grado = conexion.get_datos(f"SELECT id FROM grado_estudios WHERE grado LIKE BINARY '{grado}' LIMIT 1")[0][0]
            id_ciudad = conexion.get_datos(f"SELECT id FROM ciudad_referencia WHERE ciudad LIKE BINARY '{ciudad}' LIMIT 1")[0][0]

            # Insertar CP si no existe
            id_cp_data = conexion.get_datos(f"SELECT id FROM cp WHERE cp = '{cp}' LIMIT 1")
            if not id_cp_data:
                conexion.insert_datos(f"INSERT INTO cp (cp) VALUES ('{cp}')")
                id_cp_data = conexion.get_datos(f"SELECT id FROM cp WHERE cp = '{cp}' ORDER BY id DESC LIMIT 1")
            id_cp = id_cp_data[0][0]

            # Actualizar datos
            update_query = f"""
                UPDATE informacion
                SET nombre = '{nombre}', apellidos = '{apellidos}',
                    id_empleos = {id_empleo}, id_experiencia = {id_exp},
                    id_grado_estudios = {id_grado}, id_ciudad = {id_ciudad},
                    id_cp = {id_cp}
                WHERE id_usuario = {user_id}
            """
            conexion.insert_datos(update_query)

            flash('Perfil actualizado correctamente.', 'success')
            return redirect(url_for('perfil_usuario'))

        except Exception as e:
            flash(f'Error al actualizar: {e}', 'error')

    # Si es GET, traer datos actuales para mostrarlos en el formulario
    query = f"""
        SELECT nombre, apellidos, empleos.empleo, experiencia.experiencia, 
               grado_estudios.grado, ciudad_referencia.ciudad, cp.cp
        FROM informacion
        INNER JOIN empleos ON informacion.id_empleos = empleos.id
        INNER JOIN experiencia ON informacion.id_experiencia = experiencia.id
        INNER JOIN grado_estudios ON informacion.id_grado_estudios = grado_estudios.id
        INNER JOIN ciudad_referencia ON informacion.id_ciudad = ciudad_referencia.id
        INNER JOIN cp ON informacion.id_cp = cp.id
        WHERE informacion.id_usuario = {user_id}
    """
    datos = conexion.get_datos(query)
    if not datos:
        flash("No tienes información registrada. Por favor complétala primero.", "info")
        return redirect(url_for('info'))

    usuario = {
        'nombre': datos[0][0],
        'apellidos': datos[0][1],
        'empleo': datos[0][2],
        'experiencia': datos[0][3],
        'grado': datos[0][4],
        'ciudad': datos[0][5],
        'codigo_postal': datos[0][6]
    }

    return render_template('editar_perfil.html', usuario=usuario)
#----------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)
    